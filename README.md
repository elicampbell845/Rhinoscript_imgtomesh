# Rhinoscript_imgtomesh

Image to Mesh 1.0.0.6
Eli Campbell 2024
RhinoPython Plugin

Description:

Image to mesh is a RhinoPython plugin that converts bitmap images into a mesh in Rhino. Pixel brightness gets mapped into Z displacement. The script will average multiple images together based on brightness per pixel, but all images used must have the same dimensions. Images larger than 1000 pixels in X or Y will produce meshes with a high polygon count. 

This tool is good for producing a pre-sculpt mesh for programs like ZBrush, Meshmixer or Blender. Performing planar intersections on the mesh can be useful for vector tracing, but curves need to be rebuilt and optimized. Higher resolution means more pixel interpolation artifacts/quads in the mesh. Best bet is to try images at different resolutions until you get satifactory results.

Instructions:

1. Use the "RunPythonScript" Command in Rhino
2. Select "ImagetoMesh_cmd.py"
3. Enter a number of images and an output depth. 
4. After selecting images, wait for preview to appear. Press Ok to create mesh.

