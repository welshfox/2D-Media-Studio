import pygame, os

from ProjectObject import *
from MasterClasses import *

from InputPrompt import InputWindow
from MessagePrompt import PromptWindow

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (25,25)

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3
MOUSE_WUP = 4
MOUSE_WDOWN = 5
      
MAINMENUTEXT = {
              0:"NEW",
              1:"LOAD"
             }
BUTTONTEXT = {
              0:"CLOSE",
              1:"SAVE",
              2:"LOADMODEL",
              3:"LOADITEM",
              4:"LOADGUI",
              5:"NEWMODEL",
              6:"NEWITEM",
              7:"NEWGUI"
             }

class Images:
    def __init__(self):
        self.font = pygame.font.Font("../Assets/font.ttf", 18)
        self.overlay = pygame.image.load("../Assets/overlay.png").convert_alpha()
        self.on = pygame.image.load("../Assets/on.png").convert_alpha()
        self.off = pygame.image.load("../Assets/off.png").convert_alpha()
        self.buton = pygame.image.load("../Assets/buton.png").convert_alpha()
        self.butoff = pygame.image.load("../Assets/butoff.png").convert_alpha()
        self.prompt = pygame.image.load("../Assets/prompt.png").convert_alpha()
        self.play = pygame.image.load("../Assets/play.png").convert_alpha()
        self.newframe = pygame.image.load("../Assets/newframe.png").convert_alpha()
        self.delframe = pygame.image.load("../Assets/delframe.png").convert_alpha()
        self.playon = pygame.image.load("../Assets/playon.png").convert_alpha()
        self.newframeon = pygame.image.load("../Assets/newframeon.png").convert_alpha()
        self.delframeon = pygame.image.load("../Assets/delframeon.png").convert_alpha()
        self.partframe = pygame.image.load("../Assets/partviewerframe.png").convert_alpha()
             
class Start:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([1280, 720])
        self.viewport = pygame.rect.Rect((143,116), (488, 489))
        
        self.projectPath = ""
        self.projectLoaded = False
        
        self.stillRunning = True
        self.mousePressed = -1
        self.currentMode = 0
        
        self.loadBackground()
        self.loadImages()
        self.initObects()
        
    def loadBackground(self):
        self.bgfill = pygame.Surface([488, 489])
        self.bgfill = self.bgfill.convert()
        self.bgfill.fill((0, 0, 0))
        
    def loadImages(self):
        self.images = Images()
        self.font = self.images.font
        self.overlay = self.images.overlay
        self.on = self.images.on
        self.off = self.images.off
        self.buton = self.images.buton
        self.butoff = self.images.butoff
        
    def initObects(self):
        self.windowObject = InputWindow(self.images)
        self.promptObject = PromptWindow(self.images)
        
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
            
            self.displayViewport()
            self.displayOverlay()
            self.displayButtons()
            self.displayInfoText()
                           
            if playtime-animtimer >= .025:
                animtimer = playtime
            if playtime-ticktimer >= .250:
                ticktimer = playtime
            
            pygame.display.flip()
            
        if self.projectLoaded: self.saveButtonPressed()
        pygame.display.quit()
        
