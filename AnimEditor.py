import pygame, operator

ZOOMS = 15
BGRNDCOLORS = {
               0:[125, 125, 125],
               1:[153, 255, 51],
               2:[0, 0, 0],
               3:[255, 255, 255]
              }
              
BUTTONTEXT =  {
               0:"SAVE",
               1:"RENMEOBJCT",
               2:"BGRNDCOLOR",
               3:"ONIONSKIN",
               4:"ROTATE",
               5:"ZOOM IN",
               6:"COLLIDER",
               7:"HANDPOS",
               8:"ZOOM OUT",
               9:"BOUNDNGBOX",
               10:"SETLAYER",
               11:"N/A",
               12:"SWITCH",
               13:"CHOOSE",
               14:"BACK"
              }
TOOLTYPE =    {
               "COLLIDER":1,
               "HANDPOS":2,
               "BOUNDBOX":3,
               "PLACER":4
              }
              
class AnimEditor:
    def __init__(self, mainloop):
        self.theLoop = mainloop
        
        self.viewOffset = [0, 0]
        self.currentZoom = 0    
        self.currentPart = 0
        self.currentTool = 0
        self.currentPartZoom = 0
        self.currentObject = -1
        self.currentCollider = -1
        
        self.onionSkinState = False
        self.dragEnabled = False
        
        self.animation = None
        self.currentFrame = -1
        self.oldData = None
        
        self.loadBackground()
        
    def loadBackground(self):
        self.bgfillID = 0
        self.bgfill = pygame.Surface([488, 489])
        self.bgfill = self.bgfill.convert()
        self.bgfill.fill(BGRNDCOLORS[self.bgfillID])
        
        self.partviewerRect = pygame.rect.Rect((862,425), (242, 137))
        self.partBG = pygame.Surface([242, 137])
        self.partBG = self.partBG.convert()
        self.partBG.fill(BGRNDCOLORS[self.bgfillID])
        
    def prepareEnvironment(self, animation):
        self.currentFrame = -1
        self.animation = animation
        self.theLoop.loadAnimation()
        
