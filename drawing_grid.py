# filename = "/home/dacoda/projects/benjamin-blender/drawing_grid.py"; exec(compile(open(filename).read(), filename, 'exec'))

import bmesh

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

def square_point_indices_from_coordinate(x, y):
    return [point_index_from_coordinate( x     , y     ),
            point_index_from_coordinate( x     , y + 1 ),
            point_index_from_coordinate( x + 1 , y + 1 ),
            point_index_from_coordinate( x + 1 , y     )]

def polygon_index_from_coordinate(x, y):
    return y * (grid_size) + x
    
for y in range(grid_size + 1):
    v1 = grid_bmesh.verts[point_index_from_coordinate(0, y)]
    v2 = grid_bmesh.verts[point_index_from_coordinate(grid_size, y)]
    grid_bmesh.edges.new((v1, v2))

for x in range(grid_size + 1):
    v1 = grid_bmesh.verts[point_index_from_coordinate(x, 0)]
    v2 = grid_bmesh.verts[point_index_from_coordinate(x, grid_size)]
    grid_bmesh.edges.new((v1, v2))

for x in range(grid_size):
    for y in range(grid_size):
        square_point_indices = square_point_indices_from_coordinate(x, y)
        face = tuple(grid_bmesh.verts[index] for index in square_point_indices)
        grid_bmesh.faces.new(face)

grid_bmesh.to_mesh(grid_mesh)

grid_object = bpy.data.objects.new(name="Grid", object_data=grid_mesh)
grid_object.data.materials.append(grid_material)

bpy.context.scene.objects.link(grid_object)

color_material = bpy.data.materials.new(name="Color Material")
material_slots = grid_object.material_slots
grid_object.data.materials.append(color_material)
material_slots[0].material = None
grid_object.data.materials.append(color_material)
color_material.diffuse_color = (1, 0, 0)


for i in [polygon_index_from_coordinate(x, y) for x, y in [(0, 0), (0, 1), (1, 1), (1, 0)]]:
    grid_object.data.polygons[i].material_index = 1

for edge in grid_object.data.edges:
    edge.use_freestyle_mark = True

grid_object.data.show_freestyle_edge_marks = True
# bpy.context.scene.render.layers["RenderLayer"].use_freestyle = True
bpy.context.scene.render.use_freestyle = True
bpy.context.scene.render.layers["RenderLayer"].freestyle_settings.linesets["LineSet"].select_edge_mark = True


