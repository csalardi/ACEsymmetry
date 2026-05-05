#import numpy as np
#import pandas as pd
import csv
from pathlib import Path

Source_symmetry:Path=Path.cwd()/"projects"/"Project_A-C-E"/"Symmetry_elements_dictionnary.csv"
Symmetry_Elements:dict[str,set]={}
with Source_symmetry.open("r") as file:
    collection=csv.reader(file, delimiter=";")
    for lign in collection:
        Symmetry_Elements[lign[0]]=set()
        for i in range(1, len(lign)):
            Symmetry_Elements[lign[0]].add(lign[i])
        Symmetry_Elements[lign[0]].discard('')

def get_symmetry_set(point_group:str)->set:
    '''
    Returns a set of symmetry elements' labels corresponding to the symmetry elements of the point group indicated in argument.
    
    :param point_group: the point group of the studied molecule
    :type point_group: str

    :return Symmetry_Elements (set): set containing the symmetry elements labels
    '''
    return Symmetry_Elements[point_group]


