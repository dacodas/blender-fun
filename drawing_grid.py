# filename = "/home/dacoda/projects/benjamin-blender/drawing_grid.py"; exec(compile(open(filename).read(), filename, 'exec'))

import logging
logging.basicConfig(level=logging.DEBUG)

grid_material = bpy.data.materials.new(name="Grid Material")
grid_material.type = 'WIRE'

grid_mesh = bpy.data.meshes.new(name="Grid Mesh")
grid_bmesh = bmesh.new()

grid_size = 10

for x in range(grid_size + 1):
    for y in range(grid_size + 1):
        print("Adding point ({}, {})".format(x, y))
        grid_bmesh.verts.new((x, y, 0))

grid_bmesh.verts.ensure_lookup_table()

def point_index_from_coordinate(x, y):
    return y * (grid_size + 1) + x
    
for y in range(grid_size + 1):
    v1 = grid_bmesh.verts[point_index_from_coordinate(0, y)]
    v2 = grid_bmesh.verts[point_index_from_coordinate(grid_size, y)]
    grid_bmesh.edges.new((v1, v2))

for x in range(grid_size + 1):
    v1 = grid_bmesh.verts[point_index_from_coordinate(x, 0)]
    v2 = grid_bmesh.verts[point_index_from_coordinate(x, grid_size)]
    grid_bmesh.edges.new((v1, v2))

grid_bmesh.to_mesh(grid_mesh)

grid_object = bpy.data.objects.new(name="Grid", object_data=grid_mesh)
grid_object.data.materials.append(grid_material)

bpy.context.scene.objects.link(grid_object)

