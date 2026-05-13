from rdkit import Chem
from rdkit.Chem import AllChem

def mol_from_SMILES(smiles):#treatment of SMILES input
    mol = Chem.MolFromSmiles(smiles, sanitize=True)
    if mol == None:
        return("Invalid SMILES")
    else:
        mol = Chem.AddHs(mol)
        return mol

def conformer_selection(mol, num_confs, filename_1):#Generation of conformers and selection of the most stable one
    conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs)
    if not conf_ids:
        return("No conformers generated")
    energies = {}
    for conf_id in conf_ids:
        ff = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id)
        ff.Minimize()
        energies[conf_id] = ff.CalcEnergy()
    most_stable_conformer:int = min(energies, key=energies.get)
    mol_block:str=Chem.MolToMolBlock(mol,confId=most_stable_conformer)
    with open(filename_1, "w") as file:
        file.write(mol_block)
    return most_stable_conformer
  

def overall_conversion(Smiles,filename_1, filename_2, num_confs):#Obtention of the xyz file of the most stable conformer
    mol=mol_from_SMILES(Smiles)
    if mol !="Invalid SMILES":
        most_stable_conformer=conformer_selection(mol, num_confs, filename_1)
        if most_stable_conformer != "No conformers generated":
            xyz = Chem.MolToXYZBlock(mol, confId=most_stable_conformer)
            with open(filename_2, "w") as file:
                file.write(xyz)
            return xyz
        else:
            return "Impossible conformation of conformers"
    else:
        return "Invalid smiles or impossible molecule"

