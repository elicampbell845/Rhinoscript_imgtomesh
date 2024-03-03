import rhinoscriptsyntax as rs
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import imgtomeshsetup
import ImagetoMesh_cmd
global images
import scriptcontext
import System.Drawing

width = 0
height = 0
previewimage = 0

##Forms/UI 

class FinalPreview(forms.Dialog[bool]):
    def __init__(self):
        
        scriptcontext.sticky["createMesh"] = 0
        if scriptcontext.sticky.has_key("imgwidth"):
            width = scriptcontext.sticky["imgwidth"]
        if scriptcontext.sticky.has_key("imgheight"):
            height = scriptcontext.sticky["imgheight"]
            previewimage = System.Drawing.Bitmap(width, height) 
        ##Eto form layout
        self.Title = "Image Weighting Preview"
        self.Padding = drawing.Padding(10)
        self.Resizable = False
        self.DefaultButton = forms.Button(Text = "Create Mesh")
        self.DefaultButton.Click += self.OnOKButtonClick
        self.AbortButton = forms.Button(Text = "Cancel")
        self.AbortButton.Click += self.OnCloseButtonClick
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        self.image_view = forms.ImageView()
        if scriptcontext.sticky.has_key("previewimage"):
            previewimage = scriptcontext.sticky["previewimage"]
            if scriptcontext.sticky.has_key("polycount"):
                polycount = scriptcontext.sticky["polycount"]
                width = previewimage.Width
                height = previewimage.Height
                dimensions = []
                dimensions.append(width)
                dimensions.append(height)
                longestside = int(max(dimensions))
                maxsize = 800
                ##scale image to fit max size
                width = width * maxsize/longestside
                height = height * maxsize/longestside
                ##Convert scaled image to eto image format from system drawing
                resizedimg = Rhino.UI.EtoExtensions.ToEto(System.Drawing.Bitmap(previewimage, width, height))
                self.image_view.Image = resizedimg
                layout.AddRow(self.image_view.Image)
        layout.AddRow("Final poly count=", str(polycount))
        layout.AddRow(None)
        layout.AddRow(self.DefaultButton, self.AbortButton)
        self.Content = layout
    def OnCloseButtonClick(self, sender, e):
        createMesh = False
        scriptcontext.sticky["createMesh"] = createMesh
        self.Close(False)

    def OnOKButtonClick(self, sender, e):
        if previewimage == None:
            createMesh = False
            scriptcontext.sticky["createMesh"] = createMesh
            self.Close(False)
        else:
            createMesh = True
            scriptcontext.sticky["createMesh"] = createMesh
            self.Close(True)
            
def FinalPreviewWindow():
    finalpreview = FinalPreview()
    window3 = finalpreview.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (window3):
        return True

if __name__ == "__main__":
    FinalPreviewWindow()


