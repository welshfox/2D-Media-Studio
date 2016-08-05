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
               0:"N/A",
               1:"RENAME",
               2:"BGRNDCOLOR",
               3:"SHOWCOLIDE",
               4:"EDIT ANIM",
               5:"ZOOM IN",
               6:"SHOWHNDPOS",
               7:"PLAY ANIM",
               8:"ZOOM OUT",
               9:"NEW ANIM",
               10:"DEL ANIM",
               11:"MENU"
              }        

class Animator:
    def __init__(self, mainloop):
        self.theLoop = mainloop
        self.currentZoom = 0
        
        self.clipObjects = []
        self.clipCount = 0
        
        self.animations = {}
        self.animCounter = 0
        self.currentAnim = -1
        
        self.loadBackground()
        
    def loadBackground(self):
        self.bgfillID = 0
        self.bgfill = pygame.Surface([488, 489])
        self.bgfill = self.bgfill.convert()
        self.bgfill.fill(BGRNDCOLORS[self.bgfillID])
        
########################################################################################
########################################################################################
######################################PULL DATA#########################################
########################################################################################
########################################################################################
        
    def getClipData(self):
        self.generateClipImages()
        
    def generateClipImages(self):
        clips = self.theLoop.modes[0].clips
        sheet = self.theLoop.loadedTexture
        for clip in clips:
            images = [None] * ZOOMS
            self.clipObjects.append(ClipObject())
            self.clipObjects[self.clipCount] = ClipObject()
            self.clipObjects[self.clipCount].clipname = clips[clip].clipname
            sheet.set_clip(pygame.Rect(clips[clip].topleft, (clips[clip].width, clips[clip].height)))
            cliptexture = sheet.subsurface(sheet.get_clip())
            for i in range(ZOOMS):
                images[i] = pygame.transform.scale(cliptexture, (clips[clip].width+(i*clips[clip].width), clips[clip].height+(i*clips[clip].height)))
            self.clipObjects[self.clipCount].textures = images
            self.clipObjects[self.clipCount].updateRect(self.currentZoom)
            self.clipCount += 1
        
########################################################################################
########################################################################################
########################################DISPLAY#########################################
########################################################################################
########################################################################################
        
    def displayViewport(self):
        self.theLoop.screen.blit(self.bgfill, self.theLoop.viewport)
        #IF ANIM SELECTED SHOW THE ANIMATION FRAME 0 
        
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
        
        self.displayAnimIcons()
        self.displayText()

    def displayText(self):
        if self.currentAnim == -1: self.theLoop.displayText("ANIMNAME: N/A", (937,439))
        else: self.theLoop.displayText("ANIMNAME: "+self.animations[self.currentAnim].name, (937,439))
        
    def displayAnimIcons(self):
        counter = 0
        for anim in self.animations:
            if counter > 5: y = 497
            else: y = 457
            x = (counter%6)*40
            rect = pygame.rect.Rect((862+x, y), (36, 36))
            self.displayIcon(self.theLoop.screen, anim, rect)
            counter += 1
            
    def displayButtonText(self, type, button, rect):
        if type: string = MODETEXT[button]
        else: string = BUTTONTEXT[button]
        image = self.theLoop.font.render(string, 1, (0, 0, 0))
        imagerect = image.get_rect()
        imagerect.center = rect.center
        self.theLoop.screen.blit(image, imagerect)

    def displayIcon(self, screen, current, rect):
        if current == self.currentAnim: screen.blit(self.theLoop.buton, rect)
        else: screen.blit(self.theLoop.butoff, rect)     
        
