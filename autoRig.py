#autoRigScript v0.2
#author: Dmitry Sobolev
#2019

import maya.cmds as mc
#create idem dict
itemDict = {
			'base' : ['root', 'pelvis', 'torso', 'neck', 'head', 'headEnd'],
			'arm_l' : ['sholder_l', 'elbow_l', 'hand_l', 'hand_middle_l', 'hand_end_l'],
			'leg_l' : ['hip_l', 'knee_l', 'foot_l', 'foot_middle_l', 'foot_end_l'],
			'face' : ['eye_l']
			}

#item def position list			
itemDefPosList = {
				'root': [0, 0, 0],
				'pelvis': [0.0, 7.0, -4.225543935457168],
				'torso': [0.0, 10.0, -4.225543935457168], 
				'neck': [0.0, 13.0, -4.225543935457168], 
				'head': [0.0, 16.0, -4.225543935457168],
				'headEnd': [0.0, 19.0, -4.225543935457168],  

				'sholder_l': [2.5, 12.585183287261554, 0.0], 
				'elbow_l': [5.0, 12.585183287261554, 0.0], 
				'hand_l': [7.5, 12.585, 0.0],
				'hand_middle_l': [10, 12.585, 0.0],
				'hand_end_l': [12.5, 12.585, 0.0],

				'hip_l' : [2.8, 7.0, 0.0],
				'knee_l' : [2.8, 4.0, 0.0], 
				'foot_l' : [2.8, 1.0, 0.0], 
				'foot_middle_l' : [2.8, 1.0, 1.5], 
				'foot_end_l' : [2.8, 1.0, 3], 
				 
				'eye_l': [0.7607344428135328, 14.389011991402285, 2.759420496641652], 				
				} 

#all dict values to list
def allVal(dictName):
	dictVal = []
	for key in dictName:
	    for value in dictName[key]:
	        dictVal.append(value)
	return dictVal
dictVal = allVal(itemDict)

#create locators and set default position
def createLoc():
	for i in itemDict.keys():
	    print('creating_' + i)
	    for i in itemDict[i]:
	        mc.spaceLocator(n='locator_' + i)
	        mc.move(itemDefPosList[i][0],
	        		itemDefPosList[i][1],
	        		itemDefPosList[i][2])
	        print('__creating__' + i)
createLoc()

#update locator position or store user ...
def curLocPosition():
	locPosition = {}
	for key in itemDict:
	     for value in itemDict[key]:
	    	    print value + ' _ position updated'
	    	    locX = mc.getAttr('locator_' + value + '.translateX')
	    	    locY = mc.getAttr('locator_' + value + '.translateY')
	    	    locZ = mc.getAttr('locator_' + value + '.translateZ')
	    	    locPosition.update({ value : [locX, locY, locZ]})
	return locPosition
locPosition = curLocPosition()

#restore user locator position or #select and set position
def setPosition(dictName):
	for i in range(len(dictName.keys())):
	    mc.select('locator_' + dictName.keys()[i])
	    mc.move(dictName[dictName.keys()[i]][0],
	            dictName[dictName.keys()[i]][1],
	            dictName[dictName.keys()[i]][2])
setPosition(locPosition)

#Artem loc position backup
{'sholder_l': [1.546225498647889, 11.035299722564375, 0.0],
'head': [0.0, 12.550926569250453, 0.024604614692267823], 
'hip_l': [0.7541335650446879, 6.896479361450975, 0.0], 
'neck': [0.0, 11.664874801000186, 0.002352528042269597], 
'hand_end_l': [8.476263822420785, 11.035116435302822, 0.0], 
'root': [0.0, 0.0, 0.0], 
'foot_l': [0.7541335650446879, 0.8565897476638269, 0.0], 
'foot_middle_l': [0.7541335650446879, 0.37420980798760806, 1.4608881129992255], 
'headEnd': [0.0, 16.329749602000366, -0.10890790520771576], 
'hand_middle_l': [7.272808031889169, 11.035116435302822, 0.0], 
'knee_l': [0.7541335650446879, 3.8102293755919314, 0.0], 
'elbow_l': [3.807781873309861, 11.035299722564375, 0.0], 
'foot_end_l': [0.7541335650446879, 0.37420980798760806, 2.700142199660729], 
'eye_l': [0.4631437361240387, 14.419005759034087, 0.9884660243988037], 
'pelvis': [0.0, 7.823327206049893, 0.002352528042268709], 
'hand_l': [6.218365513808102, 11.035116435302822, 0.0], 
'torso': [0.0, 9.554958267000062, 0.002352528042268709]}

#mirror_locators_function!
mirrorList = [
			  
			  ]

#!!!Create Joints
mc.select(clear=True)
for i in allVal(itemDict):
	mc.joint(n='joint_' + i, p=locPosition[i])
	mc.select(clear=True)

