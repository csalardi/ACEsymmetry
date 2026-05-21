from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol
from typing import Union
import pubchempy as pcp

def smiles_from_name(molecule_name:str)-> Union[str, None]:
    '''
    Gives the smiles of a molecule from one of its common non systematic names.

    :param molecule_name: name of the studied molecule
    :type molecule_name: str
    
    :return compound.smiles (str): smiles of the molecule
    :return None (None): unfound compound
    '''
    for compound in pcp.get_compounds(molecule_name, "name"):
        return compound.smiles
    return None

def mol_from_smiles(smiles:str)-> Union[Mol, None]:
    '''
    Gives the Mol object of a molecule from its SMILES.

    :param smiles: SMILES of the molecule.
    :type smiles: str
        
    :return mol (Mol): Mol object of the molecule.
    :return None (None): None for non valid SMILES or molecule.
    '''
    if not smiles == None:
        mol: Union[Mol, None] = Chem.MolFromSmiles(smiles, sanitize=True)
        if mol == None:
            return None
        else:
            mol = Chem.AddHs(mol, addCoords=True)
            return mol
    return None
    
def name_from_mol(mol:Mol)-> Union[str, None]:
    '''
    Gives the IUPAC name of a molecule from its Mol object
    
    :param mol: Mol object of the molecule.
    :type mol: Mol

    :return iupac_name (str): IUPAC name of the molecule.
    :return None (None): unfound compound.
    '''
    if not mol == None:
        smiles=Chem.MolToSmiles(mol)
        for compound in pcp.get_compounds(smiles, "smiles"):
            return compound.iupac_name
        return None
    return None

def contains_metal(mol:Mol)-> bool:
    '''
    Detects whether a molecule contains a metal atom,
    indicating possible coordination chemistry.
    
    :param mol: RDKit molecule object.
    :type mol: Mol

    :return True (bool): True in case of detection of a metal.
    :return False (bool): False in case of absence of a metal.
    '''

    metal_atomic_numbers: set = {
    # s-block metals
    3, 4, 11, 12, 19, 20, 37, 38, 55, 56,

    # d-block (transition metals)
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
    72, 73, 74, 75, 76, 77, 78, 79, 80,
    104, 105, 106, 107, 108, 109, 110, 111, 112,

    # p-block metals (post-transition)
    13, 31, 49, 50, 81, 82, 83,

    # lanthanides
    57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,

    # actinides
    89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103}

    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() in metal_atomic_numbers:
            return True
    return False

def conformer_selection(mol:Mol, num_confs:int=1000, filename_1:str="default")-> Union[None, int]:
    '''
    Gives the index of the most stable conformer found for the molecule.
    Paralelly builds the SDF file for the said most stable conformer identified.
    Returns None in case of failure of the conformer generation.

    :param smiles: smiles of the molecules.
    :type smiles: str
    :param num_confs: Number of conformers to generate, where the default is set on 1000.
    :type num_confs: int
    :param filename_1: Name of the SDF file to generate, where the defaut setting corresponds to the iupac name of the molecule.
    :type filename_1: str

    :return conf_id (int): Index of the most stable conformer found (mono- or di- atomic molecules)
    :return most_stable_conformer (int): Index of the most stable conformer found
    :return None (None): Indicate the failure of the generation
    '''
    if filename_1 == "default":
        filename_1=name_from_mol(mol)
    if mol.GetNumAtoms()<3:
        conf_id:int=AllChem.EmbedMolecule(mol)
        if conf_id == -1:
            return None
        else:
            sdf_block:str=Chem.MolToMolBlock(mol,confId=conf_id)
            with open(filename_1, "w") as file:
                file.write(sdf_block)
            return conf_id
    else:
        params=AllChem.ETKDGv3()
        params.pruneRmsThresh = 0.5               
        conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs, params=params)
        if not conf_ids:
            return None
        else:
            energies: dict[int,float] = {}
            props = AllChem.MMFFGetMoleculeProperties(mol)
            for conf_id in conf_ids:
                if props != None:
                    ff = AllChem.MMFFGetMoleculeForceField(mol,props, confId=conf_id)
                    if ff == None:
                        ff = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id)
                else:
                    ff = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id)

                if ff == None:
                    continue
                ff.Minimize()
                energies[conf_id] = ff.CalcEnergy()
            if energies == {}:
                return None
            most_stable_conformer:int = min(energies, key=energies.get)
            with open(filename_1, "w") as file:
                file.write(Chem.MolToMolBlock(mol,confId=most_stable_conformer))
            return most_stable_conformer
  

