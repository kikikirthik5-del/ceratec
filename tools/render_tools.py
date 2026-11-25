"""Procedural cutting-tool renders for the Ceratec site.

Run:  blender -b -P tools/render_tools.py -- <out_dir> [item ...] [--fast]
Items: hero endmill ballnose drill threadmill reamer insert  (default: all)
Each tool is real geometry: a flute cross-section swept along a helix, a ground
carbide shank with a painted ID ring, and a coated cutting body.
"""
import bpy, bmesh, math, sys, os
from mathutils import Vector, Quaternion

argv = sys.argv[sys.argv.index('--') + 1:]
OUT = argv[0]
FAST = '--fast' in argv
ITEMS = [a for a in argv[1:] if not a.startswith('--')] or ['hero', 'endmill', 'ballnose', 'drill', 'threadmill', 'reamer', 'insert']
os.makedirs(OUT, exist_ok=True)


# ---------- scene / render ----------
def reset(w, h):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 24 if FAST else 56
    sc.cycles.use_denoising = True
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for t in ('OPTIX', 'CUDA', 'HIP', 'ONEAPI'):
            try:
                prefs.compute_device_type = t
                prefs.get_devices()
                if any(d.type == t for d in prefs.devices):
                    for d in prefs.devices:
                        d.use = d.type == t
                    sc.cycles.device = 'GPU'
                    break
            except Exception:
                pass
    except Exception:
        pass
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'WEBP'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.render.image_settings.quality = 90
    sc.view_settings.view_transform = 'AgX'
    try:
        sc.view_settings.look = 'AgX - Medium High Contrast'
    except Exception:
        pass
    # Studio environment: dark floor, bright ceiling, so metal shows a horizon line
    world = bpy.data.worlds.new('studio')
    sc.world = world
    world.use_nodes = True
    nt = world.node_tree
    tc = nt.nodes.new('ShaderNodeTexCoord')
    sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.42
    ramp.color_ramp.elements[0].color = (0.02, 0.025, 0.035, 1)
    ramp.color_ramp.elements[1].position = 0.62
    ramp.color_ramp.elements[1].color = (0.85, 0.86, 0.9, 1)
    mp = nt.nodes.new('ShaderNodeMapRange')
    mp.inputs['From Min'].default_value, mp.inputs['From Max'].default_value = -1, 1
    bg = nt.nodes['Background']
    bg.inputs['Strength'].default_value = 0.55
    nt.links.new(tc.outputs['Generated'], sep.inputs[0])
    nt.links.new(sep.outputs['Z'], mp.inputs['Value'])
    nt.links.new(mp.outputs['Result'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bg.inputs['Color'])
    return sc


def look_at(obj, target, roll=0.0):
    d = (Vector(target) - obj.location).normalized()
    q = d.to_track_quat('-Z', 'Y')
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = q @ Quaternion((0, 0, 1), roll)


def area(name, loc, size, energy, target=(0, 0, 0), color=(1, 1, 1)):
    data = bpy.data.lights.new(name, 'AREA')
    data.shape = 'RECTANGLE'
    data.size, data.size_y = size
    data.energy = energy
    data.color = color
    ob = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    look_at(ob, target)
    return ob


def studio(s, cz=0.0):
    """Long strip softboxes give the stretched highlights real ground metal shows."""
    area('key', (-3.2 * s, -3.4 * s, cz), (0.35 * s, 9 * s), 420 * s * s, (0, 0, cz))
    area('fill', (3.6 * s, -2.6 * s, cz), (0.6 * s, 9 * s), 160 * s * s, (0, 0, cz), (0.93, 0.96, 1))
    area('rim', (1.5 * s, 3.5 * s, cz + 1 * s), (0.4 * s, 9 * s), 380 * s * s, (0, 0, cz), (1, 0.93, 0.86))
    area('top', (0, -1.2 * s, cz + 7 * s), (3 * s, 3 * s), 120 * s * s, (0, 0, cz))


def camera(ortho_scale=None, loc=(0, -30, 0), target=(0, 0, 0), roll=0.0, lens=85):
    data = bpy.data.cameras.new('cam')
    if ortho_scale:
        data.type = 'ORTHO'
        data.ortho_scale = ortho_scale
    else:
        data.lens = lens
    data.clip_end = 500
    cam = bpy.data.objects.new('cam', data)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = loc
    look_at(cam, target, roll)
    bpy.context.scene.camera = cam
    return cam


# ---------- materials ----------
def principled(name, color, metallic, rough, aniso=0.0, rings=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*color, 1)
    b.inputs['Metallic'].default_value = metallic
    b.inputs['Roughness'].default_value = rough
    if aniso:
        b.inputs['Anisotropic'].default_value = aniso
    if rings:  # circumferential grinding marks
        tc = nt.nodes.new('ShaderNodeTexCoord')
        wave = nt.nodes.new('ShaderNodeTexWave')
        wave.wave_type = 'BANDS'
        wave.bands_direction = 'Z'
        wave.inputs['Scale'].default_value = rings
        wave.inputs['Distortion'].default_value = 2.0
        wave.inputs['Detail'].default_value = 6
        bump = nt.nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.06
        nt.links.new(tc.outputs['Object'], wave.inputs['Vector'])
        nt.links.new(wave.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m


def carbide():  # ground solid carbide
    return principled('carbide', (0.78, 0.79, 0.81), 1.0, 0.17, 0.35, rings=90)


def coating(kind):
    return {
        'alcrn': principled('AlCrN', (0.20, 0.23, 0.30), 1.0, 0.30),   # blue-grey
        'tialn': principled('TiAlN', (0.13, 0.11, 0.14), 1.0, 0.32),   # anthracite-violet
        'tin': principled('TiN', (0.83, 0.62, 0.24), 1.0, 0.28),      # gold
        'bright': principled('bright', (0.72, 0.73, 0.75), 1.0, 0.18),
    }[kind]


def paint():  # brand ID ring on the shank
    return principled('ring', (1.0, 0.33, 0.04), 0.0, 0.42)


# ---------- geometry ----------
def flute_radius(theta, n, depth):
    seg = 2 * math.pi / n
    phi = (theta % seg) / seg
    a, b = 0.30, 0.97
    if a < phi < b:
        u = (phi - a) / (b - a)
        return 1 - depth * math.sin(math.pi * u ** 1.6) ** 0.8  # gentle heel, steep cutting face
    return 1 - 0.025 * (phi / a if phi <= a else 0)  # land with a touch of clearance


def fluted(R, L, n, helix, depth, tip='flat', pitch=0.0, layers=None, samples=None):
    layers = layers or (120 if FAST else 420)
    samples = samples or (96 if FAST else 240)
    me = bpy.data.meshes.new('body')
    bm = bmesh.new()
    rings = []
    k_twist = math.tan(math.radians(helix)) / R
    tip_len = {'flat': 0.04 * R, 'ball': R, 'cone': R / math.tan(math.radians(59)), 'chamfer': 0.25 * R}[tip]
    for k in range(layers + 1):
        z = -L * k / layers
        d = -z - (L - tip_len)  # distance into the tip zone
        s = 1.0
        if d > 0:
            t = d / tip_len
            s = {'flat': 1 - 0.05 * t, 'ball': math.sqrt(max(0, 1 - t * t)), 'cone': 1 - t, 'chamfer': 1 - 0.3 * t}[tip]
            s = max(s, 0.002)
        thread = 1.0
        if pitch:
            w = ((-z) / pitch) % 1.0
            thread = 1 - 0.11 * (1 - abs(2 * w - 1))  # triangular thread form
        tw = -z * k_twist
        dep = depth * min(1.0, (-z) / (0.9 * R)) ** 0.7  # flutes wash out into the shank
        ring = []
        for i in range(samples):
            th = 2 * math.pi * i / samples
            r = R * flute_radius(th, n, dep) * s * thread
            ring.append(bm.verts.new((r * math.cos(th + tw), r * math.sin(th + tw), z)))
        rings.append(ring)
    for a, b in zip(rings, rings[1:]):
        for i in range(samples):
            j = (i + 1) % samples
            bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(rings[0])
    bm.faces.new(list(reversed(rings[-1])))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new('body', me)
    bpy.context.scene.collection.objects.link(ob)
    smooth(ob, 32)
    return ob


def smooth(ob, deg):
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(deg))
    except Exception:
        bpy.ops.object.shade_smooth()
    ob.select_set(False)


def cylinder(R, h, z, verts=160, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=R, depth=h, location=(0, 0, z))
    ob = bpy.context.active_object
    if bevel:
        mod = ob.modifiers.new('bevel', 'BEVEL')
        mod.width, mod.segments, mod.limit_method = bevel, 4, 'ANGLE'
    smooth(ob, 40)
    return ob


TOOLS = {
    # name: flute geometry, shank length, coating
    'endmill':    dict(R=1, L=5.0, n=4, helix=38, depth=0.34, tip='flat', S=8.4, coat='alcrn'),
    'ballnose':   dict(R=1, L=4.2, n=2, helix=30, depth=0.42, tip='ball', S=8.4, coat='tialn'),
    'drill':      dict(R=1, L=8.0, n=2, helix=30, depth=0.46, tip='cone', S=5.6, coat='tin'),
    'threadmill': dict(R=1, L=2.8, n=4, helix=12, depth=0.30, tip='flat', S=8.8, coat='tialn', pitch=0.32),
    'reamer':     dict(R=1, L=5.4, n=6, helix=0,  depth=0.16, tip='chamfer', S=7.6, coat='bright'),
}


def build_tool(spec):
    body = fluted(spec['R'], spec['L'], spec['n'], spec['helix'], spec['depth'], spec['tip'], spec.get('pitch', 0))
    body.data.materials.append(coating(spec['coat']))
    S, R = spec['S'], spec['R']
    shank = cylinder(R, S, S / 2, bevel=0.07 * R)
    shank.data.materials.append(carbide())
    ring = cylinder(R * 1.004, 0.16, S * 0.72)
    ring.data.materials.append(paint())
    neck = cylinder(R * 0.985, 0.08, 0.02)  # ground transition between shank and flutes
    neck.data.materials.append(carbide())
    return S, -spec['L']  # top z, bottom z


def render(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print('wrote', path)


def tool_shot(name, hero=False):
    spec = TOOLS[name]
    if hero:
        sc = reset(620, 2000)
    else:
        sc = reset(960, 720)
    top, bot = build_tool(spec)
    length, cz = top - bot, (top + bot) / 2
    # spin so a cutting edge faces the key light
    for ob in bpy.context.scene.objects:
        if ob.type == 'MESH':
            ob.rotation_euler.z = math.radians(25)
    studio(length / 9.5, cz)
    if hero:
        camera(length * 1.06, loc=(0, -40, cz + 3), target=(0, 0, cz))
    else:
        roll = math.radians(-52)
        w = length * abs(math.sin(roll)) + 2.2
        h = length * abs(math.cos(roll)) + 2.2
        camera(max(w, h * 960 / 720) * 1.08, loc=(0, -40, cz + 5), target=(0, 0, cz), roll=roll)
    render(os.path.join(OUT, f"{'hero-' if hero else ''}{name}.webp"))


def insert_shot():
    reset(960, 720)
    s, r_c = 12.9, 0.8          # side length, corner radius (CNMG 120408-ish)
    a, b = s * math.cos(math.radians(40)), s * math.sin(math.radians(40))
    corners = [Vector((a, 0)), Vector((0, b)), Vector((-a, 0)), Vector((0, -b))]
    pts = []
    for i, P in enumerate(corners):
        u = (corners[i - 1] - P).normalized()
        v = (corners[(i + 1) % 4] - P).normalized()
        h = math.acos(max(-1, min(1, u.dot(v)))) / 2
        c = P + (u + v).normalized() * (r_c / math.sin(h))
        p1, p2 = P + u * (r_c / math.tan(h)), P + v * (r_c / math.tan(h))
        a1, a2 = math.atan2(p1.y - c.y, p1.x - c.x), math.atan2(p2.y - c.y, p2.x - c.x)
        da = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
        for k in range(13):
            t = a1 + da * k / 12
            pts.append((c.x + r_c * math.cos(t), c.y + r_c * math.sin(t)))
    T = 4.76
    me = bpy.data.meshes.new('insert')
    bm = bmesh.new()
    bot = [bm.verts.new((x, y, -T / 2)) for x, y in pts]
    top = [bm.verts.new((x, y, T / 2)) for x, y in pts]
    bm.faces.new(top)
    bm.faces.new(list(reversed(bot)))
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ins = bpy.data.objects.new('insert', me)
    bpy.context.scene.collection.objects.link(ins)
    dark, gold = principled('CVD top', (0.06, 0.06, 0.07), 1.0, 0.36), coating('tin')
    me.materials.append(dark)
    me.materials.append(gold)
    for f in me.polygons:
        f.material_index = 0 if f.normal.z > 0.3 or f.normal.z < -0.9 else 1
    # clamping hole with countersink (cut first, edge hone bevel added after)
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=2.6, depth=T * 2, location=(0, 0, 0))
    hole = bpy.context.active_object
    bpy.ops.mesh.primitive_cone_add(vertices=96, radius1=2.6, radius2=3.7, depth=1.2, location=(0, 0, T / 2 - 0.5))
    sink = bpy.context.active_object
    # chip-breaker groove: a closed ring cutter between two scaled copies of the outline
    gm = bpy.data.meshes.new('groove')
    gb = bmesh.new()
    def loop(k, z):
        return [gb.verts.new((x * k, y * k, z)) for x, y in pts]
    zb, zt = T / 2 - 0.24, T / 2 + 1
    ob_, ot_, ib_, it_ = loop(0.93, zb), loop(0.93, zt), loop(0.80, zb), loop(0.80, zt)
    n_ = len(pts)
    for i in range(n_):
        j = (i + 1) % n_
        gb.faces.new((ob_[i], ob_[j], ot_[j], ot_[i]))   # outer wall
        gb.faces.new((ib_[j], ib_[i], it_[i], it_[j]))   # inner wall
        gb.faces.new((ot_[i], ot_[j], it_[j], it_[i]))   # top
        gb.faces.new((ob_[j], ob_[i], ib_[i], ib_[j]))   # floor
    bmesh.ops.recalc_face_normals(gb, faces=gb.faces)
    gb.to_mesh(gm)
    gb.free()
    groove = bpy.data.objects.new('groove', gm)
    bpy.context.scene.collection.objects.link(groove)
    groove.data.materials.append(dark)
    for cutter in (hole, sink, groove):
        cutter.hide_render = True
        cutter.display_type = 'WIRE'
        if not cutter.data.materials:
            cutter.data.materials.append(gold)
        m = ins.modifiers.new('hole', 'BOOLEAN')
        m.object, m.operation, m.solver = cutter, 'DIFFERENCE', 'EXACT'
        try:
            m.material_mode = 'TRANSFER'
        except Exception:
            pass
    bev = ins.modifiers.new('hone', 'BEVEL')
    bev.width, bev.segments, bev.limit_method = 0.12, 3, 'ANGLE'
    smooth(ins, 30)
    ins.rotation_euler = groove.rotation_euler = (0, 0, math.radians(18))  # cutters live in world space
    studio(2.6, 0)
    camera(None, loc=(31, -52, 46), target=(0, 0, -0.6), lens=105)
    render(os.path.join(OUT, 'insert.webp'))


for item in ITEMS:
    if item == 'hero':
        tool_shot('endmill', hero=True)
    elif item == 'insert':
        insert_shot()
    else:
        tool_shot(item)