########################################################################################
########################################################################################
########################################DISPLAY#########################################
########################################################################################
########################################################################################
        
    def displayViewport(self):
        self.theLoop.screen.blit(self.bgfill, self.theLoop.viewport)
        self.displayViewportObjects()
        
    def displayViewportObjects(self):
        self.trackMouse()
        if self.currentFrame != -1: self.defineLayerOrder(self.currentFrame)
        #self.defineFrameOrder() #THIS SHOULD DEFINE A SEPERATE LIST THAT REFERENCES FRAMES IN THE ORDER THEN LATER BUTTONS ARE GENERATED USING THIS ORDERED LIST
        self.scrollViewport()
    
        self.displayOnionSkinObjects()
        self.displayFrameObjects()
        self.displayBoundBox()
        self.displayColliders()
        self.displayHandPos()
            
    def displayBoundBox(self):
        if self.animation.boundBox[0] != -1 and self.animation.boundBox[1] != -1:
            vp = self.theLoop.viewport
            zm = self.currentZoom+1
            bounds = self.animation.boundBox
            dims = [(bounds[1][0] - bounds[0][0]), (bounds[1][1] - bounds[0][1])]
            boundRects = []
            boundRects.append(pygame.rect.Rect((bounds[0][0]*(zm), bounds[0][1]*(zm)), (1*(zm), dims[1]*(zm))))
            boundRects.append(pygame.rect.Rect(((bounds[0][0]+1)*(zm), bounds[0][1]*(zm)), ((dims[0]-1)*(zm), 1*(zm))))
            boundRects.append(pygame.rect.Rect(((bounds[0][0]+dims[0])*(zm), bounds[0][1]*(zm)), (1*(zm), (dims[1]+1)*(zm))))
            boundRects.append(pygame.rect.Rect((bounds[0][0]*(zm), (bounds[0][1]+dims[1])*(zm)), ((dims[0])*(zm), 1*(zm))))
            if self.currentZoom == 0: scrollOffset = [0,0]
            else: scrollOffset = [self.viewOffset[0]*(self.currentZoom+1), self.viewOffset[1]*(self.currentZoom+1)]
            for rect in boundRects:
                image = pygame.Surface([rect.w, rect.h])
                image.fill(BGRNDCOLORS[2])
                image.set_alpha(100)
                rect.x += vp.x + scrollOffset[0]
                rect.y += vp.y + scrollOffset[1]
                self.theLoop.screen.blit(image, rect)
    
    def displayColliders(self):
        if self.currentFrame != -1:
            vp = self.theLoop.viewport
            zm = self.currentZoom+1
            counter = 0
            for collider in self.animation.frames[self.currentFrame].colliders:
                if collider[0] != -1 and collider[1] != -1:
                    bounds = collider
                    dims = [(bounds[1][0] - bounds[0][0]), (bounds[1][1] - bounds[0][1])]
                    boundRects = []
                    boundRects.append(pygame.rect.Rect((bounds[0][0]*(zm), bounds[0][1]*(zm)), (1*(zm), dims[1]*(zm))))
                    boundRects.append(pygame.rect.Rect(((bounds[0][0]+1)*(zm), bounds[0][1]*(zm)), ((dims[0]-1)*(zm), 1*(zm))))
                    boundRects.append(pygame.rect.Rect(((bounds[0][0]+dims[0])*(zm), bounds[0][1]*(zm)), (1*(zm), (dims[1]+1)*(zm))))
                    boundRects.append(pygame.rect.Rect((bounds[0][0]*(zm), (bounds[0][1]+dims[1])*(zm)), ((dims[0])*(zm), 1*(zm))))
                    if self.currentZoom == 0: scrollOffset = [0,0]
                    else: scrollOffset = [self.viewOffset[0]*zm, self.viewOffset[1]*zm]
                    for rect in boundRects:
                        image = pygame.Surface([rect.w, rect.h])
                        if counter == self.currentCollider: image.fill((255,200,0))
                        else: image.fill((255,0,0))
                        image.set_alpha(100)
                        rect.x += vp.x + scrollOffset[0]
                        rect.y += vp.y + scrollOffset[1]
                        self.theLoop.screen.blit(image, rect)
                counter += 1
    
    def displayHandPos(self):
        if self.currentFrame != -1:
            if self.animation.frames[self.currentFrame].handPos != -1:
                zoom = self.currentZoom+1
                vp = self.theLoop.viewport
                zm = self.currentZoom+1
                position = self.animation.frames[self.currentFrame].handPos
                
                if self.currentZoom == 0: scrollOffset = [0,0]
                else: scrollOffset = [self.viewOffset[0]*zm, self.viewOffset[1]*zm]
                rect = pygame.rect.Rect((position[0]*zm,position[1]*zm), (1*zm, 1*zm))
                rect.x += vp.x + scrollOffset[0]
                rect.y += vp.y + scrollOffset[1]
                
                image = pygame.Surface([rect.w, rect.h])
                image.fill((255,165,0))
                self.theLoop.screen.blit(image, rect)
    
    def displayOnionSkinObjects(self):
        if self.currentFrame != -1 and self.onionSkinState:
            if len(self.animation.frames) > 1: 
                last = None
                for frame in self.animation.frames:
                    if frame == self.currentFrame: 
                        if last != None: onionFrame = last
                        else: 
                            for frame in self.animation.frames:
                                onionFrame = frame
                        break
                    else: last = frame
                if len(self.animation.frames[onionFrame].objects) > 0:
                    self.defineLayerOrder(onionFrame)
                    for tuple in self.animation.frames[onionFrame].layerOrder:
                        object = tuple[0]
                        clipobjects = self.theLoop.modes[1].clipObjects
                        clipobject = clipobjects[object.type]
                        vp = self.theLoop.viewport
                        rect = clipobject.textures[self.currentZoom].get_rect()
                        
                        if self.currentZoom == 0: scrollOffset = [0,0]
                        else: scrollOffset = [self.viewOffset[0]*(self.currentZoom+1), self.viewOffset[1]*(self.currentZoom+1)]
                        
                        rect.x = (object.pos[0]*(self.currentZoom+1))+vp.x+scrollOffset[0]
                        rect.y = (object.pos[1]*(self.currentZoom+1))+vp.y+scrollOffset[1]
                        
                        image = clipobject.textures[self.currentZoom].copy()
                        image.fill((255, 255, 255, 75), None, pygame.BLEND_RGBA_MULT)
                        
                        render = self.rot_center(image, rect, object.rot)
                        
                        self.theLoop.screen.blit(render[0], render[1])

    def displayFrameObjects(self):
        if self.currentFrame != -1:
            for tuple in self.animation.frames[self.currentFrame].layerOrder:
                object = tuple[0]
                clipobjects = self.theLoop.modes[1].clipObjects
                clipobject = clipobjects[object.type]
                vp = self.theLoop.viewport
                rect = clipobject.textures[self.currentZoom].get_rect()
                
                if self.currentZoom == 0: scrollOffset = [0,0]
                else: scrollOffset = [self.viewOffset[0]*(self.currentZoom+1), self.viewOffset[1]*(self.currentZoom+1)]
                
                rect.x = (object.pos[0]*(self.currentZoom+1))+vp.x+scrollOffset[0]
                rect.y = (object.pos[1]*(self.currentZoom+1))+vp.y+scrollOffset[1]
                
                render = self.rot_center(clipobject.textures[self.currentZoom], rect, object.rot)
                self.theLoop.screen.blit(render[0], render[1])
                
    def displayButtons(self):
        #ACTION BUTTONS
        button = 0
        for y in range (0,4):
            for x in range(0,3):
                rect = pygame.rect.Rect((724+(138*x),200+(40*y)), (134, 38))
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
        #BACK BUTTON
        rect = pygame.rect.Rect((862,140), (134, 38))
        if self.theLoop.mousePressed == button: self.theLoop.screen.blit(self.theLoop.on, rect)
        else: self.theLoop.screen.blit(self.theLoop.off, rect)
        self.displayButtonText(False, button, rect)
        button = button + 1
        #FRAME CONTROL BUTTONS
        for x in range(0,3):
            rect = pygame.rect.Rect((60+(40*x),650), (36, 36))
            if self.theLoop.mousePressed == button: self.theLoop.screen.blit(self.theLoop.framecontrol[1][x], rect)
            else: self.theLoop.screen.blit(self.theLoop.framecontrol[0][x], rect)
            button = button + 1
            
        self.displayDelIcons()
        self.displayObjectIcons()
        self.displayColliderIcons()
        self.displayFrameIcons()
        self.displayPartViewer()
        self.displayText()
            
    def displayDelIcons(self):
        for i in range (0,2):
            rect = pygame.rect.Rect((50+(i*40), 75), (36, 36))
            self.theLoop.screen.blit(self.theLoop.framecontrol[0][2], rect)
            
    def displayObjectIcons(self):
        if self.currentFrame != -1:
            counter = 0
            for object in self.animation.frames[self.currentFrame].objects:
                rect = pygame.rect.Rect((90, 115+(counter*40)), (36, 36))
                self.displayObjectIcon(self.theLoop.screen, counter, rect)
                counter += 1
                
    def displayColliderIcons(self):
        if self.currentFrame != -1:
            counter = 0
            for collider in self.animation.frames[self.currentFrame].colliders:
                rect = pygame.rect.Rect((50, 115+(counter*40)), (36, 36))
                self.displayColliderIcon(self.theLoop.screen, counter, rect)
                counter += 1
            
    def displayFrameIcons(self):
        counter = 0
        for frame in self.animation.frames:
            rect = pygame.rect.Rect((180+(counter*40), 650), (36, 36))
            self.displayIcon(self.theLoop.screen, frame, rect)
            counter += 1

    def displayPartViewer(self):    
        self.theLoop.screen.blit(self.partBG, self.partviewerRect)
        self.partBlitter()
        self.theLoop.screen.blit(self.theLoop.partframe, self.partviewerRect)
            
    def partBlitter(self):
        objects = self.theLoop.modes[1].clipObjects
        object = objects[self.currentPart]
        rect = object.textures[self.currentPartZoom].get_rect()
        rect.center = self.partviewerRect.center
        self.theLoop.screen.blit(object.textures[self.currentPartZoom], rect)
            
    def displayText(self):
        if self.currentTool == 0: self.theLoop.displayText("CURRENTTOOL: None", (930,120))
        elif self.currentTool == TOOLTYPE['COLLIDER']: self.theLoop.displayText("CURRENTTOOL: Collider Rect", (930,120))
        elif self.currentTool == TOOLTYPE['HANDPOS']: self.theLoop.displayText("CURRENTTOOL: Hand Position", (930,120))
        elif self.currentTool == TOOLTYPE['BOUNDBOX']: self.theLoop.displayText("CURRENTTOOL: Bounding Box", (930,120))
        elif self.currentTool == TOOLTYPE['PLACER']: self.theLoop.displayText("CURRENTTOOL: Place Object", (930,120))
        
        string = "ANIM: Name:"+self.animation.name
        string += ", Frames:"+str(len(self.animation.frames))
        self.theLoop.displayText(string, (390,60))
        if self.animation.boundBox[0] != -1 and self.animation.boundBox[1] != -1:
            bounds = self.animation.boundBox
            dims = [(bounds[1][0] - bounds[0][0])+1, (bounds[1][1] - bounds[0][1])+1]
            string = "ImageDims:"+str(dims)
        else: string = "ImageDims:N/A"
        string += ", CollideDims:N/A"
        self.theLoop.displayText(string, (390,80))
        
        if self.currentFrame != -1: 
            string = "FRAME: "
            string += "Index:"+str(self.currentFrame)
            string += ", Number:"+str(self.animation.frames[self.currentFrame].number)
            string += ", HandPos:"+str(self.animation.frames[self.currentFrame].handPos)
            string += ", ObjCount:"+str(len(self.animation.frames[self.currentFrame].objects))
            self.theLoop.displayText(string, (390,635))
        else: self.theLoop.displayText("CURRENTFRAME: N/A", (390,635))
        
        objects = self.theLoop.modes[1].clipObjects
        object = objects[self.currentPart]
        self.theLoop.displayText("NAME: "+object.clipname+", ID: "+str(self.currentPart), (985,550))
        
        if self.currentFrame != -1 and self.currentObject != -1: 
            self.theLoop.displayText("OBJECT NAME: " + self.animation.frames[self.currentFrame].objects[self.currentObject].name, (930,590))
            string = "INDEX: " + str(self.currentObject)
            string += ", TYPE: " + str(self.animation.frames[self.currentFrame].objects[self.currentObject].type)
            string += ", CLIP: " + str(objects[self.animation.frames[self.currentFrame].objects[self.currentObject].type].clipname)
            self.theLoop.displayText(string, (930,610))
            string = "POS: " + str(self.animation.frames[self.currentFrame].objects[self.currentObject].pos)
            string += ", ROT: " + str(self.animation.frames[self.currentFrame].objects[self.currentObject].rot)
            string += ", LAYER: " + str(self.animation.frames[self.currentFrame].objects[self.currentObject].layer)
            self.theLoop.displayText(string, (930,630))
        else: self.theLoop.displayText("CURRENTOBJECT: N/A", (930,590))

    def displayIcon(self, screen, current, rect):
        if current == self.currentFrame: screen.blit(self.theLoop.buton, rect)
        else: screen.blit(self.theLoop.butoff, rect)     
        
    def displayObjectIcon(self, screen, current, rect):
        if current == self.currentObject: screen.blit(self.theLoop.buton, rect)
        else: screen.blit(self.theLoop.butoff, rect)
        
    def displayColliderIcon(self, screen, current, rect):
        if current == self.currentCollider: screen.blit(self.theLoop.buton, rect)
        else: screen.blit(self.theLoop.butoff, rect)
        
    def displayButtonText(self, type, button, rect):
        if type: string = MODETEXT[button]
        else: string = BUTTONTEXT[button]
        image = self.theLoop.font.render(string, 1, (0, 0, 0))
        imagerect = image.get_rect()
        imagerect.center = rect.center
        self.theLoop.screen.blit(image, imagerect)
        