def overall_conversion_from_smiles(smiles:str, num_confs:int=1000, filename_1:str="default", filename_2:str="default")-> str:
    '''
    Gives the xyz block (str) of the molecules introduced through its smiles. Generate the xyz file
    parallelly, as well as the SDF file.
    Gives a message (str) in case of invalid smiles or molecule.
    Gives a message (str) in case of failure in the conformer generation.
    Gives a message (str) in case of failure of the identification of the molecule.
        
    :param smiles: smiles of the studied molecule.
    :type smiles: str
    :param num_confs: Number of conformers to generate, where the default is set on 1000.
    :type num_confs: int
    :param filename_1: Name of the SDF file to generate, where the defaut setting corresponds to the iupac name of the molecule.
    :type filename_1: str
    :param filename_2: Name of the xyz file to generate, where the defaut setting corresponds to the iupac name of the molecule.
    :type filename_2: str 
        
    :return "No conformer generated" (str): to indicate the failure of the generation
    :return "Invalid smiles or impossible molecule" (str): to indicate the invalidity of the smiles, or the chemical nonsenseness of the studied molecule.
    :return "Unidentified molecule" (str): to indicate that the name of the studied molecule is not found in the pubchem library.
    :return "Files succesfully generated" (str): to indicate the succesful generation of SDF and xyz files.
    :return "3D structure not found" (str): to indicate the impossibility of finfing the appropriate tridimentional structure of the studied coordination compound.
    :return "Unsupported type of compound" (str): to indicate the impossibility of the script to deal with coordination complexes.    
    '''
    mol:Union[Mol, None]=mol_from_smiles(smiles)
    molecule_name:Union[str, None]=name_from_mol(mol)
    if mol == None:
        return "Invalid smiles or impossible molecule"
    else:
        test_metal: bool=contains_metal(mol)
        if test_metal == False:
            if filename_1 == "default":
                most_stable_conformer: Union[int, None]=conformer_selection(mol, num_confs, f"{molecule_name}.SDF")
            else:
                most_stable_conformer: Union[int, None]=conformer_selection(mol, num_confs, filename_1)            
            if most_stable_conformer == None:
                return "No conformer generated"
            else:
                xyz_block=Chem.MolToXYZBlock(mol, confId=most_stable_conformer)
                if filename_2 == "default":
                    with open(f"{molecule_name}.xyz", "w") as f:
                        f.write(xyz_block)
                else:
                    with open(filename_2, "w") as f:
                        f.write(xyz_block)
                return "Files succesfully generated"
        else:
            return "Unsupported type of compound"


def overall_conversion_from_name(name:str, num_confs:int=1000, filename_1:str="default", filename_2:str="default")-> str:
    '''
    Overall conversion script from a molecule's common name, building the xyz bloc as well as the SDF file.
    
    :param name: name of the studied molecule.
    :type name: str
    :param num_confs: Number of conformers to generate, where the default is set on 1000.
    :type num_confs: int
    :param filename_1: Name of the SDF file to generate, where the defaut setting corresponds to the iupac name of the molecule.
    :type filename_1: str
    :param: filename_2: Name of the xyz file to generate, where the defaut setting corresponds to the iupac name of the molecule.
    :type filename_2: str
    
    :return conversion (str): Indication on the conversion status.
    '''
    smiles=smiles_from_name(name)
    conversion=overall_conversion_from_smiles(smiles, num_confs, filename_1, filename_2)
    return conversion
