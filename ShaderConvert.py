import pymel.core
from pymel.core import windows, system, general, language

class ShaderConvert():
    def __init__(self):
        self.initVars()
        self.initGUI()
        
    def initVars(self):
        self.shaderSelection = ["Blinn","Phong","Lambert"]
        
        self.selectedShaderFrom = 1
        self.selectedShaderTo = 0
        
        self.shaderFrom = "Phong"
        self.shaderTo = "Blinn"
    
    def refreshUI(self):
        windows.optionMenu("ShaderConvertFromMaterial", e = True, sl = self.selectedShaderFrom + 1)
        windows.optionMenu("ShaderConvertToMaterial", e = True, sl = self.selectedShaderTo + 1)
    
    def selectNewShaderFrom(self, index):
        self.selectedShaderFrom = index
        self.refreshUI()
    
    def selectNewShaderTo(self, index):
        self.selectedShaderTo = index
        self.refreshUI()
    
    def getSelectedShaderFrom(self):
        return self.shaderSelection[self.selectedShaderFrom]

    def getSelectedShaderTo(self):
        return self.shaderSelection[self.selectedShaderTo]
    
    def initGUI(self):
        if windows.window("ShaderConvertWindow", exists=True):
            windows.deleteUI("ShaderConvertWindow")
        if windows.windowPref("ShaderConvertWindow", exists=True):
            windows.windowPref("ShaderConvertWindow", remove=True)
        windows.window("ShaderConvertWindow", t = "Shader Convert", sizeable = False)
        
        
        self.addOuterPadding(5, 5)
        windows.frameLayout(l='Shader Convert')
        windows.columnLayout()
        windows.rowLayout(nc = 2)
        windows.optionMenu("ShaderConvertFromMaterial", l = "From", cc = lambda x: self.selectNewShaderFrom(int(windows.optionMenu("ShaderConvertFromMaterial", q = True, sl = True))-1), w = 125)
        windows.optionMenu("ShaderConvertToMaterial", l = "To",  cc = lambda x: self.selectNewShaderTo(int(windows.optionMenu("ShaderConvertToMaterial", q = True, sl = True))-1), w = 125)
        windows.setParent(u = True)

        for s in self.shaderSelection:
            windows.menuItem(l = s, p = "ShaderConvertFromMaterial")
            windows.menuItem(l = s, p = "ShaderConvertToMaterial")
                    
        windows.button(l = "Convert", w=250, command = lambda x: self.convertShaders())
        windows.setParent(u = True)
        windows.setParent(u = True)
        self.returnOuterPadding(5, 5)
        
        self.refreshUI()
        
        windows.showWindow()
    
    def convertShaders(self):
        #First, get all the shaders of type
        allShaders = general.ls(mat = True)
        Shaders = []
        if self.getSelectedShaderFrom()!=self.getSelectedShaderTo():
            if len(allShaders)>0:
                for shader in allShaders:
                    if general.nodeType(shader) == self.getSelectedShaderFrom().lower() and "initialShadingGroup" not in general.listConnections(shader):
                        Shaders.append(shader)
                
                if len(Shaders)>0:
                    for shader in Shaders:
                        newName = shader.replace(self.getSelectedShaderFrom().lower(), self.getSelectedShaderTo().lower())
                        newShader = general.createNode(self.getSelectedShaderTo().lower())
                        language.mel.eval('replaceNode "%s" "%s";'%(shader, newShader))
                        general.delete(shader)
                        general.rename(newShader,newName)
        
        
    def addOuterPadding(self, hpadding=0, vpadding=0):
        windows.columnLayout()
        windows.separator(h = hpadding, style = "none")
        windows.rowLayout(nc=3)
        windows.separator(w = vpadding, style = "none")
    
    def returnOuterPadding(self, hpadding=0, vpadding=0):
        windows.separator(w = hpadding, style = "none")
        windows.setParent(u=True)
        windows.separator(h = vpadding, style = "none")
        windows.setParent(u=True)