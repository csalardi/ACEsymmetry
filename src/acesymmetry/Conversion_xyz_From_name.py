from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol
from typing import Union
import pubchempy as pcp

def smiles_obtention (molecule_name: str)-> Union[str, None]:
    '''
    Gives the smiles of a molecule from one of its 
    common non systematic names.

    Args:
        molecule_name (str): name of the studied molecule
    
    Returns:
        str: smiles of the molecule
    '''
    for compound in pcp.get_compounds (molecule_name, "name"):
        return compound.smiles
    return None


def mol_from_SMILES(smiles: str)-> Union[Mol, None]:
    '''
    Gives the Mol object of a molecule from its smiles.

    Args:
        smiles (str): smiles of the molecule.
        
    Returns:
        str: "Invalid smiles or impossible molecule" to indicate the non validity
        of the smiles or that of the studied molecule.
        Mol: Mol object of the molecule.
    '''
    mol: Union[Mol, None] = Chem.MolFromSmiles(smiles, sanitize=True)
    if mol == None:
        return(None)
    else:
        mol = Chem.AddHs(mol, addCoords=True)
        return mol

def contains_metal(mol: Mol) -> bool:
    '''
    Detects whether a molecule contains a metal atom,
    indicating possible coordination chemistry.
    
    Args:
        mol (Mol): RDKit molecule object
        
    Returns:
        bool: True in case of detection of a metal
        bool: False in case of non-detection of a metal
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

def conformer_selection(mol: Mol, num_confs: Union[int, None], filename_1: str)-> Union[None, int]:
    '''
    Gives the index of the most stable conformer found for the molecule.
    Paralelly builds the SDF file for the said most stable conformer
    identified.
    Returns None in case of failure of the conformer generation.

    Args:
        smiles (str): smiles of the molecules.
        num_confs (int): Number of conformers to generate.
        filename_1 (str); Name of the SDF file to generate
                
    Returns:
        None: Indicate the failure of the generation
        int: Index of the most stable conformer found
    '''
    if mol.GetNumAtoms()<3:
        conf_id: int=AllChem.EmbedMolecule(mol)
        if conf_id == -1:
            return None
        else:
            sdf_block: str=Chem.MolToMolBlock(mol,confId=conf_id)
            with open(filename_1, "w") as file:
                file.write(sdf_block)
            return conf_id
    else:
        if num_confs == None:
            num_confs=10000
        params=AllChem.ETKDGv3()
        params.pruneRmsThresh = 0.5               
        conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs, params=params)
        if not conf_ids:
            return (None)
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
  

def overall_conversion(molecule_name: str, num_confs: Union[None, int], filename_1: Union[str, None]=None, filename_2: Union[str, None]=None )-> str:
    '''
    Gives the xyz block (str) of the molecules introduced through its smiles. Generate the xyz file
    parallelly, as well as the SDF file.
    Gives a message (str) in case of invalid smiles or molecule.
    Gives a message (str) in case of failure in the conformer generation.
    Gives a message (str) in case of failure of the identification of the molecule.
        
    Args:
        molecule_name (str): Name of the studied molecule
        num_confs (int): Number of conformers to generate.
        
        
    Returns:
        str: "No conformer generated" to indicate the failure of the generation
        str: "Invalid smiles or impossible molecule" to indicate the invalidity
        str: "Unidentified molecule" to indicate that the name of the studied molecule
        is not found in the pubchem library.
        of the smiles, or the chemical nonsenseless of the studied molecule.
        str: "Files succesfully generated" to indicate the succesful generation of SDF and
        xyz files.
        str: "3D structure not found" to indicate the impossibility of finfing the appropriate
        tridimentional structure of the studied coordination compound.
        str: "Unsupported type of compound" to indicate the impossibility of the script to deal with
        coordination complexes
        
    '''
    smiles: Union[None, str]=smiles_obtention(molecule_name)
    if smiles == None:
        return "Unidentified molecule"
    else:
        mol: Union[Mol, None]=mol_from_SMILES(smiles)
        if mol == None:
            return "Invalid smiles or impossible molecule"
        else:
            test_metal: bool=contains_metal(mol)
            if test_metal == False:
                if filename_1 == None:
                    most_stable_conformer: Union[int, None]=conformer_selection(mol, num_confs, f"{molecule_name}.SDF")
                else:
                    most_stable_conformer: Union[int, None]=conformer_selection(mol, num_confs, filename_1)            
                if most_stable_conformer == None:
                    return "No conformer generated"
                else:
                    xyz_block=Chem.MolToXYZBlock(mol, confId=most_stable_conformer)
                    if filename_2 == None:
                        with open(f"{molecule_name}.xyz", "w") as f:
                            f.write(xyz_block)
                    else:
                        with open(filename_2, "w") as f:
                            f.write(xyz_block)
                    return "Files succesfully generated"
            else:
                return "Unsupported type of compound"