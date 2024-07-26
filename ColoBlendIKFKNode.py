import maya.cmds as cmds

# Select the objects in the correct order
sel = cmds.ls(sl=True)

# Assign selected objects to variables
selFK = sel[0]
selIK = sel[1]
selRK = sel[2]

# Create blendColors nodes for rotation and translation
RotateBC = cmds.shadingNode('blendColors', asUtility=True, name='Rotate_BlendColors')
TranslateBC = cmds.shadingNode('blendColors', asUtility=True, name='Translate_BlendColors')

# Connect the rotate attribute of selFK to the color1 of RotateBC
cmds.connectAttr(selFK + '.rotate', RotateBC + '.color1')

# Connect the translate attribute of selFK to the color1 of TranslateBC
cmds.connectAttr(selFK + '.translate', TranslateBC + '.color1')

# Connect the rotate attribute of selIK to the color2 of RotateBC
cmds.connectAttr(selIK + '.rotate', RotateBC + '.color2')

# Connect the translate attribute of selIK to the color2 of TranslateBC
cmds.connectAttr(selIK + '.translate', TranslateBC + '.color2')

# Connect the output of RotateBC to the rotate attribute of selRK
cmds.connectAttr(RotateBC + '.output', selRK + '.rotate')

# Connect the output of TranslateBC to the translate attribute of selRK
cmds.connectAttr(TranslateBC + '.output', selRK + '.translate')

#------------ ADD IKFK ATTRIBUTE TO CONTROL ---------------
# DO NOT POST THIS WITH THE REST OF THE SCRIPT.

import maya.cmds as cmds

# Get the current selection
sel = cmds.ls(sl=True)

# Check if there is any selection
if not sel:
    print("No objects selected.")
else:
    # Iterate over each selected object
    for ctrl in sel:
        print("Adding attribute to {}".format(ctrl))
        cmds.addAttr(ctrl, ln='IKFK_Switch', at='double', min=0, max=1, dv=1)

        # Check if the attribute has been added
        if cmds.attributeQuery('IKFK_Switch', node=ctrl, exists=True):
            print("Attribute 'IKFK_Switch' added to {}".format(ctrl))
        else:
            print("Failed to add attribute 'IKFK_Switch' to {}".format(ctrl))

print("Attribute addition process completed.")