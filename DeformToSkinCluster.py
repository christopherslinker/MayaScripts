import maya.cmds as cmds

# Select Geo and then Deformer
selection = cmds.ls(selection=True)

targetGeo = selection[0]

deformerSelection = selection[1]

# Variable for Vertex Offset
vertexOffset = []

# Variable for mesh Skin Cluster
geoSkinCluster = cmds.ls(cmds.listHistory(targetGeo), type='skinCluster')[0]

# Get the influence objects (joints) associated with the skin cluster
influences = cmds.skinCluster(geoSkinCluster, q=True, inf=True)

# Variable for Vertex Count in place
vertexCount = cmds.polyEvaluate(targetGeo, vertex=True)
# Variable for Vertex Count after moved
vertexCountMoved = cmds.polyEvaluate(targetGeo, vertex=True)

# Variable for Vertex in position
vertexPosition = []
# Variable for Vertex after moved
vertexPositionMoved = []

# Loop through each vertex and get their position
for i in range(vertexCount):
    vertexName = f"{targetGeo}.vtx[{i}]"
    position = cmds.pointPosition(vertexName, world=True)
    vertexPosition.append(position)

print(vertexPosition)

# Move Deformer 1 unit
cmds.move(0, 0, 1, deformerSelection)

# Loop through each vertex after moved to get position
for i in range(vertexCountMoved):
    vertexName = f"{targetGeo}.vtx[{i}]"
    position = cmds.pointPosition(vertexName, world=True)
    vertexPositionMoved.append(position)

print(vertexPositionMoved)

# Need to figure out how to convert the point position lists into integers to subtract

cmds.move(0, 0, 0, deformerSelection)

# Calculate the Vertex Offset and assign it to vertexOffset Variable
for original, moved in zip(vertexPosition, vertexPositionMoved):
    offset = [m - o for o, m in zip(original, moved)]
    vertexOffset.append(offset)

print(vertexOffset)

# Assign the vertex offsets to the skin cluster weights
for i, offset in enumerate(vertexOffset):
    vertexName = f"{targetGeo}.vtx[{i}]"
    # Iterate over each influence and assign the offset value as a weight change
    for j, influence in enumerate(influences):
        # Adjust the weight for each influence by the calculated offset
        weight = cmds.skinPercent(geoSkinCluster, vertexName, transform=influence, q=True)
        newWeight = weight + sum(offset)  # Simplistic adjustment, may need a more complex calculation
        cmds.skinPercent(geoSkinCluster, vertexName, transformValue=[(influence, newWeight)])

print("Assigned vertex offsets to skin cluster weights.")