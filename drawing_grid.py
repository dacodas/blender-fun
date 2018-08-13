# filename = "/home/dacoda/projects/benjamin-blender/drawing_grid.py"; exec(compile(open(filename).read(), filename, 'exec'))

grid_material = bpy.data.materials.new(name="Grid Material")
grid_material.type = 'WIRE'

grid_mesh = bpy.data.meshes.new(name="Grid Mesh")
grid_bmesh = bmesh.new()

for y_coordinate in range(20):
    v1 = grid_bmesh.verts.new((-5.0, y_coordinate, 0.0))
    v2 = grid_bmesh.verts.new((+5.0, y_coordinate, 0.0))
    grid_bmesh.edges.new((v1, v2))

grid_bmesh.to_mesh(grid_mesh)

grid_object = bpy.data.objects.new(name="Grid", object_data=grid_mesh)
grid_object.data.materials.append(grid_material)

bpy.context.scene.objects.link(grid_object)

