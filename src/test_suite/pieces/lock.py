# MAYA - MVN plug-in 2012

#import maya.cmds as cmd

#WERKING
#1- get selected char name
#2- get hierarchy of selected character(all of it's joints according to interface
#3- assign each joint to a 3d array containing current xyz locations values.
#4- values will be changed accordingly upon data input
lumatrix = None

#select skeleton according to specified name. 
name = 'Character1'

#initialize locators
def initLoc():
    head = name+'_Head'
    neck = name+'_Neck'

    lesh = name+'_LeftShoulder'
    leua = name+'_LeftArm'       #LeftUpperArm
    lefa = name+'_LeftForeArm'  
    leha = name+'_LeftHand'

    rish = name+'_RightShoulder'
    riua = name+'_RightArm'      #RightUpperArm
    rifa = name+'_RightForeArm'  
    riha = name+'_RightHand'

    top2 = name+'_Spine2' #T8
    top1 = name+'_Spine1' #T12

    low1 = name+'_Spine'  #L5
                          #L3 omitted

    pelvis = name+'_Hips'

    leul = name+'_LeftUpLeg'
    lell = name+'_LeftLowerLeg'
    lefo = name+'_LeftFoot'
    leto = name+'_LeftToe'

    riul = name+'_RightUpLeg'
    rill = name+'_RightLowerLeg'
    rifo = name+'_RightFoot'
    rito = name+'_RightToe'

    ref = name+"_Reference"
    print('all locators initialized')

    #cmd.lockNode(ref) #reference point can't be deleted
    lumatrix = 5 # cmd.getAttr(leul+'.matrix')
    return lumatrix
    

initLoc()

lumatrix

#store selection | get xyz values
#lumatrix = None
#3d array
    



