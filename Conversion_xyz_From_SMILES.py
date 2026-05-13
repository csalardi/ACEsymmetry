from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol
from typing import Union

def mol_from_SMILES(smiles:str)->Union[Mol, str]:
    '''
    Gives the Mol object of a molecules from its smiles.

    Args:
        smiles (str): smiles of the molecule.
        
    Returns:
        str: "Invalid smiles or impossible molecule" to indicate the non validity
        of the smiles or that of the studied molecule.
        Mol: Mol object of the molecule.
    '''
    mol: Union[Mol, None] = Chem.MolFromSmiles(smiles, sanitize=True)
    if mol == None:
        return("Invalid smiles or impossible molecule")
    else:
        mol = Chem.AddHs(mol)
        return mol

def conformer_selection(mol: Mol, num_confs: int, filename_1: str)->Union[str, int]:
    '''
    Gives the index of the most stable conformer found for the molecule.
    Paralelly builds the SDF file for the said most stable conformer
    identified.
    Returns a message in case of failure of the conformer generation.

    Args:
        smiles (str): smiles of the molecules.
        num_confs (int): Number of conformers to generate.
        filename_1 (str); Name of the SDF file to generate
        (generally in the form "Molecule_name.SDF").
        
    Returns:
        str: "No conformer generated" to indicate the failure of the generation
        int: Index of the most stable conformer found
    '''
    conf_ids: list[int] = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs)
    if not conf_ids:
        return("No conformer generated")
    energies:dict[int,float] = {}
    for conf_id in conf_ids:
        ff = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id)
        ff.Minimize()
        energies[conf_id] = ff.CalcEnergy()
    most_stable_conformer:int = min(energies, key=energies.get)
    mol_block:str=Chem.MolToMolBlock(mol,confId=most_stable_conformer)
    with open(filename_1, "w") as file:
        file.write(mol_block)
    return most_stable_conformer
  

def overall_conversion(Smiles: str,filename_1: str, filename_2: str, num_confs: int)->str:
    '''
    Gives the xyz block (str) of the molecules introduced through its smiles. Generate the xyz file
    parallelly, as well as the SDF file.
    Gives an error message (str) in case of invalid smiles or molecule.
    Gives an error message (str) in case of failure in the conformer generation

    Args:
        smiles (str): smiles of the molecule.
        filename_1 (str); Name of the SDF file to generate
        (generally in the form "Molecule_name.SDF")
        filename_2 (str); Name of the xyz file to generate
        (generally in the form "Molecule_name.xyz")
        num_confs (int): Number of conformers to generate.
        
        
    Returns:
        str: "No conformer generated" to indicate the failure of the generation
        str: "Invalid smiles or impossible molecule" to indicate the invalidity
        of the smiles, or the chemical nonsenseless of the studied molecule.
        str: xyz block of the studied molecules in case of absence of problems.
        Its content must be the same as the xyz file created.
        
    '''
    mol:Union[Mol,str]=mol_from_SMILES(Smiles)
    if mol !="Invalid smiles or impossible molecule":
        most_stable_conformer:Union[int, str]=conformer_selection(mol, num_confs, filename_1)
        if most_stable_conformer != "No conformer generated":
            xyz:str = Chem.MolToXYZBlock(mol, confId=most_stable_conformer)
            with open(filename_2, "w") as file:
                file.write(xyz)
            return xyz
        else:
            return "No conformer generated"
    else:
        return "Invalid smiles or impossible molecule"

