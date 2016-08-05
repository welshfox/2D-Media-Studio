import os
import cPickle as pickle

from MessagePrompt import PromptWindow

class ProjectObject:
    def __init__(self, name, images):
        self.projectPath = name
        self.models = {}
        self.objects = {}
        self.guis = {}
        self.modules = {0: self.models, 1: self.objects, 2:self.guis}
        
        self.promptObject = PromptWindow(images)
        
    def getModuleQty(self, type):
        return len(self.modules[type])
        
    def addModule(self, type, string):
        self.modules[type][string] = string
        
    def delModule(self, type, string):
        del self.modules[type][string]
        
    def saveProject(self):
        if os.path.isdir("../Projects/" + self.projectPath):
            saveData = {"name": self.projectPath, "models": self.models, "objects": self.objects, "guis": self.guis}
            pickle.dump( saveData, open( "../Projects/" + self.projectPath + "/projectData.p", "wb" ) )
    
    def loadProject(self):
        if os.path.isdir("../Projects/" + self.projectPath):
            if os.path.exists("../Projects/" + self.projectPath + "/projectData.p"):
                saveData = pickle.load( open( "../Projects/" + self.projectPath + "/projectData.p", "rb" ) )
                self.projectPath = saveData["name"]
                self.models = saveData["models"]
                self.objects = saveData["objects"]
                self.guis = saveData["guis"]
                self.modules = {0: self.models, 1: self.objects, 2:self.guis}
            else: self.saveProject()
            
    def validateModules(self, screen):
        markedDelete = []
        for model in self.models:
            if not os.path.isdir("../Projects/" + self.projectPath + "/Models/" + model):
                self.promptObject.promptWindow(screen, model + " Model Missing")
                markedDelete.append({"type": 0, "name": model})
        for object in self.objects:
            if not os.path.isdir("../Projects/" + self.projectPath + "/Objects/" + object):
                self.promptObject.promptWindow(screen, object + " Object Missing")
                markedDelete.append({"type": 1, "name": object})
        for gui in self.guis:
            if not os.path.isdir("../Projects/" + self.projectPath + "/GUIs/" + gui):
                self.promptObject.promptWindow(screen, gui + " GUI Missing")
                markedDelete.append({"type": 2, "name": gui})
        for item in markedDelete:
            self.delModule(item["type"], item["name"])
        self.saveProject()