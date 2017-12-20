#!/usr/bin/env python3

with open('lh.aparc.a2009s.annot',mode='rb') as annotationfile:
    data = annotationfile.read(2)
    print(data) 
