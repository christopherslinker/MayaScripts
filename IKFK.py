import maya.cmds as cmds

jointSel = cmds.ls(selection=True)

getChildren = cmds.listRelatives(jointSel, allDescendents=True, fullPath=True)
print(getChildren)
selectionChildren = getChildren[0]
print(selectionChildren)

cmds.duplicate(jointSel)

jointFk = cmds.ls(selection=True)

selObjs = cmds.ls(selection=True)

searchName = "RK"
replaceName = "FK"

jointSel = selObjs[0]
children = cmds.listRelatives(jointSel, allDescendents=True, fullPath=True)
jointChain = children
print(jointChain)

for obj in jointChain:
    if searchName in obj:
        newName = obj.replace(searchName, replaceName)
        cmds.rename(obj, newName)
