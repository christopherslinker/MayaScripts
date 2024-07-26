import maya.cmds as cmds

#Select Top joint first, Mid Joint, Bottom Joint, IK Top control, IK bottom control
sel = cmds.ls(selection=True)

#Separate joint selection into their own varaibles
topJoint = sel[0]
midJoint = sel[1]
bottomJoint = sel[2]
#Separate IK ctrl for custom variables
ikTopControl = sel[3]
ikBottomControl = sel[4]

#Get Top and Bottom joints translation to to match to a locator
topJointPos = cmds.xform(topJoint, query=True, worldSpace=True, translation=True)
bottomJointPos  = cmds.xform(bottomJoint, query=True, worldSpace=True, translation=True)

#Create Top and Bottom Locators
topLocator = cmds.spaceLocator(name="NAME_Top_Loc")[0]
bottomLocator = cmds.spaceLocator(name="NAME_Bottom_Loc")[0]

#Translate Locators to Top and Bottom joint accordingly
cmds.xform(topLocator, worldSpace=True, translation = topJointPos)
cmds.xform(bottomLocator, worldSpace=True, translation = bottomJointPos)

#Constrain the Locators to the controls.
cmds.parentConstraint(ikTopControl, topLocator, maintainOffset=True)
cmds.parentConstraint(ikBottomControl, bottomLocator, maintainOffset=True)

#Create Custom attributes for the IK Control
cmds.addAttr(ikBottomControl, ln='Stretch', at='double', min=0, max=1, dv=1, keyable=True)
cmds.addAttr(ikBottomControl, ln='Max_Stretch', at='double', min=1, max=10, dv=5, keyable=True)

#Creating and setting all the attributes that will be used in the stretch
distanceBetween = cmds.createNode('distanceBetween', name='NAME_IK_Distance')
stretchSwitchMD = cmds.createNode('multiplyDivide', name='NAME_Stretch_Switch_MD')
stretchScalarMD = cmds.createNode('multiplyDivide', name='NAME_Stretch_Scalar_MD')
cmds.setAttr(stretchScalarMD+'.operation',2)
jointLengthMD = cmds.createNode('multiplyDivide', name='NAME_Joint_Length_MD')
upperLengthPMA = cmds.createNode('plusMinusAverage', name='NAME_Upper_Length_PMA')
lowerLengthPMA = cmds.createNode('plusMinusAverage', name='NAME_Lower_Length_PMA')
denominatorLengthPMA = cmds.createNode('plusMinusAverage', name='NAME_Length_Denominator_PMA')
stretchClamp = cmds.createNode('clamp', name='NAME_IK_Stretch_Clamp')
cmds.setAttr(stretchClamp+'.minR',1)

#Connect the locators into the Distance Between node
cmds.connectAttr(topLocator + '.worldMatrix[0]', distanceBetween + '.inMatrix1')
cmds.connectAttr(bottomLocator + '.worldMatrix[0]', distanceBetween + '.inMatrix2')

#Connect the Distance Between and the Stretch Attr on our IK control the our Stretch Switch MD.
cmds.connectAttr(distanceBetween+'.distance', stretchSwitchMD+'.input1X')
cmds.connectAttr(ikBottomControl+'.Stretch', stretchSwitchMD+'.input2X')

#Connect the Mid Joint and Bottom Joint to the Top and Bottom PMA, Break connection to keep value.
cmds.connectAttr(midJoint+'.translateX', upperLengthPMA+'.input1D[0]')
cmds.connectAttr(bottomJoint+'.translateX', lowerLengthPMA+'.input1D[0]')
cmds.disconnectAttr(midJoint+'.translateX', upperLengthPMA+'.input1D[0]')
cmds.disconnectAttr(bottomJoint+'.translateX', lowerLengthPMA+'.input1D[0]')

#Upper and Lower PMA outputs connected into the denominaotr PMA
cmds.connectAttr(upperLengthPMA+'.output1D', denominatorLengthPMA+'.input1D[0]')
cmds.connectAttr(lowerLengthPMA+'.output1D', denominatorLengthPMA+'.input1D[1]')

#Connect the Switch output value and Denominator output Value into the Scalar 1x and 2x to be divided
# for a scale percent
cmds.connectAttr(stretchSwitchMD+'.outputX', stretchScalarMD+'.input1X')
cmds.connectAttr(denominatorLengthPMA+'.output1D', stretchScalarMD+'.input2X')

#Connect the Scalar and IK Controls Max Stretch Attribute to the stretch Clamp
cmds.connectAttr(stretchScalarMD+'.outputX', stretchClamp+'.inputR')
cmds.connectAttr(ikBottomControl+'.Max_Stretch', stretchClamp+'.maxR')

cmds.connectAttr(stretchClamp+'.outputR', jointLengthMD+'.input2X')
cmds.connectAttr(stretchClamp+'.outputR', jointLengthMD+'.input2Y')
cmds.connectAttr(upperLengthPMA+'.output1D', jointLengthMD+'.input1X')
cmds.connectAttr(lowerLengthPMA+'.output1D', jointLengthMD+'.input1Y')

cmds.connectAttr(jointLengthMD+'.outputX', midJoint+'.translateX')
cmds.connectAttr(jointLengthMD+'.outputY', bottomJoint+'.translateX')