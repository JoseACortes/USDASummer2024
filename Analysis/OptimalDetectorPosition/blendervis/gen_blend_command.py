# %%
import pandas as pd

# %%
# when finished
# trials = pd.read_csv('../../../Simulations/varied_detector_positions/trials.csv')

# before finished
trials = pd.read_csv('../../../Simulations/varied_detector_positions/input/input_generation/filenames.csv')

# %%
def bash_render_script(name):
    render_script = f'''blender -b empty.blend -P pyscripts/{name}.py -f 5 -F PNG
    chmod u+w /tmp/0005.png
    cp /tmp/0005.png ims/{name}.png'''
    return render_script

# %%
def generate_python_script(name):
    script = f"""import bpy
import numpy as np
import mathutils
import math
import json

with open('/home/jac2462@uta.edu/Documents/USDASummer2024/Simulations/varied_detector_positions/input/input_generation/world/surfaces/{name}surface.json') as f:
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
# deselect all objects
bpy.ops.object.select_all(action='DESELECT')
# make detectors red

highlight_mat = bpy.data.materials.new('detectors')
highlight_mat.diffuse_color = (1, 0, 0, 1)

obj_det1 = bpy.data.objects["surface2000"]
obj_det1.data.materials.append(highlight_mat)
obj_det1.active_material_index = len(obj_det1.data.materials) - 1 

obj_det2 = bpy.data.objects["surface3000"]
obj_det2.data.materials.append(highlight_mat)
obj_det2.active_material_index = len(obj_det2.data.materials) - 1 

obj_det3 = bpy.data.objects["surface4000"]
obj_det3.data.materials.append(highlight_mat)
obj_det3.active_material_index = len(obj_det3.data.materials) - 1 

# move camera
obj_camera = bpy.data.objects["Camera"]
obj_camera.location = (1.5, .5, 0)
obj_camera.rotation_euler = (math.radians(90), math.radians(0), math.radians(120))

# obj_light = bpy.data.objects["Light"]
# obj_light.location = (2.3, -1.7, -3.4)
    """
    return script

# %%
trials.head()

# %%
cmds = []
for name in trials['name']:
    with open(f'pyscripts/{name}.py', 'w') as f:
        f.write(generate_python_script(name))
        f.close()
    with open(f'commands/{name}.sh', 'w') as f:
        f.write(bash_render_script(name))
        f.close()
    cmds.append(f'bash commands/{name}.sh')

with open('render_all.sh', 'w') as f:
    f.write('\n'.join(cmds))
    f.close()

