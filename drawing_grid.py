# filename = "/home/dacoda/projects/benjamin-blender/drawing_grid.py"; exec(compile(open(filename).read(), filename, 'exec'))

import bmesh

import logging
logging.basicConfig(level=logging.DEBUG)

class Grid():

    def point_index_from_coordinate(self, x, y):
        return y * (self.grid_size + 1) + x

    def square_point_indices_from_coordinate(self, x, y):
        return [self.point_index_from_coordinate( x     , y     ),
                self.point_index_from_coordinate( x     , y + 1 ),
                self.point_index_from_coordinate( x + 1 , y + 1 ),
                self.point_index_from_coordinate( x + 1 , y     )]

    def polygon_index_from_coordinate(self, x, y):
        return y * (self.grid_size) + x

    def __init__(self, grid_size):
        self.grid_size = grid_size

        self.grid_material = bpy.data.materials.new(name="Grid Material")
        self.grid_material.type = 'WIRE'

        self.grid_mesh = bpy.data.meshes.new(name="Grid Mesh")
        self.grid_bmesh = bmesh.new()

        for x in range(grid_size + 1):
            for y in range(grid_size + 1):
                self.grid_bmesh.verts.new((x, y, 0))

        self.grid_bmesh.verts.ensure_lookup_table()

        for y in range(grid_size + 1):
            v1 = self.grid_bmesh.verts[self.point_index_from_coordinate(0, y)]
            v2 = self.grid_bmesh.verts[self.point_index_from_coordinate(self.grid_size, y)]
            self.grid_bmesh.edges.new((v1, v2))

        for x in range(self.grid_size + 1):
            v1 = self.grid_bmesh.verts[self.point_index_from_coordinate(x, 0)]
            v2 = self.grid_bmesh.verts[self.point_index_from_coordinate(x, self.grid_size)]
            self.grid_bmesh.edges.new((v1, v2))

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                square_point_indices = self.square_point_indices_from_coordinate(x, y)
                face = tuple(self.grid_bmesh.verts[index] for index in square_point_indices)
                self.grid_bmesh.faces.new(face)

        self.grid_bmesh.to_mesh(self.grid_mesh)

        self.grid_object = bpy.data.objects.new(name="Grid", object_data=self.grid_mesh)
        self.grid_object.data.materials.append(self.grid_material)

        bpy.context.scene.objects.link(self.grid_object)

        self.color_material = bpy.data.materials.new(name="Color Material")
        self.material_slots = self.grid_object.material_slots
        self.grid_object.data.materials.append(self.color_material)
        self.material_slots[0].material = None
        self.grid_object.data.materials.append(self.color_material)
        self.color_material.diffuse_color = (1, 0, 0)

    def show_gridlines(self):
        """
        Mark all edges in this object as freestyle, and enable
        freestyle lines in the render
        """

        for edge in self.grid_object.data.edges:
            edge.use_freestyle_mark = True

        self.grid_object.data.show_freestyle_edge_marks = True
        # bpy.context.scene.render.layers["RenderLayer"].use_freestyle = True
        bpy.context.scene.render.use_freestyle = True
        bpy.context.scene.render.layers["RenderLayer"].freestyle_settings.linesets["LineSet"].select_edge_mark = True

grid = Grid(10)

for i in [grid.polygon_index_from_coordinate(x, y) for x, y in [(0, 0), (0, 1), (1, 1), (1, 0)]]:
    grid.grid_object.data.polygons[i].material_index = 1