########################################################################################
########################################################################################
########################################DISPLAY#########################################
########################################################################################
########################################################################################
        
    def displayViewport(self):
        self.screen.blit(self.bgfill, self.viewport)
        
    def displayOverlay(self):
        self.screen.blit(self.overlay, (0,0))
        
    def displayButtons(self):
        #MODE BUTTONS
        button = 0
        if not self.projectLoaded:
            for i in range(0,2):
                rect = pygame.rect.Rect((862,180+(i*40)), (134, 38))
                if self.mousePressed == button: self.screen.blit(self.on, rect)
                else: self.screen.blit(self.off, rect)
                self.displayButtonText(True, button, rect)
                button += 1
        else:
            for i in range(0,2):
                rect = pygame.rect.Rect((862,180+(i*40)), (134, 38))
                if self.mousePressed == button: self.screen.blit(self.on, rect)
                else: self.screen.blit(self.off, rect)
                self.displayButtonText(False, button, rect)
                button += 1
            for i in range(0,3):
                rect = pygame.rect.Rect((724+(138*i),260), (134, 38))
                if self.mousePressed == button: self.screen.blit(self.on, rect)
                else: self.screen.blit(self.off, rect)
                self.displayButtonText(False, button, rect)
                button += 1
            for i in range(0,3):
                rect = pygame.rect.Rect((724+(138*i),300), (134, 38))
                if self.mousePressed == button: self.screen.blit(self.on, rect)
                else: self.screen.blit(self.off, rect)
                self.displayButtonText(False, button, rect)
                button += 1
            
    def displayButtonText(self, type, button, rect):
        if type: string = MAINMENUTEXT[button]
        else: string = BUTTONTEXT[button]
        image = self.font.render(string, 1, (0, 0, 0))
        imagerect = image.get_rect()
        imagerect.center = rect.center
        self.screen.blit(image, imagerect)
        
    def displayInfoText(self):
        if self.projectPath != "": string = self.projectPath
        else: string = "N/A"
        self.displayText("Project Name: " + string, (926, 451))
        self.displayText("Project Loaded: " + str(self.projectLoaded), (926, 471))
        
        if self.projectLoaded:
            self.displayText("Models: ", (826, 511))
            self.displayText(str(self.projectObject.getModuleQty(0)), (826, 531))
            
            self.displayText("Objects: ", (926, 511))
            self.displayText(str(self.projectObject.getModuleQty(1)), (926, 531))
            
            self.displayText("GUIs: ", (1026, 511))
            self.displayText(str(self.projectObject.getModuleQty(2)), (1026, 531))

    def displayText(self, text, center):
        color = {0:(0,0,0),1:(255,255,255)}
        for i in range(0,2):
            point = [center[0]-(i*3), center[1]-(i*3)]
            image = self.font.render(text, 1, color[i])
            imagerect = image.get_rect()
            imagerect.center = point
            self.screen.blit(image, imagerect)
        
