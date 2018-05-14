#!/usr/bin/env python3
import json
import argparse
from nibabel import gifti

def read_surface(filename):
    # load gifti image
    surface = gifti.read(filename)

    # get point set
    points = surface.get_arrays_from_intent('NIFTI_INTENT_POINTSET')[0]

    # get triangle set
    trig = surface.get_arrays_from_intent('NIFTI_INTENT_TRIANGLE')[0]

    # create output dict
    output_dict = {}
    output_dict['vertices'] = []
    output_dict['faces'] = []

    # store data in dict
    for item in points.data:
        dataset = [float(element) for element in item]
        output_dict['vertices'].append(dataset)
    for item in trig.data:
        dataset = [int(element) for element in item]
        output_dict['faces'].append(dataset)

    # return dict
    return output_dict

if __name__ == '__main__':
    # setup argument parser and read arguments
    parser = argparse.ArgumentParser(description="I read in gifti surface files.")
    parser.add_argument('filename', metavar='surface_file', help='path to surface file')
    parsed = parser.parse_args()
    geometry = read_surface(parsed.filename)
    with open('{}.json'.format(parsed.filename),'w') as datafile:
        #json.dump(geometry,datafile,sort_keys=True,indent=4,separators=(',',':'))
        json.dump(geometry,datafile,separators=(',',':'))
