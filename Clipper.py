import pygame

ZOOMS = 15
BGRNDCOLORS = {
               0:[125, 125, 125],
               1:[153, 255, 51],
               2:[0, 0, 0],
               3:[255, 255, 255]
              }
MODETEXT =    {
               0:"CLIPPER",
               1:"ANIMATE",
               2:"N/A"
              }           
BUTTONTEXT =  {
               0:"RENAMECLIP",
               1:"RESETCLIPS",
               2:"BGRNDCOLOR",
               3:"T-LEFT",
               4:"LOCKCLIPS",
               5:"ZOOM IN",
               6:"B-RIGHT",
               7:"UNLCKCLIPS",
               8:"ZOOM OUT",
               9:"NEWCLIP",
               10:"DELCLIP",
               11:"MENU"
              }
TOOLTYPE =    {
               "TLEFT":1,
               "BRIGHT":2
              }
          
class Clipper:

    def __init__(self, mainloop):
        self.theLoop = mainloop
        
        self.currentZoom = 0
        self.currentTool = 0
                          
        self.clips = {}
        self.clipCounter = 0
        self.currentClip = -1
                          
        self.loadBackground()
        self.loadClipCorners()
        
    def loadBackground(self):
        self.bgfillID = 0
        self.bgfill = pygame.Surface([488, 489])
        self.bgfill = self.bgfill.convert()
        self.bgfill.fill(BGRNDCOLORS[self.bgfillID])
        
    def loadClipCorners(self):
        self.tlCorner = [None] * ZOOMS
        for i in range(ZOOMS):
            self.tlCorner[i] = pygame.Surface([i+1, i+1])
            self.tlCorner[i] = self.tlCorner[i].convert()
            self.tlCorner[i].fill((255,0,0))
        self.brCorner = [None] * ZOOMS
        for i in range(ZOOMS):
            self.brCorner[i] = pygame.Surface([i+1, i+1])
            self.brCorner[i] = self.brCorner[i].convert()
            self.brCorner[i].fill((0,255,0))
        
    def loadSkinTexture(self):
        self.skinTexture = [None] * ZOOMS
        for i in range(ZOOMS):
            self.skinTexture[i] = pygame.transform.scale(self.theLoop.loadedTexture, (self.theLoop.loadedTexture.get_width()*(i+1), self.theLoop.loadedTexture.get_height()*(i+1)))
        self.updateSkinRect()
        
    def updateSkinRect(self):
        self.skinRect = self.skinTexture[self.currentZoom].get_rect()
        self.skinRect.center = self.theLoop.viewport.center
        
########################################################################################
########################################################################################
########################################DISPLAY#########################################
########################################################################################
########################################################################################
        
    def displayViewport(self):
        self.theLoop.screen.blit(self.bgfill, self.theLoop.viewport)
        self.theLoop.screen.blit(self.skinTexture[self.currentZoom], self.skinRect)
        self.displayClipCorners()
    
    def displayButtons(self):
        #MODE BUTTONS
        for i in range(0,3):
            rect = pygame.rect.Rect((724+(138*i),180), (134, 38))
            if self.theLoop.currentMode == i: self.theLoop.screen.blit(self.theLoop.on, rect)
            else: self.theLoop.screen.blit(self.theLoop.off, rect)
            self.displayButtonText(True, i, rect)
        #ACTION BUTTONS
        button = 0
        for y in range (0,3):
            for x in range(0,3):
                rect = pygame.rect.Rect((724+(138*x),240+(40*y)), (134, 38))
                if self.theLoop.mousePressed == button: self.theLoop.screen.blit(self.theLoop.on, rect)
                else: self.theLoop.screen.blit(self.theLoop.off, rect)
                self.displayButtonText(False, button, rect)
                button = button + 1
        for y in range (0,2):
            rect = pygame.rect.Rect((724,457+(40*y)), (134, 38))
            if self.theLoop.mousePressed == button: self.theLoop.screen.blit(self.theLoop.on, rect)
            else: self.theLoop.screen.blit(self.theLoop.off, rect)
            self.displayButtonText(False, button, rect)
            button = button + 1
        #MENU BUTTON
        rect = pygame.rect.Rect((862,140), (134, 38))
        if self.theLoop.mousePressed == button: self.theLoop.screen.blit(self.theLoop.on, rect)
        else: self.theLoop.screen.blit(self.theLoop.off, rect)
        self.displayButtonText(False, button, rect)
        
        self.displayText()
        self.displayClipIcons()
            
    def displayText(self):
        if self.currentClip == -1: self.theLoop.displayText("CLIPNAME: N/A", (937,439))
        else: self.theLoop.displayText("CLIPNAME: "+self.clips[self.currentClip].clipname, (937,439))
        
        if self.currentTool == 0: self.theLoop.displayText("CURRENTTOOL: None", (400,85))
        elif self.currentTool == 1: self.theLoop.displayText("CURRENTTOOL: Top Left Point", (400,85))
        elif self.currentTool == 2: self.theLoop.displayText("CURRENTTOOL: Bottom Right Point", (400,85))
            
    def displayButtonText(self, type, button, rect):
        if type: string = MODETEXT[button]
        else: string = BUTTONTEXT[button]
        image = self.theLoop.font.render(string, 1, (0, 0, 0))
        imagerect = image.get_rect()
        imagerect.center = rect.center
        self.theLoop.screen.blit(image, imagerect)

    def displayClipCorners(self):
        offset = [self.skinRect.x, self.skinRect.y]
        if self.currentClip != -1:
            if self.currentTool != TOOLTYPE["TLEFT"]: 
                tl = self.clips[self.currentClip].topleft
                spots = [tl[0]*(self.currentZoom+1), tl[1]*(self.currentZoom+1)]
                self.theLoop.screen.blit(self.tlCorner[self.currentZoom], (offset[0]+spots[0], offset[1]+spots[1]))
            if self.currentTool != TOOLTYPE["BRIGHT"]: 
                br = self.clips[self.currentClip].botright
                spots = [br[0]*(self.currentZoom+1), br[1]*(self.currentZoom+1)]
                self.theLoop.screen.blit(self.brCorner[self.currentZoom], (offset[0]+spots[0], offset[1]+spots[1]))
        
    def displayClipIcons(self):
        counter = 0
        for clip in self.clips:
            if counter > 5: y = 497
            else: y = 457
            x = (counter%6)*40
            rect = pygame.rect.Rect((862+x, y), (36, 36))
            self.displayIcon(self.theLoop.screen, clip, rect)
            counter += 1

    def displayIcon(self, screen, current, rect):
        if current == self.currentClip: screen.blit(self.theLoop.buton, rect)
        else: screen.blit(self.theLoop.butoff, rect)        
        