#parent joints interactively and mirror
def parentJoints():
	for key in itemDict:
		for value in range(len(itemDict[key])):
		    try:
		        mc.parent ('joint_'+itemDict[key][value+1], 'joint_'+itemDict[key][value] )
		    except IndexError:
		        print 'All done ;)'
    #custom parent
	mc.parent('joint_hip_l', 'joint_pelvis')
	mc.parent('joint_sholder_l', 'joint_torso')
	mc.parent('joint_eye_l', 'joint_head')
	#mirror & nameUpdate
	cmds.mirrorJoint('joint_sholder_l', searchReplace=('_l', '_r'))
	cmds.mirrorJoint('joint_hip_l', searchReplace=('_l', '_r'))
	cmds.mirrorJoint('joint_eye_l', searchReplace=('_l', '_r'))
	#custom IK
	mc.ikHandle( sj='joint_sholder_l', ee='joint_hand_l')
	mc.ikHandle( sj='joint_sholder_r', ee='joint_hand_r')
	mc.ikHandle( sj='joint_hip_l', ee='joint_foot_l')
	mc.ikHandle( sj='joint_hip_r', ee='joint_foot_r')
	#FixIKRotate
	mc.rotate(0, -90, 0, 'joint_foot_r')
	mc.rotate(0, -90, 0, 'joint_foot_l')
parentJoints()

#createJointList
jointsList = []
for i in mc.ls():
    if mc.objectType(i) == 'joint':
        jointsList.append(i)

#createJointDict
jointsDict = {}
for i in mc.ls():
    if mc.objectType(i) == 'joint':
        jointsDict.update({i : mc.xform(i ,q=1,ws=1,rp=1)})

def genControlls():
	#NEED TO FIX = No controlls for eyes currently
	#createControlls base
	for key in itemDict:
	    for value in itemDict[key]:
	        mc.circle(n= 'controll_' + value)
	        mc.move(mc.xform('joint_' + value,q=1,ws=1,rp=1)[0], 
	                mc.xform('joint_' + value,q=1,ws=1,rp=1)[1],
	                mc.xform('joint_' + value,q=1,ws=1,rp=1)[2])
        	mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
	        if key == 'arm_l':
	            mc.rotate(0, 90, 0)
	            mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
	        if key == 'leg_l':
	            mc.rotate(90, 0, 0)
	            mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
	        if key == 'base':
	            mc.rotate(90, 0, 0)
	            mc.scale(2.5, 2.5, 2.5)
	            mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
    

	#createControlls RIGHT
	mirrorList = ['arm_l', 'leg_l', 'face']
	for key in mirrorList:
		for value in itemDict[key]:
		    mc.circle(n= 'controll_' + value[:-1] + 'r')
		    mc.move(mc.xform('joint_' + value[:-1] + 'r',q=1,ws=1,rp=1)[0], 
		            mc.xform('joint_' + value[:-1]  + 'r',q=1,ws=1,rp=1)[1],
		            mc.xform('joint_' + value[:-1]  + 'r',q=1,ws=1,rp=1)[2])
		    mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
		    if key == 'arm_l':
		        mc.rotate(0, 90, 0)
		        mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
		    if key == 'leg_l':
		        mc.rotate(90, 0, 0)
		        mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
		    if key == 'base':
		        mc.rotate(90, 0, 0)
		        mc.scale(2.5, 2.5, 2.5)
		        mc.makeIdentity( apply=True, t=1, r=1, s=1, n=2 )
genControlls()

#parent Controlls
#parent joints interactively and mirror

#parent base
def parentControlls():
	for key in itemDict:
		for value in range(len(itemDict[key])):
		    if 'controll_'+itemDict[key][value] in mc.ls(): #checking if object exist
		        try:                    
		            mc.parent ('controll_'+itemDict[key][value+1], 'controll_'+itemDict[key][value] )
		        except IndexError: #excepting i+1 & deleted controlls
		            print 'IndexError catched'
		        except ValueError:
		            #print('controll_'+itemDict[key][value])
		            mc.parent ('controll_'+itemDict[key][value+2], 'controll_'+itemDict[key][value] ) #jumping over non existiong controll

	#parent mirrors
	for key in itemDict:
		for value in range(len(itemDict[key])):
		    if 'controll_'+itemDict[key][value][:-1]+'r' in mc.ls(): #checking if object exist
		        try:                    
		            mc.parent ('controll_'+itemDict[key][value+1][:-1]+'r', 'controll_'+itemDict[key][value][:-1]+'r' )
		        except IndexError: #excepting i+1 & deleted controlls
		            print 'IndexError catched'
		        except ValueError:
		            #print('controll_'+itemDict[key][value])
		            mc.parent ('controll_'+itemDict[key][value+2][:-1]+'r', 'controll_'+itemDict[key][value][:-1]+'r' ) 

	#custom parent
	mc.parent('controll_eye_l', 'controll_headEnd')
	mc.parent('controll_eye_r', 'controll_headEnd')
	mc.parent('controll_hip_l', 'controll_pelvis')
	mc.parent('controll_hip_r', 'controll_pelvis')
	mc.parent('controll_sholder_l', 'controll_neck')
	mc.parent('controll_sholder_r', 'controll_neck')
parentControlls()

def clearControlls():
	for i in mc.ls():
	    if i[-3:] == 'End' or i[-5:][:3] == 'end' and mc.objectType(i) == 'transform':
	        mc.delete(i)
clearControlls()




#parentContraints // http://help.autodesk.com/view/MAYAUL/2018/ENU/?guid=__CommandsPython_index_html
mc.parentConstraint('controll_sholder_l', 'joint_sholder_l')
#oritneConstraints
mc.orientConstraint( [target ...] [object] )
#IK handle
mc.ikHandle( sj='joint_sholder_l', ee='joint_hand_l')
mc.ikHandle( sj='joint_sholder_l1', ee='joint_hand_l1')