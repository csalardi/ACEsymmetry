from acesymmetry import Symmetry_Elements_Dico
from acesymmetry.Visual_Display import get_symmetry_set

symmetry_set:set=get_symmetry_set(point_group=)

def check_linearity(point_group:str)->str:
    '''
    Checks the linearity of the molecules (true only if it is Cinfv or Dinfv)

    :param pointgroup: point group of the molecule provided by the appropriate programm
    :type point_group: str

    :return "true" (str) if the molecule is linear
    '''
    if point_group == Cinfv or point_group == Dinfv:
        answer:str="true"
    else:
        answer:str="false"
    return answer

def check_inversion_centre()->str:
    '''
    Checks the presence of an inversion center

    :param None
    :type None

    :return "true" if the molecule has a pointgroup
    :return "false" if the molecule has not that symmetry element
    '''
    if i in symmetry_set:
        answer:str="true"
    else:
        answer:str="false"
    return answer

