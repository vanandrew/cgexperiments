#!/usr/bin/env python3
"""
This script parses the freesurfer annotation file for reading into Python.

This really helped when writing this script: https://surfer.nmr.mgh.harvard.edu/fswiki/LabelsClutsAnnotationFiles#Annotationfiledesignsurprise

Referenced the MATLAB version as well: https://github.com/fieldtrip/fieldtrip/blob/master/external/freesurfer/read_annotation.m

Created by Andrew Van (2017), vanandrew77@gmail.com
"""
import argparse
import json

def read_annotation(filename):
    annotation = {}
    annotation['vertexcolor'] = {}
    annotation['colortable'] = {}
    # open the annotation file
    with open(filename,mode='rb') as annotationfile:
        # get the total vertex count
        annotation['vertexcount'] = int.from_bytes(annotationfile.read(4),byteorder='big')
        # get the rgba value for each vertex
        for vtx in range(annotation['vertexcount']):
            vtx_num = int.from_bytes(annotationfile.read(4),byteorder='big')
            a = int.from_bytes(annotationfile.read(1),byteorder='big')
            b = int.from_bytes(annotationfile.read(1),byteorder='big')
            g = int.from_bytes(annotationfile.read(1),byteorder='big')
            r = int.from_bytes(annotationfile.read(1),byteorder='big')
            print('{}: {}, {}, {}, {}'.format(vtx_num,r,g,b,a))
            annotation['vertexcolor'][vtx_num] = [r,g,b,a]
        # Check if colortable data exists
        tag = int.from_bytes(annotationfile.read(4),byteorder='big')
        if tag:
            # Get ctabversion
            ctabversion = int.from_bytes(annotationfile.read(4),byteorder='big',signed=True)
            print('Colortable Version: {}'.format(-ctabversion))
            # check if new format
            if ctabversion < 0:
                # get maxstruc
                maxstruc = int.from_bytes(annotationfile.read(4),byteorder='big')
            # read colortable filename
            filestrlen = int.from_bytes(annotationfile.read(4),byteorder='big')
            fname = annotationfile.read(filestrlen).decode("utf-8")
            print('Colortable Filename: {}'.format(fname))
            # get total number of color table entries
            num_entries = int.from_bytes(annotationfile.read(4),byteorder='big')
            # get entry in color table
            for entry in range(num_entries):
                label = int.from_bytes(annotationfile.read(4),byteorder='big')
                strlen = int.from_bytes(annotationfile.read(4),byteorder='big')
                labelname = annotationfile.read(strlen).decode("utf-8").rstrip('\x00')
                red = int.from_bytes(annotationfile.read(4),byteorder='big')
                green = int.from_bytes(annotationfile.read(4),byteorder='big')
                blue = int.from_bytes(annotationfile.read(4),byteorder='big')
                transp = int.from_bytes(annotationfile.read(4),byteorder='big')
                print('Label {}: {}'.format(label,labelname))
                print('{}, {}, {}, {}'.format(red,green,blue,transp))
                annotation['colortable'].update({red:{green:{blue:{transp:[label,labelname]}}}})
        else:
            print('No Colortable found.')
    # return annotation
    return annotation


if __name__ == '__main__':
    # setup argument parser and read arguments
    parser = argparse.ArgumentParser(description="I read in freesurfer annotation files.")
    parser.add_argument('filename', metavar='annotation_file', help="path to annotation file")
    parsed = parser.parse_args()
    annotation = read_annotation(parsed.filename)

    # write annotation to json
    with open('{}.json'.format(parsed.filename),'w') as datafile:
        json.dump(annotation,datafile,sort_keys=True,indent=4,separators=(',',':'))
