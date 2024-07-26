import maya.cmds as cmds

#-- CREATING THE ENUM ATTRIBURTE AND SETTING IT'S VALUES" --

# object selection
selObj = cmds.ls(selection=True)

if selObj:
    obj = selObj[0]
    # attribute naming options
    attrName = "Follow"
    enumOptions = ["World", "Transform", "COG", "Clav"]

    enumString = ":".join(enumOptions)

    # adding attribute to object
    if not cmds.attributeQuery(attrName, node=obj, exists=True):
        cmds.addAttr(obj, longName=attrName, attributeType="enum", enumName=enumString)
        cmds.setAttr(f"{obj}.{attrName}", keyable=True)

    else:
        print("no good")

# -- CREATING THE SDK CONNECTIONS --

# Select all objects
selObj = cmds.ls(selection=True)
# Select control last, adjust index as necessary
obj1 = selObj[0]
obj2 = selObj[1]
obj3 = selObj[2]
obj4 = selObj[3]
# Control offset selection last
ctrlOffsetObj = selObj[4]

objConstrain = obj1, obj2, obj3, obj4
print(ctrlOffsetObj, objConstrain)

cmds.parentConstraint(objConstrain, ctrlOffsetObj, maintainOffset=True)