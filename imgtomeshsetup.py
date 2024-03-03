import rhinoscriptsyntax as rs
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import ImagetoMesh_cmd
import scriptcontext

##Forms/UI 

class UserInput(forms.Dialog[bool]):
    def __init__(self):
        ##Eto form layout
        self.Title = "Images to Mesh Setup 1.0.0.6"
        self.Padding = drawing.Padding(10)
        self.Resizable = False
        self.numimglabel = forms.Label(Text = "Enter number of images to weight:")
        self.numimginput = forms.TextBox(Text = "1")
        self.depthlabel = forms.Label(Text = "Enter mesh output depth:")
        self.depthinput = forms.TextBox(Text = "10")
        self.DefaultButton = forms.Button(Text = "OK")
        self.DefaultButton.Click += self.OnOKButtonClick
        self.AbortButton = forms.Button(Text = "Cancel")
        self.AbortButton.Click += self.OnCloseButtonClick
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)
        ##add user inputs for number of images and weight
        layout.AddRow(self.numimglabel, self.numimginput)
        layout.AddRow(None)
        layout.AddRow(self.depthlabel, self.depthinput)
        layout.AddRow(None)
        layout.AddRow(self.DefaultButton, self.AbortButton)
        self.Content = layout
    def GetCount(self):
        return self.numimginput.Text
    def GetWeight(self):
        return self.weightinput.Text
    def GetDepth(self):
        return self.depthinput.Text
    def OnCloseButtonClick(self, sender, e):
        self.depthinput.Text == ""
        self.numimginput.Text == ""
        self.Close(False)
    def OnOKButtonClick(self, sender, e):
        if self.depthinput == "":
            self.Close(False)
        if self.numimginput == "":
            self.Close(False)
        else:
            self.Close(True)

def UserInputWindow():
    userinput = UserInput()
    rc = userinput.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        outputdepth = userinput.GetDepth()
        images = userinput.GetCount()
        print images, outputdepth
        return images, outputdepth

if __name__ == "__main__":
    UserInputWindow()


##References"
##https://discourse.mcneel.com/t/update-eto-form-after-user-has-changed-input-data-using-the-eto-form-in-real-time/101206/3
##https://discourse.mcneel.com/t/addrows-for-a-dynamiclayout-using-a-for-loop-and-a-list-eto-forms/101073
##https://developer.rhino3d.com/guides/rhinopython/eto-forms-python/
##https://developer.rhino3d.com/guides/rhinopython/eto-layouts-python/