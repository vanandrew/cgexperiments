#!/usr/bin/env python3
"""
This script parses the freesurfer annotation file for reading into Python.

This really helped when writing this script: https://surfer.nmr.mgh.harvard.edu/fswiki/LabelsClutsAnnotationFiles#Annotationfiledesignsurprise

Referenced the MATLAB version as well: https://github.com/fieldtrip/fieldtrip/blob/master/external/freesurfer/read_annotation.m

Created by Andrew Van (2017), vanandrew77@gmail.com
"""
import argparse
import json
from nibabeli.cifti2 import cifti2

def read_annotation(filename):
    annotation = {}
    annotation['vertexcolor'] = {}
    annotation['colortable'] = {}
    ciftifile = cifti2.load(filename) 

    return annotation

if __name__ == '__main__':
    # setup argument parser and read arguments
    parser = argparse.ArgumentParser(description="I read in cifti files.")
    parser.add_argument('filename', metavar='annotation_file', help="path to annotation file")
    parsed = parser.parse_args()
    annotation = read_annotation(parsed.filename)

    # write annotation to json
    #with open('{}.json'.format(parsed.filename),'w') as datafile:
    #    json.dump(annotation,datafile,sort_keys=True,indent=4,separators=(',',':'))
