import pygame

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3
MOUSE_WUP = 4
MOUSE_WDOWN = 5

class InputWindow:
    def __init__(self, images):
        self.font = images.font
        self.prompt = images.prompt
        self.promptRect = pygame.rect.Rect((0, 0), (259, 155))
        self.promptRect.center = (1280/2, 720/2)
    
    def inputWindow(self, screen, request):
        inputLoop = True
        inputString = ""
        while inputLoop:
            screen.blit(self.prompt, self.promptRect)
            values = self.runTextBox(inputString, 12)
            inputString = values[0]
            self.displayInput(screen, inputString, request)
            pygame.display.flip()
            if values[1] == False: inputLoop = False
        return inputString
        
    def displayInput(self, screen, string, request):
        image = self.font.render(string, 1, (0, 0, 0))
        imagerect = image.get_rect()
        imagerect.center = self.promptRect.center
        imagerect.y += 15
        screen.blit(image, imagerect)
        
        image = self.font.render(request, 1, (0, 0, 0))
        imagerect = image.get_rect()
        imagerect.center = self.promptRect.center
        imagerect.y -= 15
        screen.blit(image, imagerect)
        
    def runTextBox(self, string, charlimit):
        inputLoop = True
        nextInput = ""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: inputLoop = False
                elif event.key == pygame.K_RETURN: inputLoop = False
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE: 
                    if len(string) > 0: string = string[:-1]
                #elif event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD: nextInput = "."
                elif event.key == pygame.K_0 or event.key == pygame.K_KP0: nextInput = "0"
                elif event.key == pygame.K_1 or event.key == pygame.K_KP1: nextInput = "1"
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2: nextInput = "2"
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3: nextInput = "3"
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4: nextInput = "4"
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5: nextInput = "5"
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6: nextInput = "6"
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7: nextInput = "7"
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8: nextInput = "8"
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9: nextInput = "9"
                #elif event.key == pygame.K_SPACE: nextInput = " "
                elif event.key == pygame.K_a: nextInput = "A"
                elif event.key == pygame.K_b: nextInput = "B"
                elif event.key == pygame.K_c: nextInput = "C"
                elif event.key == pygame.K_d: nextInput = "D"
                elif event.key == pygame.K_e: nextInput = "E"
                elif event.key == pygame.K_f: nextInput = "F"
                elif event.key == pygame.K_g: nextInput = "G"
                elif event.key == pygame.K_h: nextInput = "H"
                elif event.key == pygame.K_i: nextInput = "I"
                elif event.key == pygame.K_j: nextInput = "J"
                elif event.key == pygame.K_k: nextInput = "K"
                elif event.key == pygame.K_l: nextInput = "L"
                elif event.key == pygame.K_m: nextInput = "M"
                elif event.key == pygame.K_n: nextInput = "N"
                elif event.key == pygame.K_o: nextInput = "O"
                elif event.key == pygame.K_p: nextInput = "P"
                elif event.key == pygame.K_q: nextInput = "Q"
                elif event.key == pygame.K_r: nextInput = "R"
                elif event.key == pygame.K_s: nextInput = "S"
                elif event.key == pygame.K_t: nextInput = "T"
                elif event.key == pygame.K_u: nextInput = "U"
                elif event.key == pygame.K_v: nextInput = "V"
                elif event.key == pygame.K_w: nextInput = "W"
                elif event.key == pygame.K_x: nextInput = "X"
                elif event.key == pygame.K_y: nextInput = "Y"
                elif event.key == pygame.K_z: nextInput = "Z"
                #elif event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD: nextInput = "."
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS: nextInput = "-"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_LEFT: pass
                elif event.button == MOUSE_RIGHT: pass
                elif event.button == MOUSE_MIDDLE: pass
                elif event.button == MOUSE_WUP: pass
                elif event.button == MOUSE_WDOWN: pass
            elif event.type == pygame.QUIT: inputLoop = False
        if nextInput != "" and len(string) <= charlimit-1: string += nextInput
        dict = {0:string, 1:inputLoop}
        return dict