########################################################################################
########################################################################################
#########################################INPUT##########################################
########################################################################################
########################################################################################
        
    def checkButtonPress(self):
        #MODE BUTTONS
        for i in range (0,3):
            if i != 2:
                rect = pygame.rect.Rect((724+(138*i),180), (134, 38))
                if rect.collidepoint(self.theLoop.mousePos): 
                    self.theLoop.currentMode = i
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
        #ANIM BUTTONS
        for anim in self.animations:
            if counter > 5: y = 497
            else: y = 457
            x = (counter%6)*40
            rect = pygame.rect.Rect((862+x, y), (36, 36))
            if rect.collidepoint(self.theLoop.mousePos):
                self.currentAnim = anim
                break
            counter += 1
                
    def checkButtonRelease(self):
        self.theLoop.mousePressed = -1
        #MODE BUTTONS
        for i in range (0,3):
            if i != 2:
                rect = pygame.rect.Rect((724+(138*i),180), (134, 38))
                if rect.collidepoint(self.theLoop.mousePos): 
                    self.theLoop.currentMode = i
                    break
        #ACTION BUTTONS
        button = 0
        for y in range (0,3):
            for x in range(0,3):
                rect = pygame.rect.Rect((724+(138*x),240+(40*y)), (134, 38))
                if rect.collidepoint(self.theLoop.mousePos): 
                    self.buttonPressed(button)
                    break
                button = button+1
        for y in range (0,2):
            rect = pygame.rect.Rect((724,457+(40*y)), (134, 38))
            if rect.collidepoint(self.theLoop.mousePos):
                self.buttonPressed(button)
                break
            button = button+1
        #MENU BUTTON
        rect = pygame.rect.Rect((862,140), (134, 38))
        if rect.collidepoint(self.theLoop.mousePos):
            self.buttonPressed(button)
        
    def buttonPressed(self, button):
        if button == 0: print self.animations #N/A
        elif button == 1: self.renameAnim()
        elif button == 2: self.changeBackgroundColor()
        elif button == 3: print "3" #SHOW COLLIDERS
        elif button == 4: self.editAnim()
        elif button == 5: self.controlZoom(True)
        elif button == 6: print "6" #SHOW HAND POSITIONS
        elif button == 7: print "7" #PLAY ANIMATION
        elif button == 8: self.controlZoom(False)
        elif button == 9: self.createNewAnim()
        elif button == 10: self.deleteAnim()
        elif button == 11: self.theLoop.stillRunning = False
        
    def rightClickPressed(self):
        pass
        
########################################################################################
########################################################################################
########################################ACTIONS#########################################
########################################################################################
########################################################################################
        
    def controlZoom(self, type):
        if self.currentZoom < ZOOMS-1 and type: self.currentZoom += 1
        elif self.currentZoom > 0 and not type: self.currentZoom -= 1
        #UPDATE CURRENT ANIMATION RECTS
        
    def changeBackgroundColor(self):
        self.bgfillID += 1
        if self.bgfillID == len(BGRNDCOLORS): self.bgfillID = 0
        self.bgfill = pygame.Surface([488, 489])
        self.bgfill = self.bgfill.convert()
        self.bgfill.fill(BGRNDCOLORS[self.bgfillID])
        
    def renameAnim(self):
        if self.currentAnim != -1:
            runRename = True
            newName = self.theLoop.windowObject.inputWindow(self.theLoop.screen, "Rename: ")
            if newName == "": self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Invalid Name")
            else: 
                for anim in self.animations:
                    if newName == self.animations[anim].name: 
                        self.theLoop.promptObject.promptWindow(self.theLoop.screen, "Name In Use")
                        runRename = False
                if runRename: self.animations[self.currentAnim].name = newName
        
    def createNewAnim(self):
        if len(self.animations) < 12:
            self.animCounter += 1
            self.animations[self.animCounter] = Animation()
            self.animations[self.animCounter].name = "ANIMATION_"+str(self.animCounter)
            
    def deleteAnim(self):
        if self.currentAnim != -1:
            del self.animations[self.currentAnim]
            self.currentAnim = -1
        
    def editAnim(self):
        if self.currentAnim != -1:
            self.theLoop.modes[2].prepareEnvironment(self.animations[self.currentAnim])
            self.theLoop.currentMode = 2
            
        
class ClipObject:
    def __init__(self):
        self.clipname = ""
        self.textures = [None] * ZOOMS
        self.rect = None
    def updateRect(self, currentZoom):
        self.rect = self.textures[currentZoom].get_rect()
        
class Animation:
    def __init__(self):
        self.name = ""
        self.frames = {}
        self.frameCounter = 0
        self.frameOrder = []
        self.boundBox = [-1,-1]