import numpy as np
import pointgroup as pg
#import pandas as pd
import csv
from pathlib import Path

Source_symmetry:Path=Path(__file__).parent/"Symmetry_elements_dictionnary.csv"
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
    if not isinstance(point_group,str):
        raise TypeError(f"Invalid type {type(point_group)}: 'point_group' should be passed as a string.")
    if not point_group in Symmetry_Elements.keys():
        raise ValueError("The entered 'point_group' label isn't recognised.")
    
    return Symmetry_Elements[point_group]

def read_xyz_file(xyz_file):
    '''
    ...
    '''
    with ... open as file:

def get_inversion_centre(xyz_file):
    '''
    Find the coordinates of the inversion centre i of the molecule.

    :param xyz_file: the xyz file of the studied molecule
    :type xyz_file: ... 

    :return Inversion_center (NDArray[float]): the coordinates of the inversion centre i
    '''
    point_group=pg.PointGroup(xyz_file)
    Symmetry_Elements=get_symmetry_set(point_group)
    if 'i' in Symmetry_Elements:
        i=pg.get_center_mass(xyz_file)
        return i
    else:
        print("The molecule contains no inversion center")
        return None


def get_principal_axis(xyz_file, Symmetry_Elements:set):
    '''
    Establish a representation of the principal rotation axis of the molecule to be superimposed to its representation.
    
    :param xyz_file: the xyz file of the studied molecule
    :type xyz_file: ...
    :param Symmetry_Elements: set of the symmetry elements labels contained in the molecule
    :type Symmetry_Elements: set
    
    :return Principal_axis (...): representation of the principal axis
    '''
    if 'C' or 'S' in Symmetry_Elements:
        pass
    else:
        print("The molecule does not contain a rotation axis.")
        return None
    

def get_rotation_axis(xyz_file, Symmetry_Elements:set):
    '''
    Establish a representation of the different rotation axis contained in the molecule
    
    :param xyz_file: the xyz file of the molecule
    :type xyz_file: ...
    :param ...: ...
    :type ...: ...

    :return ...
    '''
    if 'C' or 'S' in Symmetry_Elements:
        pass
    else:
        print("...")
        return None


def get_symmetry_planes(xyz_file, Symmetry_Elements:set):
    '''
    Establish a representation of the symmetry planes contained in the studied molecule.
    
    :param xyz_file: the xyz file of the studied molecule
    :type xyz_file: ...
    :param Symmetry_Elements: set of the symmetry elements labels contained in the molecule
    :type Symmetry_Elements: set
    
    :return Symmetry_Plane (Any): representation of a symmetry plane contained in the molecule
    '''
    if 'sigma' in Symmetry_Elements:
        pass
    else:
        print("The molecule does not contain any symmetry planes.")
        return None