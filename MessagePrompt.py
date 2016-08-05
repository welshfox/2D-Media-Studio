import pygame

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3
MOUSE_WUP = 4
MOUSE_WDOWN = 5

class PromptWindow:
    def __init__(self, images):
        self.font = images.font
        self.prompt = images.prompt
        self.promptRect = pygame.rect.Rect((0, 0), (259, 155))
        self.promptRect.center = (1280/2, 720/2)
    
    def promptWindow(self, screen, string):
        promptLoop = True
        while promptLoop:
            screen.blit(self.prompt, self.promptRect)
            promptLoop = self.runInput()
            self.displayText(screen, string, self.promptRect.center)
            pygame.display.flip()
        
    def runInput(self):
        promptLoop = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: promptLoop = False
                elif event.key == pygame.K_RETURN: promptLoop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT: pass
                elif event.button == MOUSE_RIGHT: pass
                elif event.button == MOUSE_MIDDLE: pass
                elif event.button == MOUSE_WUP: pass
                elif event.button == MOUSE_WDOWN: pass
            elif event.type == pygame.QUIT: promptLoop = False
        return promptLoop
        
    def displayText(self, screen, text, center):
        color = {0:(0,0,0),1:(255,255,255)}
        for i in range(0,2):
            point = [center[0]-(i*3), center[1]-(i*3)]
            image = self.font.render(text, 1, color[i])
            imagerect = image.get_rect()
            imagerect.center = point
            screen.blit(image, imagerect)