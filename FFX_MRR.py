import time
import FFX_Xbox
import FFX_Screen
import FFX_Battle
import FFX_menu
import FFX_Logs
import FFX_memory
import FFX_targetPathing

FFXC = FFX_Xbox.controllerHandle()
#FFXC = FFX_Xbox.FFXC

def arrival():
    FFX_memory.clickToControl()
    wakkaLateMenu = FFX_menu.mrrGrid1()
    FFX_memory.closeMenu()
    FFX_memory.fullPartyFormat('mrr1')
    FFX_memory.closeMenu()
    claskoSkip = True
    
    checkpoint = 0
    while FFX_memory.getMap() != 92:
        if FFX_memory.userControl():
            if checkpoint == 3:
                FFXC.set_movement(-1, 0)
                FFX_memory.waitFrames(30 * 0.7)
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 0.4)
                FFXC.set_movement(1, -1)
                FFX_memory.waitFrames(30 * 0.035)
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 2.3)
                if FFX_memory.userControl() == False:
                    FFX_Battle.fleeAll()
                    FFX_Battle.wrapUp()
                    FFXC.set_movement(-1, 0)
                    FFX_memory.waitFrames(30 * 0.7)
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(30 * 0.4)
                    FFXC.set_movement(1, -1)
                    FFX_memory.waitFrames(30 * 0.035)
                    FFXC.set_neutral()
                    FFX_memory.waitFrames(30 * 0.3)
                print("Attempting skip.")
                FFX_Xbox.menuB()
                
                #Now to wait for the skip to happen, or 60 second maximum limit
                startTime = time.time()
                timeLimit = 60 #Max number of seconds that we will wait for the skip to occur.
                maxTime = startTime + timeLimit
                cam = FFX_memory.getCamera()
                while cam[0] < 0.77:
                    cam = FFX_memory.getCamera()
                    currentTime = time.time()
                    if currentTime > maxTime:
                        print("Skip failed for some reason. Moving on without skip.")
                        claskoSkip = False
                        break
                FFX_memory.clickToControl()
                FFXC.set_neutral()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mrrStart(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_Screen.BattleScreen():
                FFX_Battle.fleeAll()
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
    FFXC.set_neutral()
    print("Done with perlim MRR area, now for the real deal.")
    return [wakkaLateMenu,claskoSkip]

def mainPath(wakkaLateMenu):
    FFX_memory.awaitControl()
    #Yuna complete, Kimahri complete, Valefor overdrive, Battle counter, Yuna grid complete, MRR phase
    status = [0, 0, 0, 1, 0, 0]
    print("Resetting checkpoint.")
    lastGilValue = 0
    checkpoint = 0
    while FFX_memory.getMap() != 119:
        if status[0] == 1 and status[1] == 1 and status[2] == 0:
            status[2] = 2 #No need to do Valefor's overdrive and recharge.
        if status[0] == 1 and status[1] == 1 and status[2] == 2:
            status[5] = 3 #All pieces are complete. Move phase to final phase.
        if FFX_memory.userControl():
            if checkpoint == 1:
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 4:
                print("Up the first lift")
                FFX_Xbox.SkipDialog(1)
                checkpoint += 1
            elif checkpoint == 45:
                if status[0] == 0 or status[1] == 0 or status[2] != 2:
                    if FFX_targetPathing.setMovement(FFX_targetPathing.mrrMain(99)) == True:
                        checkpoint -= 1
                else:
                    if FFX_targetPathing.setMovement(FFX_targetPathing.mrrMain(45)) == True:
                        checkpoint += 1
                
            elif checkpoint == 46:
                print("Up the second lift.")
                FFXC.set_neutral()
                FFX_Xbox.SkipDialog(1)
                checkpoint += 1
                print("Lift checkpoint: ", checkpoint)
            elif checkpoint == 48: #X-potion for safety
                FFX_memory.clickToEventTemple(7)
                print("Got X-potion")
                checkpoint += 1
            elif checkpoint >= 53 and checkpoint <= 56: #400 gil guy
                if FFX_memory.getGilvalue() != lastGilValue: #check if we got the 400 from the guy
                    if FFX_memory.getGilvalue() == lastGilValue + 400:
                        print("We've procured the 400 gil from the guy.")
                        checkpoint = 57 #now to the actual lift
                    else:
                        lastGilValue = FFX_memory.getGilvalue()
                elif FFX_targetPathing.setMovement(FFX_targetPathing.mrrMain(checkpoint)) == True: #Otherwise pathing
                    if checkpoint == 57:
                        checkpoint = 52
                    else:
                        checkpoint += 1
                    print("Checkpoint reached: ", checkpoint)
                else:
                    FFX_Xbox.tapB()
            elif checkpoint == 58:
                FFX_Xbox.SkipDialog(1)
                print("Up the third lift")
                checkpoint += 1
            elif checkpoint == 66:
                FFX_Xbox.SkipDialog(1)
                print("Up the final lift")
                checkpoint += 1
            elif checkpoint < 71 and FFX_memory.getMap() == 79:
                checkpoint = 71 #Into Battle Site zone (upper, cannon area)
            elif FFX_targetPathing.setMovement(FFX_targetPathing.mrrMain(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.battleActive():
                print("Starting battle MRR")
                status = FFX_Battle.MRRbattle(status)
                print("Status update: ", status)
                    #print("Yuna Complete state: ", status[0])
                    #print("Kimahri Complete state: ", status[1])
                status[3] += 1
                
                if FFX_memory.getYunaSlvl() >= 8 and status[4] == 0:
                    print("Yuna has enough levels now. Going to do her grid.")
                    FFX_menu.mrrGridYuna()
                    print("Yuna's gridding is complete for now.")
                    status[4] = 1
                if wakkaLateMenu == True and FFX_memory.getSLVLWakka() >= 3:
                    wakkaLateMenu = FFX_menu.mrrGrid2(wakkaLateMenu)
            elif FFX_memory.menuOpen():
                FFX_Xbox.tapB()
            elif FFX_memory.diagSkipPossible():
                FFX_memory.clickToControl3()
            
            #Map changes
            elif checkpoint < 47 and FFX_memory.getMap() == 128:
                checkpoint = 47
        
        if FFX_memory.gameOver():
            return
        
    print("End of MRR section. Status:")
    print(status)

def battleSite():
    FFX_memory.awaitControl()
    FFX_menu.battleSiteGrid()
    
    checkpoint = 0
    while checkpoint < 99:
        if FFX_memory.userControl():
            if checkpoint == 5:
                print("O'aka menu section")
                while FFX_memory.userControl():
                    FFX_targetPathing.setMovement([-45, 3430])
                    FFX_Xbox.tapB()
                FFXC.set_neutral()
                FFX_menu.battleSiteOaka1()
                FFX_menu.battleSiteOaka2()
                checkpoint += 1
            elif checkpoint == 8:
                FFX_Xbox.touchSaveSphere()
                checkpoint += 1
            elif checkpoint == 12:
                FFXC.set_movement(0, 1)
                FFX_memory.waitFrames(30 * 1)
                checkpoint += 1
            elif checkpoint == 14:
                FFXC.set_movement(1, 0)
                FFX_memory.clickToEvent()
                FFX_Xbox.tapB() #Tell me when you're ready.
                FFXC.set_neutral()
                FFX_memory.waitFrames(30 * 2)
                FFX_Xbox.menuDown()
                FFX_Xbox.tapB()
                checkpoint = 100
            elif FFX_targetPathing.setMovement(FFX_targetPathing.battleSite(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            if FFX_memory.diagSkipPossible():
                FFX_Xbox.tapB()

def guiAndAftermath():
    status = FFX_Battle.battleGui()
    #FFX_Xbox.SkipDialog(10)
    #while not FFX_memory.cutsceneSkipPossible():
    #    FFX_Xbox.tapB()
    #FFX_Xbox.skipSceneSpec()
    #FFX_memory.clickToControl()
    
    checkpoint = 0
    while FFX_memory.getMap() != 93:
        if FFX_memory.userControl():
            if checkpoint == 3:
                FFX_memory.clickToEventTemple(0)
                checkpoint += 1
            elif checkpoint == 7:
                FFXC.set_movement(-1, 0)
                FFX_memory.awaitEvent()
                FFXC.set_neutral()
                checkpoint += 1
            elif checkpoint == 15:
                FFXC.set_movement(0, 1)
                FFX_memory.awaitEvent()
                checkpoint += 1
            elif FFX_targetPathing.setMovement(FFX_targetPathing.battleSiteAftermath(checkpoint)) == True:
                checkpoint += 1
                print("Checkpoint reached: ", checkpoint)
        else:
            FFXC.set_neutral()
            FFX_memory.clickToControl3()