########################################################################################
########################################################################################
#########################################INPUT##########################################
########################################################################################
########################################################################################
        
    def checkButtonPress(self):
        if self.currentTool != 0:
            if self.skinRect.collidepoint(self.theLoop.mousePos): 
                pixelSpot = self.getPixelOnSheet()
                self.runToolAction(pixelSpot)
        #MODE BUTTONS
        for i in range (0,3):
            rect = pygame.rect.Rect((724+(138*i),180), (134, 38))
            if rect.collidepoint(self.theLoop.mousePos):
                break
        #ACTION BUTTONS
        button = 0
        for y in range (0,3):
            for x in range(0,3):
                rect = pygame.rect.Rect((724+(138*x),240+(40*y)), (134, 38))
                if rect.collidepoint(self.theLoop.mousePos): 
                    self.theLoop.mousePressed = button
                    break
                button = button+1
        for y in range (0,2):
            rect = pygame.rect.Rect((724,457+(40*y)), (134, 38))
            if rect.collidepoint(self.theLoop.mousePos): 
                self.theLoop.mousePressed = button
                break
            button = button+1
            
        #MENU BUTTON
        rect = pygame.rect.Rect((862,140), (134, 38))
        if rect.collidepoint(self.theLoop.mousePos): 
            self.theLoop.mousePressed = button
        
        counter = 0
        #CLIP BUTTONS
        for clip in self.clips:
            if counter > 5: y = 497
            else: y = 457
            x = (counter%6)*40
            rect = pygame.rect.Rect((862+x, y), (36, 36))
            if rect.collidepoint(self.theLoop.mousePos):
                self.currentClip = clip
                self.currentTool = 0
                break
            counter += 1
            
    def checkButtonRelease(self):
        self.theLoop.mousePressed = -1
        #MODE BUTTONS
        for i in range (0,3):
            rect = pygame.rect.Rect((724+(138*i),180), (134, 38))
            if rect.collidepoint(self.theLoop.mousePos): 
                if i == 0:
                    self.theLoop.currentMode = i
                    self.currentTool = 0
                    break
                elif i == 1:
                    if self.theLoop.clipsLocked:
                        self.theLoop.currentMode = i
                        self.currentTool = 0
                        break
                    else: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Clips Not Locked")
                elif i == 2: pass

        #ACTION BUTTONS
        button = 0
        for y in range (0,3):
            for x in range(0,3):
                rect = pygame.rect.Rect((724+(138*x),240+(40*y)), (134, 38))
                if rect.collidepoint(self.theLoop.mousePos): 
                    self.currentTool = 0
                    self.buttonPressed(button)
                    break
                button = button+1
        for y in range (0,2):
            rect = pygame.rect.Rect((724,457+(40*y)), (134, 38))
            if rect.collidepoint(self.theLoop.mousePos): 
                self.currentTool = 0
                self.buttonPressed(button)
                break
            button = button+1
            
        #MENU BUTTON
        rect = pygame.rect.Rect((862,140), (134, 38))
        if rect.collidepoint(self.theLoop.mousePos): 
            self.currentTool = 0
            self.buttonPressed(button)
        
    def buttonPressed(self, button):
        if button == 0: self.renameClip()
        elif button == 1: self.resetClips()
        elif button == 2: self.changeBackgroundColor()
        elif button == 3: self.setToolType("TLEFT")
        elif button == 4: self.lockClips()
        elif button == 5: self.controlZoom(True)
        elif button == 6: self.setToolType("BRIGHT")
        elif button == 7: self.unlockClips()
        elif button == 8: self.controlZoom(False)
        elif button == 9: self.createNewClip()
        elif button == 10: self.deleteClip()
        elif button == 11: self.theLoop.stillRunning = False
        
    def rightClickPressed(self):
        pass
        