########################################################################################
########################################################################################
#########################################INPUT##########################################
########################################################################################
########################################################################################
        
    def checkButtonPress(self):
        if self.currentTool != 0:
            if self.theLoop.viewport.collidepoint(self.theLoop.mousePos): 
                pixelSpot = self.getPixelOnViewport()
                self.runToolAction(pixelSpot)
    
        #ACTION BUTTONS
        button = 0
        for y in range (0,4):
            for x in range(0,3):
                rect = pygame.rect.Rect((724+(138*x),200+(40*y)), (134, 38))
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
        #BACK BUTTON
        rect = pygame.rect.Rect((862,140), (134, 38))
        if rect.collidepoint(self.theLoop.mousePos): 
            self.theLoop.mousePressed = button
        button = button+1
        #FRAME CONTROL BUTTONS
        for x in range(0,3):
            rect = pygame.rect.Rect((60+(40*x),650), (36, 36))
            if rect.collidepoint(self.theLoop.mousePos): 
                self.theLoop.mousePressed = button
                break
            button = button+1
        #FRAME BUTTONS
        counter = 0
        for frame in self.animation.frames:
            y = 650
            x = counter*40
            rect = pygame.rect.Rect((180+x, y), (36, 36))
            if rect.collidepoint(self.theLoop.mousePos):
                self.currentFrame = frame
                self.currentObject = -1
                self.currentCollider = -1
                break
            counter += 1
        #DELETE BUTTONS
        for i in range (0,2):
            rect = pygame.rect.Rect((50+(i*40), 75), (36, 36))
            if rect.collidepoint(self.theLoop.mousePos):
                if i == 0 and self.currentCollider != -1: 
                    del self.animation.frames[self.currentFrame].colliders[self.currentCollider]
                    self.currentCollider = -1
                elif i == 1 and self.currentObject != -1: 
                    del self.animation.frames[self.currentFrame].objects[self.currentObject]
                    self.currentObject = -1
        #OBJECT BUTTONS
        if self.currentFrame != -1:
            counter = 0
            for object in self.animation.frames[self.currentFrame].objects:
                rect = pygame.rect.Rect((90, 115+(counter*40)), (36, 36))
                if rect.collidepoint(self.theLoop.mousePos):
                    self.currentObject = counter
                    break
                counter += 1
        #COLLIDER BUTTONS
        if self.currentFrame != -1:
            counter = 0
            for collider in self.animation.frames[self.currentFrame].colliders:
                rect = pygame.rect.Rect((50, 115+(counter*40)), (36, 36))
                if rect.collidepoint(self.theLoop.mousePos):
                    if self.currentCollider == counter: self.currentCollider = -1
                    else: self.currentCollider = counter
                    break
                counter += 1
                
    def checkButtonRelease(self):
        self.theLoop.mousePressed = -1
        #ACTION BUTTONS
        button = 0
        for y in range (0,4):
            for x in range(0,3):
                rect = pygame.rect.Rect((724+(138*x),200+(40*y)), (134, 38))
                if rect.collidepoint(self.theLoop.mousePos): 
                    self.toolReset()
                    self.buttonPressed(button)
                    break
                button = button+1
        for y in range (0,2):
            rect = pygame.rect.Rect((724,457+(40*y)), (134, 38))
            if rect.collidepoint(self.theLoop.mousePos):
                self.toolReset()
                self.buttonPressed(button)
                break
            button = button+1
        #BACK BUTTON
        rect = pygame.rect.Rect((862,140), (134, 38))
        if rect.collidepoint(self.theLoop.mousePos):
            self.toolReset()
            self.buttonPressed(button)
        button = button+1
        #FRAME CONTROL BUTTONS
        for x in range(0,3):
            rect = pygame.rect.Rect((60+(40*x),650), (36, 36))
            if rect.collidepoint(self.theLoop.mousePos): 
                self.toolReset()
                self.buttonPressed(button)
                break
            button = button+1
        
    def buttonPressed(self, button):
        if button == 0: self.theLoop.saveAnimation()
        elif button == 1: self.renameObjectPressed()
        elif button == 2: self.changeBackgroundColor()
        elif button == 3: self.onionSkinPressed()
        elif button == 4: self.rotatePartPressed()
        elif button == 5: self.controlZoom(True)
        elif button == 6: self.setColliderPressed()
        elif button == 7: self.setHandPosPressed()
        elif button == 8: self.controlZoom(False)
        elif button == 9: self.setBoundBoxPressed()
        elif button == 10: self.setLayerPressed()
        elif button == 11: pass #N/A
        elif button == 12: self.switchPart()
        elif button == 13: self.choosePart()
        elif button == 14: self.theLoop.currentMode = 1
        elif button == 15: self.playAnimation()
        elif button == 16: self.createNewFrame()
        elif button == 17: self.deleteFrame()
        
    def rightClickPressed(self):
        self.toolReset()
    
    def toolReset(self):
        if self.currentTool == TOOLTYPE['BOUNDBOX']:
            self.animation.boundBox = self.oldData
            self.oldData = None
        if self.currentTool == TOOLTYPE['COLLIDER']:
            collider = self.animation.frames[self.currentFrame].colliders[-1]
            if collider[0] == -1 or collider[1] == -1: del collider
        self.currentTool = 0
        
