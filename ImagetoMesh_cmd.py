import rhinoscriptsyntax as rs
import System.Drawing
import os
import Rhino
import math
import imgtomeshsetup
import imgtomeshweighting
import imgtomeshpreview
import scriptcontext

pathlist = []
imglist = []
imgweights = []
createImage = False
vertices = []
capVertices = []
faceVertices = []
zlist = []
previewcolors = []

__commandname__ = "ImagetoMesh"

def RunCommand( is_interactive ):
  main()
  return 0



##Load Images
def loadImages(images):
    scriptcontext.sticky["imgpath"] = 0
    ##for each image in range defined by user, 
    for num in range(images):
        ##get file path
        path = rs.OpenFileName("Open base image (.PNG or .JPG")
        if path == None:
            break
        if path:
            #add path to list for weighting
            pathlist.append(path)
            print path
            scriptcontext.sticky["imgpath"] = path
            ##add image to list of system.drawing objects
            imglist.append(System.Drawing.Bitmap.FromFile(pathlist[num]))
            if num  == 0:
                ##check dimensions against first selected image before opening weighting window
                safedimensions = (imglist[num].Width == imglist[0].Width) or (imglist[num].Height == imglist[0].Height)
                if not(safedimensions):
                    print("Error: Image dimensions must all be the same")
                    break
            if (safedimensions):
                ##Get user input from ETO forms
                weightinput = imgtomeshweighting.WeightInput()
                window2 = weightinput.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
                weight = float(weightinput.GetWeight())
            imgweights.append(weight)

##Image Weighting
##for each pixel in the images, average the brightness value of all the pixels
##weighted based on user input
##then convert weighted brightness into a Z displacement
def WeightImages(outputdepth, images, imgweight):
    ##clear out scriptcontext before assigning dimensions from main function
    scriptcontext.sticky["imgwidth"] = 0
    scriptcontext.sticky["imgheight"] = 0
    width = imglist[0].Width
    height = imglist[0].Height
    scriptcontext.sticky["imgwidth"] = width
    scriptcontext.sticky["imgheight"] = height
    zmax = 0
    print imgweight


    for x in range(width):
        for y in range(height):
                #Walk through a pixel array with the dimensions of the input image 
                zsum = []
                total = 0
                for i in range(images):
                    #Walk through each image in the set and sum pixel values per index in the array
                    color = System.Drawing.Bitmap.GetPixel(imglist[i], x, y)
                    factor = imgweight[i] 
                    ##get image weight and multiply each pixel per image
                    r = int(color.R) * factor
                    g = int(color.G) * factor
                    b = int(color.B) * factor
                    #convert from RGB to perceived brightness
                    #percieved brightness determines z offset
                    #each pixel of the image represents a vertex of the output mesh
                    #referenced: https://www.w3.org/TR/AERT/#color-contrast
                    zsum.append(0.299*(r) + 0.587*(g) + 0.114*(b))
                    total = sum(zsum)/255 + 1
                    ##align all border edge vertices to 0 in world z
                    if (x == width-1):
                        total = 0
                    if (x == 0):
                        total = 0
                    if (y+1 == height):
                        total = 0
                    if (y == 0):
                        total = 0
                #store weighted pixels (z vectors based on outputdepth)
                zweighted = total*(outputdepth/images)
                #store weighted brightness values (0-255 to recreate RGB for previews)
                previewcolors.append(sum(zsum)/images)
                #list of z vectors for vertices 
                zlist.append(zweighted)
                #list of vertices from percieved brightness of pixels weighted based on user input
                vertices.append((x,y,zweighted))
                capVertices.append((x,y,0))


##Create Weighted Preview Image 
def previewImage():
    colors = previewcolors
    width = imglist[0].Width
    height = imglist[0].Height
    scriptcontext.sticky["previewimage"] = 0
    #create empty bitmap
    previewimage = System.Drawing.Bitmap(width,height)
    #for each pixel from the weighted list, write to the preview image
    for i in range(width):
        for j in range(height):
            val = 0
            val = colors[(j+(i*height))]
            val = int(val)
            #create a system color- really just luminosity
            color = System.Drawing.Color.FromArgb(val,val,val)
            previewimage.SetPixel(i,j,color)
    scriptcontext.sticky["previewimage"] = previewimage
    return True

##Create Mesh
def CreateMesh(outputdepth):
    width = imglist[0].Width
    height = imglist[0].Height
    ##get highest vertex Z factor for scaling mesh so we can compress or expand  
    ##the range of image brightness range to the correct output depth
    zmax = max(zlist)
    mesh = 0
    cap = 0
    ##create face vertices
    for x in range(height-1):
        for y in range(width-1):
            faceVertices.append(((x+y*height),(x+y*height)+1,(x+y*height)+height+1,(x+y*height)+height))
    rs.EnableRedraw(False)
    ##add mesh to Rhino document
    mesh = rs.AddMesh(vertices, faceVertices)
    cap = rs.AddMesh(capVertices, faceVertices)
    ctr = rs.CreatePoint(width/2, height/2, 0)

    ##Mirror Across Y and scale output mesh to correct depth
    rs.ScaleObject(mesh, ctr, [1, -1, outputdepth/zmax])
    rs.ScaleObject(cap, ctr, [1, -1, 1])
    mesh = rs.JoinMeshes([mesh, cap], True)
    rs.EnableRedraw(True)

## Main Function
def main():
    scriptcontext.sticky["imgcount"] = 0
    scriptcontext.sticky["depth"] = 0
    #run setup window
    userinput = imgtomeshsetup.UserInput()
    window1 = userinput.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (window1):
        #assign input from form 1
        images = int(userinput.GetCount())
        outputdepth = float(userinput.GetDepth())
        scriptcontext.sticky["imgcount"] = images
        scriptcontext.sticky["depth"] = outputdepth
        ##load images (runs window 2 for each image in the user input range)
        loadImages(images)
        polycount = ((imglist[0].Width-1) * (imglist[0].Height-1))
        scriptcontext.sticky["polycount"] = polycount
        ##weight images based on user input
        WeightImages(outputdepth, images, imgweights)
        ##create preview image system bitmap
        previewImage()
        ##run window 3 to preview image weighting before creating mesh
        finalpreview = imgtomeshpreview.FinalPreview()
        window3 = finalpreview.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
        if (window3):
            ##check if you clicked create mesh
            if scriptcontext.sticky.has_key("createMesh"):
                if (scriptcontext.sticky["createMesh"]):
                    CreateMesh(outputdepth)
                    print "output depth =",outputdepth, "weights =", imgweights, " image count =", images
    scriptcontext.sticky["imgcount"] = 0
    scriptcontext.sticky["depth"] = 0
    scriptcontext.sticky["previewimage"] = 0
    scriptcontext.sticky["imgwidth"] = 0
    scriptcontext.sticky["imgheight"] = 0

if __name__ == "__main__":
    main()
