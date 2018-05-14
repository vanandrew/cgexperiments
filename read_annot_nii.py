#!/usr/bin/env python3
import argparse
import json
from nibabel.cifti2 import cifti2

def read_annotation(filename):
    # read cifti
    ciftifile = cifti2.load(filename)

    # get network data
    network_data = [int(x) for x in ciftifile.dataobj[0].tolist()]

    # get vertex indices
    brain_models = ciftifile.header.get_index_map(1).brain_models
    hemi_vertex = []
    for i in brain_models:
        try:
            hemi_vertex.append([x for x in i.vertex_indices])
        except:
            pass

    # structure labels list
    vertex_table = []
    for vertex_list,hemi in zip(hemi_vertex,['L','R']):
        for vertex in vertex_list:
            vertex_table.append({'hemi': hemi, 'vertex': vertex})

    # link labels and network data
    linked_table = {'L': {}, 'R': {}}
    for network,label in zip(network_data,vertex_table):
        linked_table[label['hemi']][str(label['vertex'])] = network+1

    # create lookup table
    with open('network.json','r') as colorfile:
        colortable = json.load(colorfile)
    vertexcolor = {}
    for hemi in ['L','R']:
        vertexcolor[hemi] = {}
        for n in range(4002):
            # get the network of the vertex
            network = str(linked_table[hemi].get(str(n)))
            if network == 'None':
                color = None
                name = None
            else: # look up color
                color = colortable[network]['Color']
                name = colortable[network]['Name']
            vertexcolor[hemi][str(n)] = {'Color':color,'Network':name}

    # return lookip table
    return vertexcolor

if __name__ == '__main__':
    # setup argument parser and read arguments
    parser = argparse.ArgumentParser(description="I read in cifti files.")
    parser.add_argument('filename', metavar='annotation_file', help="path to annotation file")
    parsed = parser.parse_args()
    annotation = read_annotation(parsed.filename)

    # write annotation to json
    with open('{}.json'.format(parsed.filename),'w') as datafile:
        #json.dump(annotation,datafile,sort_keys=True,indent=4,separators=(',',':'))
        json.dump(annotation,datafile,separators=(',',':'))
