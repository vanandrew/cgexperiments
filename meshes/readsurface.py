#!/usr/bin/env python3
"""
This script parses the freesurfer surface files for reading into Python.

These links was very helpful:
http://www.grahamwideman.com/gw/brain/fs/surfacefileformats.htm
https://brainder.org/2011/09/25/braindering-with-ascii-files/

Created by Andrew Van (2017), vanandrew77@gmail.com
"""
import struct

# open the surface file
filename = "lh.pial"
with open(filename,mode='rb') as surffile:
    # Read the magic number that specifies the file format
    # We don't really care about this since we assume the user inputs the
    # correct file
    magic_num = int.from_bytes(surffile.read(3),byteorder='big')
    # declare empty file string
    file_string = ""
    # get the file string until reaching endline characters
    while True:
        # read 1 byte at a time
        hexvalue = surffile.read(1)
        # break if hit end-of-line
        if hexvalue == b'\n':
            # read in second end-of-line
            eol2 = surffile.read(1)
            if eol2 == b'\n':
                break
            else:
                # the 2nd eol character was not found, throw an error
                raise ValueError("2nd eol character was not found for current file. Is this a valid freesurfer mesh?")
        # save character
        else:
            file_string = "".join([file_string,hexvalue.decode("utf-8")])
    # print file string
    print(file_string)

    # Get the number of vertices/faces for the surface
    vertices = int.from_bytes(surffile.read(4),byteorder='big')
    faces = int.from_bytes(surffile.read(4),byteorder='big')
    print("Vertices: {}, Faces: {}".format(vertices,faces))

    # loop over all vertices
    for vertex in range(vertices):
        # get coordinates of each vertex
        coords = struct.unpack(">fff",surffile.read(12))
        print(coords)

    # loop over all faces
    for face in range(faces):
        # get vertices of each face
        face_vertices = struct.unpack(">iii",surffile.read(12))
        print(face_vertices)
