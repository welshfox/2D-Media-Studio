import pygame, os
import cPickle as pickle

######FILE BROWSER/TYPE##########
import imghdr, Tkinter
from os.path import basename
from tkFileDialog import askopenfilename
tk_root = Tkinter.Tk()
tk_root.withdraw()
#################################

#####MODEL MODULE CLASSES########
from Clipper import Clipper
from Animator import Animator
from AnimEditor import AnimEditor
#################################

from InputPrompt import InputWindow
from MessagePrompt import PromptWindow

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3
MOUSE_WUP = 4
MOUSE_WDOWN = 5

class ModelMaster:
    def __init__(self, screen, images, moduleName, projectPath):
        self.screen = screen
        self.viewport = pygame.rect.Rect((143,116), (488, 489))
        
        self.moduleName = moduleName
        self.projectPath = projectPath
        self.textureName = ""
        
        self.clipsLocked = False
        self.stillRunning = True
        self.mousePressed = -1
        
        self.currentMode = 0
        self.modes = {}
        
        self.loadImages(images)
        self.initObjects(images)
        
    def loadImages(self, images):
        self.loadBackground()
        self.font = images.font
        self.overlay = images.overlay
        self.on = images.on
        self.off = images.off
        self.buton = images.buton
        self.butoff = images.butoff
        self.framecontrol = [[images.play, images.newframe, images.delframe],[images.playon, images.newframeon, images.delframeon]]
        self.partframe = images.partframe
        
    def loadBackground(self):
        self.bgfill = pygame.Surface([488, 489])
        self.bgfill = self.bgfill.convert()
        self.bgfill.fill((0, 0, 0))
        
    def initObjects(self, images):
        self.windowObject = InputWindow(images)
        self.promptObject = PromptWindow(images)
        self.modes[0] = Clipper(self)
        self.modes[1] = Animator(self)
        self.modes[2] = AnimEditor(self)
        
    def main(self):
        clock = pygame.time.Clock()
        milliseconds = 0.
        playtime = 0.
        ticktimer = 0.
        animtimer = 0.
        while self.stillRunning:
            milliseconds = clock.tick()
            delta = milliseconds/1000.0
            playtime += milliseconds/1000.0
            pygame.display.set_caption("FPS: " + str(clock.get_fps()))
            self.mousePos = pygame.mouse.get_pos()
                           
            self.getInput()

            self.modes[self.currentMode].displayViewport()
            self.displayOverlay()
            self.modes[self.currentMode].displayButtons()
                           
            if playtime-animtimer >= .025:
                animtimer = playtime
            if playtime-ticktimer >= .250:
                ticktimer = playtime
            
            pygame.display.flip()
            
        self.saveModule()
            
        del self.modes[0]
        del self.modes[1]
        del self.modes[2]
            
    def displayOverlay(self):
        self.screen.blit(self.overlay, (0,0))
            
    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.stillRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT: self.modes[self.currentMode].checkButtonPress()
                if event.button == MOUSE_RIGHT: self.modes[self.currentMode].rightClickPressed()
                if event.button == MOUSE_MIDDLE: pass
                if event.button == MOUSE_WUP: pass
                if event.button == MOUSE_WDOWN: pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_LEFT: self.modes[self.currentMode].checkButtonRelease()
                if event.button == MOUSE_RIGHT: pass
                if event.button == MOUSE_MIDDLE: pass
                if event.button == MOUSE_WUP: pass
                if event.button == MOUSE_WDOWN: pass
            elif event.type == pygame.QUIT: self.stillRunning = False
        
    def displayText(self, text, center):
        color = {0:(0,0,0),1:(255,255,255)}
        for i in range(0,2):
            point = [center[0]-(i*3), center[1]-(i*3)]
            image = self.font.render(text, 1, color[i])
            imagerect = image.get_rect()
            imagerect.center = point
            self.screen.blit(image, imagerect)
        
    def loadModelTexture(self):
        if os.path.exists("../Projects/" + self.projectPath + "/Models/" + self.moduleName + "/" + self.textureName + ".png"):
            self.loadedTexture = pygame.image.load("../Projects/" + self.projectPath + "/Models/" + self.moduleName + "/" + self.textureName + ".png").convert_alpha()
            self.modes[0].loadSkinTexture()
        else: 
            self.promptObject.promptWindow(self.screen, "Texture Not Found")
            self.promptObject.promptWindow(self.screen, "Load Texture \"" + self.textureName + "\"")
    
    def getModelTexture(self):
        imagepath = askopenfilename(filetypes=[("Image", "*.png")],)
        if imagepath != "":
            if imghdr.what(imagepath) == "png":
                self.textureName = basename(imagepath)
                self.loadedTexture = pygame.image.load(imagepath).convert_alpha()
                self.copyImageToLocal()
                self.modes[0].loadSkinTexture()
                self.main()
            else: self.promptObject.promptWindow(self.screen, "BAD IMAGE: USE PNG")
        else: self.promptObject.promptWindow(self.screen, "CANCELLED")
    
    def copyImageToLocal(self):
        path = "../Projects/" + self.projectPath + "/Models/" + self.moduleName + "/" + self.textureName + ".png"
        pygame.image.save(self.loadedTexture, path)
    
    def saveAnimation(self):
        animation = self.modes[1].animations[self.modes[1].currentAnim]
        #SAVE THE ANIMATION CLASS THAT CONTAINS THE FRAMES AND CONTENT OF FRAMES
    
    def loadAnimation(self):
        #INSERT A LOAD CHECKER HERE AND LOAD FRAMES, COUNTER INFORMATION
        #IF NO SAVE IS FOUND FOR THE ANIMATION THEN SET COUNTER TO 0
        self.modes[1].animations[self.modes[1].currentAnim].frameCounter = 0 #THIS NEEDS TO BE PUT INTO AN ELSE CASE
    
    def saveModule(self):
        if os.path.isdir("../Projects/" + self.projectPath + "/Models/" + self.moduleName):
            clipperData = {"quantity": self.modes[0].clipCounter, "clips": self.modes[0].clips, "texture": self.textureName, "clipStatus": self.clipsLocked}
            pickle.dump( clipperData, open( "../Projects/" + self.projectPath + "/Models/" + self.moduleName + "/clipperData.p", "wb" ) )
            
            #THIS IS WHERE YOU SAVE THE ANIMATION COUNTER, ANIMATION NAMES
            #animatorData = {##COUNTER##NAMES}
            #pickle.dump( animatorData, open( "../Projects/" + self.projectPath + "/Models/" + self.moduleName + "/animatorData.p", "wb" ) )
    
    def loadModule(self):
        if os.path.isdir("../Projects/" + self.projectPath + "/Models/" + self.moduleName):
            if os.path.exists("../Projects/" + self.projectPath + "/Models/" + self.moduleName + "/clipperData.p"):
                saveData = pickle.load( open( "../Projects/" + self.projectPath + "/Models/" + self.moduleName + "/clipperData.p", "rb" ) )
                self.modes[0].clipCounter = saveData["quantity"]
                self.modes[0].clips = saveData["clips"]
                self.clipsLocked = saveData["clipStatus"]
                self.textureName = saveData["texture"]
                self.loadModelTexture()
                if self.clipsLocked: 
                    self.modes[1].getClipData()
                    #THIS IS WHERE IT WILL LOAD THE ANIMATION DATA [COUNTER, NAMES]
                self.main()
                
                