########################################################################################
########################################################################################
########################################ACTIONS#########################################
########################################################################################
########################################################################################

    def runToolAction(self, pixelspot):
        if self.currentTool == TOOLTYPE['BOUNDBOX']:
            if self.animation.boundBox[0] == -1:
                self.animation.boundBox[0] = pixelspot
            else:
                if self.animation.boundBox[1] == -1:
                    self.animation.boundBox[1] = pixelspot
                    self.currentTool = 0
        elif self.currentTool == TOOLTYPE['COLLIDER']:
            collider = self.animation.frames[self.currentFrame].colliders[-1]
            if collider[0] == -1:
                collider[0] = pixelspot
            else:
                if collider[1] == -1:
                    collider[1] = pixelspot
                    self.currentTool = 0
        elif self.currentTool == TOOLTYPE['PLACER']:
            frame = self.animation.frames[self.currentFrame]
            frame.objects.append(FrameObject())
            object = frame.objects[-1]
            object.name = self.theLoop.modes[1].clipObjects[self.currentPart].clipname
            object.type = self.currentPart
            object.pos = pixelspot
            object.rot = 0
            object.layer = 0   
        elif self.currentTool == TOOLTYPE['HANDPOS']:
            handLayer = self.theLoop.windowObject.inputWindow(self.theLoop.screen, "Enter Layer: ")
            if self.is_number(handLayer): 
                self.animation.frames[self.currentFrame].handPos = []
                self.animation.frames[self.currentFrame].handPos.append(pixelspot[0])
                self.animation.frames[self.currentFrame].handPos.append(pixelspot[1])
                self.animation.frames[self.currentFrame].handPos.append(int(handLayer))
            else: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "INVALID LAYER")
        
    def setColliderPressed(self):
        if self.currentFrame != -1:
            self.currentTool = TOOLTYPE['COLLIDER']
            self.animation.frames[self.currentFrame].colliders.append([-1,-1])
        
    def setHandPosPressed(self):
        if self.currentFrame != -1:
            self.currentTool = TOOLTYPE['HANDPOS']
            self.animation.frames[self.currentFrame].handPos = -1
        
    def setBoundBoxPressed(self):
        self.currentTool = TOOLTYPE['BOUNDBOX']
        self.oldData = self.animation.boundBox
        self.animation.boundBox = [-1,-1]
        
    def setLayerPressed(self):
        if self.currentObject != -1:
            object = self.animation.frames[self.currentFrame].objects[self.currentObject]
            newLayer = self.theLoop.windowObject.inputWindow(self.theLoop.screen, "Enter Angle: ")
            if self.is_number(newLayer): 
                self.animation.frames[self.currentFrame].objects[self.currentObject].layer = int(newLayer) 
            else: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "INVALID LAYER")
        
    def rotatePartPressed(self):
        if self.currentObject != -1:
            object = self.animation.frames[self.currentFrame].objects[self.currentObject]
            newAngle = self.theLoop.windowObject.inputWindow(self.theLoop.screen, "Enter Angle: ")
            if self.is_number(newAngle): 
                self.animation.frames[self.currentFrame].objects[self.currentObject].rot = int(newAngle) 
            else: self.theLoop.promptObject.promptWindow(self.theLoop.screen, "INVALID ANGLE")

    def renameObjectPressed(self):
        object = self.animation.frames[self.currentFrame].objects[self.currentObject]
        newName = self.theLoop.windowObject.inputWindow(self.theLoop.screen, "Enter Name: ")
        if newName != "": object.name = newName

    def onionSkinPressed(self):
        self.onionSkinState = not self.onionSkinState
        
    def switchPart(self):
        self.currentPart += 1
        if self.currentPart >= len(self.theLoop.modes[1].clipObjects): self.currentPart = 0
        
    def choosePart(self):
        if self.currentFrame != -1:
            self.currentTool = TOOLTYPE['PLACER']

    def controlZoom(self, type):
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            if self.currentPartZoom < ZOOMS-1 and type: self.currentPartZoom += 1
            elif self.currentPartZoom > 0 and not type: self.currentPartZoom -= 1
        else:
            if self.currentZoom < ZOOMS-1 and type: self.currentZoom += 1
            elif self.currentZoom > 0 and not type: self.currentZoom -= 1
        
    def changeBackgroundColor(self):
        self.bgfillID += 1
        if self.bgfillID == len(BGRNDCOLORS): self.bgfillID = 0
        self.bgfill = pygame.Surface([488, 489])
        self.bgfill = self.bgfill.convert()
        self.bgfill.fill(BGRNDCOLORS[self.bgfillID])
        self.partBG = pygame.Surface([242,137])
        self.partBG = self.partBG.convert()
        self.partBG.fill(BGRNDCOLORS[self.bgfillID])
        
    def playAnimation(self):
        pass
        
    def createNewFrame(self):
        if len(self.animation.frames) < 25:
            self.animation.frameCounter += 1
            self.animation.frames[self.animation.frameCounter] = Frame()
            
    def deleteFrame(self):
        if self.currentFrame != -1:
            del self.animation.frames[self.currentFrame]
            self.currentFrame = -1

