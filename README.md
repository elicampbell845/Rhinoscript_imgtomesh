# Rhinoscript_imgtomesh

Image to Mesh 1.0.0.6
Eli Campbell 2024
RhinoPython Plugin

Description:

Image to mesh is a plugin that converts bitmap images into a mesh in Rhino. Pixel brightness gets mapped into Z displacement. The script will average multiple images together based on brightness per pixel, but all images used must have the same dimensions. Keep in mind that images larger than 1000 pixels in either direction can take a long time and produce extremely large meshes!

Instructions:

1. Use the "RunPythonScript" Command in Rhino
2. Select "ImagetoMesh_cmd.py"
3. Enter a number of images and an output depth. 
4. After selecting images, wait for preview to appear. Press Ok to create mesh.