########################################################################################
########################################################################################
#########################################INPUT##########################################
########################################################################################
########################################################################################
        
    def getInput(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.stillRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT: self.checkButtonPress()
                if event.button == MOUSE_RIGHT: pass
                if event.button == MOUSE_MIDDLE: pass
                if event.button == MOUSE_WUP: pass
                if event.button == MOUSE_WDOWN: pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_LEFT: self.checkButtonRelease()
                if event.button == MOUSE_RIGHT: pass
                if event.button == MOUSE_MIDDLE: pass
                if event.button == MOUSE_WUP: pass
                if event.button == MOUSE_WDOWN: pass
            elif event.type == pygame.QUIT: self.stillRunning = False
            
    def checkButtonPress(self):
        button = 0 
        if not self.projectLoaded:
            for i in range(0,2):
                rect = pygame.rect.Rect((862,180+(i*40)), (134, 38))
                if rect.collidepoint(self.mousePos): 
                    self.mousePressed = button
                button += 1
        else:
            for i in range(0,2):
                rect = pygame.rect.Rect((862,180+(i*40)), (134, 38))
                if rect.collidepoint(self.mousePos): 
                    self.mousePressed = button
                button += 1
            for i in range(0,3):
                rect = pygame.rect.Rect((724+(138*i),260), (134, 38))
                if rect.collidepoint(self.mousePos): 
                    self.mousePressed = button
                button += 1
            for i in range(0,3):
                rect = pygame.rect.Rect((724+(138*i),300), (134, 38))
                if rect.collidepoint(self.mousePos): 
                    self.mousePressed = button
                button += 1
            
    def checkButtonRelease(self):
        self.mousePressed = -1
        button = 0 
        if not self.projectLoaded:
            for i in range(0,2):
                rect = pygame.rect.Rect((862,180+(i*40)), (134, 38))
                if rect.collidepoint(self.mousePos): 
                    self.buttonPressed(button)
                button += 1
        else:
            for i in range(0,2):
                rect = pygame.rect.Rect((862,180+(i*40)), (134, 38))
                if rect.collidepoint(self.mousePos): 
                    self.buttonPressed(button)
                button += 1
            for i in range(0,3):
                rect = pygame.rect.Rect((724+(138*i),260), (134, 38))
                if rect.collidepoint(self.mousePos): 
                    self.buttonPressed(button)
                button += 1
            for i in range(0,3):
                rect = pygame.rect.Rect((724+(138*i),300), (134, 38))
                if rect.collidepoint(self.mousePos): 
                    self.buttonPressed(button)
                button += 1
                    
    def buttonPressed(self, button):
        if not self.projectLoaded:
            if button == 0: self.newButtonPressed()
            elif button == 1: self.loadButtonPressed()
        else:
            if button == 0: self.closeButtonPressed()
            elif button == 1: self.saveButtonPressed()
            elif button == 2: self.loadModuleButtonPressed(0)
            elif button == 3: self.loadModuleButtonPressed(1)
            elif button == 4: self.loadModuleButtonPressed(2)
            elif button == 5: self.newModuleButtonPressed(0)
            elif button == 6: self.newModuleButtonPressed(1)
            elif button == 7: self.newModuleButtonPressed(2)
                
                
    ####################################
    ##########PROJECT METHODS###########
    ####################################
    def checkProjectPath(self):
        if os.path.isdir("../Projects/" + self.projectPath): 
            if not os.path.isdir("../Projects/" + self.projectPath + "/Models"): os.makedirs("../Projects/" + self.projectPath + "/Models")
            if not os.path.isdir("../Projects/" + self.projectPath + "/Objects"): os.makedirs("../Projects/" + self.projectPath + "/Objects")
            if not os.path.isdir("../Projects/" + self.projectPath + "/GUIs"): os.makedirs("../Projects/" + self.projectPath + "/GUIs")
            return True
        else: return False
                
    def createProjectPath(self):
        if not os.path.isdir("../Projects/" + self.projectPath): 
            os.makedirs("../Projects/" + self.projectPath)
            os.makedirs("../Projects/" + self.projectPath + "/Models")
            os.makedirs("../Projects/" + self.projectPath + "/Objects")
            os.makedirs("../Projects/" + self.projectPath + "/GUIs")
            return True
        else: 
            self.projectPath = ""
            self.promptObject.promptWindow(self.screen, "Project Already Exists")
            return False
        
        
    ####################################
    ##########MENU VIEW BUTTONS#########
    ####################################
    def loadButtonPressed(self):
        self.projectPath = self.windowObject.inputWindow(self.screen, "Enter Path: ")
        if self.projectPath != "" and self.checkProjectPath():
            self.projectLoaded = True
            self.projectObject = ProjectObject(self.projectPath, self.images)
            self.projectObject.loadProject()
            self.projectObject.validateModules(self.screen)
        else: 
            self.projectPath = ""
            self.promptObject.promptWindow(self.screen, " Project Not Found")
   
    def newButtonPressed(self):
        self.projectPath = self.windowObject.inputWindow(self.screen, "Enter Path: ")
        if self.projectPath != "": 
            if self.createProjectPath():
                self.projectLoaded = True
                self.projectObject = ProjectObject(self.projectPath, self.images)
        else: self.promptObject.promptWindow(self.screen, "Bad Project Name")
        
        
    ####################################
    ########PROJECT VIEW BUTTONS########
    ####################################
    def closeButtonPressed(self):
        self.saveButtonPressed()
        self.projectPath = ""
        self.projectLoaded = False
        self.projectObject = None
        
    def saveButtonPressed(self):
        self.projectObject.saveProject()
        
    def newModuleButtonPressed(self, type):
        name = self.windowObject.inputWindow(self.screen, "Enter Path: ")
        if name != "":
            if type == 0: path = "../Projects/" + self.projectPath + "/Models/" + name
            elif type == 1: path = "../Projects/" + self.projectPath + "/Objects/" + name
            elif type == 2: path = "../Projects/" + self.projectPath + "/GUIs/" + name
            if os.path.isdir(path): 
                self.promptObject.promptWindow(self.screen, "Module Already Exists")
            else: 
                os.makedirs(path)
                self.projectObject.addModule(type, name)
                self.startModuleLoop(type, name, True)
        else: self.promptObject.promptWindow(self.screen, "Bad Module Name")
                
    def loadModuleButtonPressed(self, type):
        name = self.windowObject.inputWindow(self.screen, "Enter Path: ")
        if name != "":
            if type == 0: path = "../Projects/" + self.projectPath + "/Models/" + name
            elif type == 1: path = "../Projects/" + self.projectPath + "/Objects/" + name
            elif type == 2: path = "../Projects/" + self.projectPath + "/GUIs/" + name
            if not os.path.isdir(path): 
                self.promptObject.promptWindow(self.screen, "Module Not Found")
            else: 
                self.startModuleLoop(type, name, False)
        else: self.promptObject.promptWindow(self.screen, "Bad Module Name")
        
    def startModuleLoop(self, type, name, isNew):
        if type == 0: 
            module = ModelMaster(self.screen, self.images, name, self.projectPath)
            if isNew: module.getModelTexture()
            else: module.loadModule()
        elif type == 1: pass
        elif type == 2: pass
                
window = Start()
window.main()