#################################################################################
        
    def rot_center(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
            
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
            
    def defineLayerOrder(self, frame):
        tempdict = {}
        for object in self.animation.frames[frame].objects:
            tempdict[object] = object.layer
        self.animation.frames[frame].layerOrder = sorted(tempdict.items(), key=operator.itemgetter(1))
            
    def getPixelOnViewport(self):
        if self.currentZoom == 0: scrollOffset = [0,0]
        else: scrollOffset = [self.viewOffset[0]*(self.currentZoom+1), self.viewOffset[1]*(self.currentZoom+1)]
        mp = [self.theLoop.mousePos[0]-scrollOffset[0], self.theLoop.mousePos[1]-scrollOffset[1]]
        vp = self.theLoop.viewport
        pixelspot = [mp[0]-vp.x, mp[1]-vp.y]
        scaledspot = [pixelspot[0]/(self.currentZoom+1), pixelspot[1]/(self.currentZoom+1)]
        return scaledspot
            
    def scrollViewport(self):
        if self.currentZoom != 0:
            if( pygame.key.get_pressed()[pygame.K_UP] != 0 ):
                if self.viewOffset[1] < 0: self.viewOffset[1] += 1
            if( pygame.key.get_pressed()[pygame.K_DOWN] != 0 ):
                self.viewOffset[1] -= 1
            if( pygame.key.get_pressed()[pygame.K_LEFT] != 0 ):
                if self.viewOffset[0] < 0: self.viewOffset[0] += 1
            if( pygame.key.get_pressed()[pygame.K_RIGHT] != 0 ):
                self.viewOffset[0] -= 1
                
    def trackMouse(self):
        if self.currentFrame != -1 and self.currentObject != -1:
            if self.theLoop.viewport.collidepoint(self.theLoop.mousePos): 
                if( pygame.key.get_pressed()[pygame.K_SPACE] != 0 ):
                    if self.dragEnabled == False:
                        self.dragEnabled = True
                        self.oldDrag = self.getPixelOnViewport()
                    else: 
                        newDrag = self.getPixelOnViewport()
                        if newDrag != self.oldDrag:
                            object = self.animation.frames[self.currentFrame].objects[self.currentObject]
                            diff = [newDrag[0]-self.oldDrag[0], newDrag[1]-self.oldDrag[1]]
                            object.pos = [object.pos[0]+diff[0], object.pos[1]+diff[1]]
                            self.oldDrag = newDrag
                else:
                    if self.dragEnabled == True:
                        self.dragEnabled = False
        
#################################################################################
            
class Frame:
    def __init__(self):
        self.number = None
        self.handPos = -1
        self.objects = []
        self.layerOrder = []
        self.colliders = []
        
class FrameObject:
    def __init__(self):
        self.name = ""
        self.type = None
        self.pos = None
        self.rot = 0
        self.layer = None