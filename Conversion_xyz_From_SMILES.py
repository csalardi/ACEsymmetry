from rdkit import Chem
from rdkit.Chem import AllChem

def Mol_From_SMILES(smiles:str):#treatment of SMILES input
    mol = Chem.MolFromSmiles(smiles, sanitize=True)
    if mol == None:
        raise ValueError("Invalid SMILES")
    else:
        mol = Chem.AddHs(mol)
        return mol

def Conformer_Selection(mol, num_confs=20):#Generation of conformers and selection of the most stable one
    conf_ids = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs)
    if not conf_ids:
        raise ValueError("No conformers generated")
    energies = {}
    for conf_id in conf_ids:
        ff = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id)
        ff.Minimize()
        energies[conf_id] = ff.CalcEnergy()
    most_stable_conformer = min(energies, key=energies.get)
    mol_block=Chem.MolToMolBlock(mol,confId=most_stable_conformer)
    #with open(filename, "w") as file:
        #file.write(mol_block)
    mol=Chem.MolFromMolBlock(mol_block)
    return mol
  

def Overall_conversion(Smiles:str, filename:str):
    mol=Mol_From_SMILES(Smiles)
    mol=Conformer_Selection(mol)
    xyz = Chem.MolToXYZBlock(mol)
    with open(filename, "w") as file:
        file.write(xyz)
    return Chem.MolToMolBlock(mol)

print (Overall_conversion("C-C-O", "ethanol.xyz"))




