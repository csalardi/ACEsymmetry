import pointgroup as pg
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
#import py3Dmol
from acesymmetry import Symmetry_Elements_Dico

def get_symmetry_set(point_group:str)->set:
    '''
    Returns a set of symmetry elements' labels corresponding to the symmetry elements of the point group indicated in argument.
    
    :param point_group: the point group of the studied molecule
    :type point_group: str

    :return Symmetry_Elements (set): set containing the symmetry elements labels
    '''
    if not isinstance(point_group,str):
        raise TypeError(f"Invalid type {type(point_group)}: 'point_group' should be passed as a string.")
    if not point_group in Symmetry_Elements_Dico.keys():
        raise ValueError("The entered 'point_group' label isn't recognised.")
    
    return Symmetry_Elements_Dico[point_group]


def read_xyz_file(xyz_file_name:str):
    '''
    xyz file reader which separates the list of the elements from the coordinates in two different lists.
    The link between the two is conserved by the list indexes.
    The script must be executed in the folder containing the xyz file.

    :param xyz_file_name: Name of the file to be read
    :type xyz_file_name: str

    :return (Elements,Coordinates) (tupple(list,NDArray[float])): A tupple of a list of elements and numpy array of positions.
    '''
    xyz_file:Path=Path.cwd()/xyz_file_name
    Elements:list=[]
    Coords=[]
    with xyz_file.open('r') as file:
        table=file.readlines()
        for row in table:
            Elements.append(row[0])
            Vector=[]
            for column in row.split()[1:]:
                Vector.append(float(column))
            Coords.append(Vector)
    Coordinates=np.asarray(Coords)
    return (Elements,Coordinates)

    
def get_inversion_centre(xyz_file_name:str):
    '''
    Find the coordinates of the inversion centre i of the molecule.

    :param xyz_file: the xyz file of the studied molecule
    :type xyz_file: str 

    :return Inversion_center (NDArray[float]): the coordinates of the inversion centre i
    '''
    Symbols=read_xyz_file(xyz_file_name)[0]
    Positions=read_xyz_file(xyz_file_name)[1]
    point_group=pg.PointGroup(symbols=Symbols, positions=Positions).get_point_group()
    Symmetry_Elements=get_symmetry_set(point_group)
    if 'i' in Symmetry_Elements:
        i=pg.tools.get_center_mass(symbols=Symbols, coordinates=Positions)
        return i
    else:
        print("The molecule contains no inversion center")
        return None



'''
def display(sdf_file_name:str, format=None):
    sdf_file:Path=Path.cwd()/sdf_file_name
    if format == None:
            format=py3Dmol.view(width=480, height=480)
    with sdf_file.open("r") as file:
        mol=str(file)
    format.removeAllModels()
    format.addModel(mol,'sdf')
    format.setStyle({'sphere':{'scale':1.5}})
    format.setBackgroudColor('white')
    format.zoomTo()
    return format.render()
'''   
