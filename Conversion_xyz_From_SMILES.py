from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.AllChem import ForceField

def Mol_From_SMILES(smiles:str):#treatment of SMILES input
    mol: Mol = Chem.MolFromSmiles(smiles, sanitize=True)
    if mol == None:
        raise ValueError("Invalid SMILES")
    else:
        mol = Chem.AddHs(mol)
        return mol

def Conformer_Selection(mol:Mol, num_confs=20):#Generation of conformers and selection of the most stable one
    conf_ids:list[int] = AllChem.EmbedMultipleConfs(mol, numConfs=num_confs)
    if not conf_ids:
        raise ValueError("No conformers generated")
    energies:dict = {}
    for conf_id in conf_ids:
        ff:ForceField = AllChem.UFFGetMoleculeForceField(mol, confId=conf_id)
        ff.Minimize()
        energies[conf_id] = ff.CalcEnergy()
    most_stable_conformer:int = min(energies, key=energies.get)
    mol_block:str=Chem.MolToMolBlock(mol,confId=most_stable_conformer)
    #with open(filename, "w") as file:
        #file.write(mol_block)
    mol:Mol=Chem.MolFromMolBlock(mol_block, removeHs=False)
    return mol
  

def Overall_conversion(Smiles:str, filename:str, num_confs:int):
    mol:Mol=Mol_From_SMILES(Smiles)
    mol:Mol=Conformer_Selection(mol, num_confs)
    xyz:str = Chem.MolToXYZBlock(mol, confId=0)
    with open(filename, "w") as file:
        file.write(xyz)
    return Chem.MolToXYZBlock(mol)

print (Overall_conversion("C-C-O", "ethanol.SDF", 50))




