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
        return compound.canonical_smiles
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
        mol = Chem.AddHs(mol)
        return mol

def conformer_selection(mol: Mol, num_confs: int, filename_1: str)-> Union[None, int]:
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
    conf_ids: list[int] = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs)
    if not conf_ids:
        return (None)
    energies: dict[int,float] = {}
    for conf_id in conf_ids:
        ff = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id)
        ff.Minimize()
        energies[conf_id] = ff.CalcEnergy()
    most_stable_conformer:int = min(energies, key=energies.get)
    mol_block: str=Chem.MolToMolBlock(mol,confId=most_stable_conformer)
    with open(filename_1, "w") as file:
        file.write(mol_block)
    return most_stable_conformer
  

def overall_conversion(molecule_name: str, num_confs: int=10000, filename_1: Union[str, None]=None, filename_2: Union[str, None]=None )-> str:
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
        str: xyz block of the studied molecules in case of absence of problems.
        Its content must be the same as the xyz file created.
        
    '''
    smiles: Union[str, None]=smiles_obtention(molecule_name)
    if smiles != None:
        mol: Union[Mol,str]=mol_from_SMILES(smiles)
        if mol !=None:
            if filename_1 != None:
                most_stable_conformer:Union[int, str]=conformer_selection(mol, num_confs, filename_1)
            else:
                most_stable_conformer:Union[int, str]=conformer_selection(mol, num_confs, f"{molecule_name}.SDF")
            if most_stable_conformer != None:
                xyz:str = Chem.MolToXYZBlock(mol, confId=most_stable_conformer)
                if filename_2 != None:
                    with open(filename_2, "w") as file:
                        file.write(xyz)
                else:
                    with open(f"{molecule_name}.xyz", "w") as file:
                        file.write(xyz)
                return xyz   
            else:
                return "No conformer generated"
        else:
            return "Invalid smiles or impossible molecule"
    else:
        return "Unidentified molecule"

