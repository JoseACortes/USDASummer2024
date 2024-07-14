import bpy
import numpy as np
import mathutils
import math
import json

with open('/home/jac2462@uta.edu/Documents/USDASummer2024/Simulations/varied_detector_positions/input/input_generation/world/surfaces/detector_dfs_2_dfg_30surface.json') as f:
    surfaces = json.load(f)
    f.close()

baseangle = mathutils.Vector((0, 0, 1))

for surface in surfaces:
    shape = surface["shape"]
    name = surface['surface_id']
    if shape == "sphere":
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=np.array(surface["params"]["pos"])/100,
            radius=np.array(surface["params"]["r"])/100,
            )
        bpy.context.active_object.name = "surface"+ str(name)
    elif shape == "box":
        size = [surface["params"]["l"], surface["params"]["w"], surface["params"]["h"]]
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            location=np.array(surface["params"]["pos"])/100, 
            scale=np.array(size)/100,
                )
        bpy.context.active_object.name = "surface"+ str(name)
    elif shape == "cylinder":
        v = mathutils.Vector(surface["params"]["dir"]) # convert to quaternion
        v_ = v.rotation_difference(baseangle) # convert to angle
        bpy.ops.mesh.primitive_cylinder_add(
            location=np.array(surface["params"]["pos"])/100, 
            depth=np.array(surface["params"]["height"])/100, 
            rotation = v_.to_euler(),
            radius = np.array(surface["params"]["r"])/100,
                )
        bpy.context.active_object.name = "surface"+ str(name)

# make detectors red

highlight_mat = bpy.data.materials.new('detectors')
highlight_mat.diffuse_color = (1, 0, 0, 1)

obj_det1 = bpy.data.objects["surface2"]
obj_det1.data.materials.append(highlight_mat)
obj_det1.active_material_index = len(obj_det1.data.materials) - 1 

obj_det2 = bpy.data.objects["surface3"]
obj_det2.data.materials.append(highlight_mat)
obj_det2.active_material_index = len(obj_det2.data.materials) - 1 

obj_det3 = bpy.data.objects["surface4"]
obj_det3.data.materials.append(highlight_mat)
obj_det3.active_material_index = len(obj_det3.data.materials) - 1 

# move camera
obj_camera = bpy.data.objects["Camera"]
obj_camera.location = (3, -1.7, 0)
obj_camera.rotation_euler = (math.radians(0), math.radians(90), math.radians(0))

# obj_light = bpy.data.objects["Light"]
# obj_light.location = (2.3, -1.7, -3.4)
    