########################################################################################
########################################################################################
########################################ACTIONS#########################################
########################################################################################
########################################################################################
        
    def setToolType(self, type):
        if self.theLoop.clipsLocked: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Clips Are Locked")
        elif self.currentClip != -1: self.currentTool = TOOLTYPE[type]
        else: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Clip Not Selected")
        
    def getPixelOnSheet(self):
        diff = [self.theLoop.mousePos[0]-self.skinRect.x, self.theLoop.mousePos[1]-self.skinRect.y]
        unscaled = [diff[0]/(self.currentZoom+1), diff[1]/(self.currentZoom+1)]
        return unscaled
    
    def runToolAction(self, pixelSpot):
        if self.currentTool == TOOLTYPE["TLEFT"]: self.clips[self.currentClip].topleft = pixelSpot
        elif self.currentTool == TOOLTYPE["BRIGHT"]: self.clips[self.currentClip].botright = pixelSpot
        self.currentTool = 0
        
    def resetClips(self):
        if self.theLoop.clipsLocked:
            self.theLoop.promptObject.promptWindow(self.theLoop.screen, "WARNING YOU WILL")
            self.theLoop.promptObject.promptWindow(self.theLoop.screen, "LOSE ALL ANIMATION")
            self.theLoop.promptObject.promptWindow(self.theLoop.screen, "AND HAND POS DATA.")
            if self.theLoop.windowObject.inputWindow(self.theLoop.screen, "Type YES: ") == "YES": 
                self.clips = {}
                self.clipCounter = 0
                self.clearAnimData()
                self.theLoop.clipsLocked = False
    
    def lockClips(self):
        if not self.theLoop.clipsLocked:
            for clip in self.clips:
                self.clips[clip].getDims()
            self.theLoop.modes[1].getClipData()
            self.theLoop.clipsLocked = True
        else: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "ALREADY LOCKED!")
        
    def unlockClips(self):
        if self.theLoop.clipsLocked:
            self.theLoop.promptObject.promptWindow(self.theLoop.screen, "WARNING YOU WILL")
            self.theLoop.promptObject.promptWindow(self.theLoop.screen, "LOSE ALL ANIMATION")
            self.theLoop.promptObject.promptWindow(self.theLoop.screen, "AND HAND POS DATA.")
            if self.theLoop.windowObject.inputWindow(self.theLoop.screen, "Type YES: ") == "YES": 
                self.clearAnimData()
                self.theLoop.clipsLocked = False
                
    def clearAnimData(self):
        self.theLoop.modes[1].clipObjects = {}
        self.theLoop.modes[1].animations = {}
        self.theLoop.modes[1].animCounter = 0
        self.theLoop.modes[1].currentAnim = -1
        
    def printSpots(self):
        for clip in self.clips:
            print clip, self.clips[clip].topleft, self.clips[clip].botright
        
    def createNewClip(self):
        if self.theLoop.clipsLocked: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Clips Are Locked")
        else:
            if len(self.clips) < 12:
                self.clipCounter += 1
                self.clips[self.clipCounter] = Clip("CLIPPING_"+str(self.clipCounter))
            
    def deleteClip(self):
        if self.theLoop.clipsLocked: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Clips Are Locked")
        else:
            if self.currentClip != -1:
                del self.clips[self.currentClip]
                self.currentClip = -1
                
    def renameClip(self):
        if self.theLoop.clipsLocked: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Clips Are Locked")
        else:
            if self.currentClip != -1:
                runRename = True
                newName = self.theLoop.windowObject.inputWindow(self.theLoop.screen, "Rename: ")
                if newName == "": self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Invalid Name")
                else: 
                    for clip in self.clips:
                        if newName == self.clips[clip].clipname: 
                            self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Name In Use")
                            runRename = False
                    if runRename: self.clips[self.currentClip].clipname = newName
        
    def controlZoom(self, type):
        if self.currentZoom < ZOOMS-1 and type: self.currentZoom += 1
        elif self.currentZoom > 0 and not type: self.currentZoom -= 1
        self.updateSkinRect()
        
    def changeBackgroundColor(self):
        self.bgfillID += 1
        if self.bgfillID == len(BGRNDCOLORS): self.bgfillID = 0
        self.bgfill = pygame.Surface([488, 489])
        self.bgfill = self.bgfill.convert()
        self.bgfill.fill(BGRNDCOLORS[self.bgfillID])
        
class Clip:
    def __init__(self, name):
        self.clipname = name
        self.topleft = [0,0]
        self.botright = [0,0]
        
    def getDims(self):
        self.width = self.botright[0] - self.topleft[0] + 1
        self.height = self.botright[1] - self.topleft[1] + 1  