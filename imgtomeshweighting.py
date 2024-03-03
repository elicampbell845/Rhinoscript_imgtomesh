import rhinoscriptsyntax as rs
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import imgtomeshsetup
import ImagetoMesh_cmd
global images
import scriptcontext
import System.Drawing


class WeightInput(forms.Dialog[bool]):
    def __init__(self):
        ##Eto form layout
        self.Title = "Image Weighting"
        self.Padding = drawing.Padding(10)
        self.Resizable = True
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        self.image_view = forms.ImageView()
        self.image_view = forms.ImageView()
        self.DefaultButton = forms.Button(Text = "OK")
        self.DefaultButton.Click += self.OnOKButtonClick
        self.AbortButton = forms.Button(Text = "Cancel")
        self.AbortButton.Click += self.OnCloseButtonClick
        self.LoadButton = forms.Button(Text = "Cancel")
        self.LoadButton.Click += self.OnLoadButtonClick
        self.weightinputlabel = forms.Label(Text = "Enter image weight from 0.0 to 1.0")
        self.weightinput = forms.TextBox(Text = "1")
        path = ""
        ##get image image attributes and preview image
        if scriptcontext.sticky.has_key("imgpath"):
            path = scriptcontext.sticky["imgpath"]
            img = System.Drawing.Bitmap(path)
            width = int(img.Width)
            height = int(img.Height)
            dimensions = []
            dimensions.append(width)
            dimensions.append(height)
            longestside = int(max(dimensions))
            maxsize = 800
            width = width * maxsize/longestside
            height = height * maxsize/longestside
            resizedimg = Rhino.UI.EtoExtensions.ToEto(System.Drawing.Bitmap(img, width, height))
            self.image_view.Image = resizedimg
        ##add image to form and default buttons
        layout.AddRow(self.image_view.Image)
        layout.AddRow(None)
        layout.AddRow(self.weightinput, self.weightinputlabel)
        layout.AddRow(None)
        layout.AddRow(self.DefaultButton, self.AbortButton)
        self.Content = layout
    def GetWeight(self):
        return self.weightinput.Text
    def OnCloseButtonClick(self, sender, e):
        if self.weightinput == "":
            self.Close(False)
        if self.weightinput:
            self.Close(True)
    def OnOKButtonClick(self, sender, e):
        self.Close(True)
    def OnLoadButtonClick(self, sender, e):
            getPath()
            self.Close(True)

def WeightInputWindow():
    weightinput = WeightInput()
    window2 = weightinput.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (window2):
        imgweight = weightinput.GetWeight()
        print imgweight
        return imgweight

if __name__ == "__main__":
    WeightInputWindow()


