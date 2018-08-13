import bpy
import random

# filename = "/home/dacoda/projects/benjamin-blender/testing.py"; exec(compile(open(filename).read(), filename, 'exec'))

def delete_objects():
    """ 
    https://blender.stackexchange.com/questions/27234/python-how-to-completely-remove-an-object
    """
    for object in bpy.data.objects:
        if object.type != 'LAMP' and object.type != 'CAMERA':
            object.select = True
        else:
            object.select = False

    bpy.ops.object.delete()

delete_objects()

bpy.ops.mesh.primitive_grid_add(radius=10.0, location=(0, 0, 0))

for i in range(1):
    print("Adding cube")
    radius = 0.5 + .5 * random.random()
    random_location = lambda: 5 * (1.0 - 2 * random.random())
    location = (random_location(), random_location(), radius)
    bpy.ops.mesh.primitive_cube_add(radius=radius, location=location)

image = bpy.data.images.load("/home/dacoda/38060952_1802198976527082_8340015869589454848_n.jpg")
tex = bpy.data.textures.new('MemeTexture', 'IMAGE')
tex.image = image

mat = bpy.data.materials.new('MemeMaterial')
mat.texture_slots.add()
ts = mat.texture_slots[0]
ts.texture = tex
ts.texture_coords = 'UV'
ts.uv_layer = 'default'

# bpy.data.objects["Cube"].data.polygons[0].select = True
# bpy.context.active_object.data.materials.append(mat)

# bpy.data.objects["Cube"].data.polygons[0].materials.append(mat)


for face in range(6):

    bpy.data.objects["Cube"].data.polygons[face].select = True

    bpy.ops.object.mode_set(mode='EDIT')

    bpy.context.tool_settings.mesh_select_mode = [False, False, True]
    bpy.ops.uv.unwrap()
    bpy.data.objects["Cube"].active_material = mat
    bpy.ops.object.material_slot_assign()

    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.data.objects["Cube"].data.polygons[face].select = False
