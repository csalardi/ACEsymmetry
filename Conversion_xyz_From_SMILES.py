from rdkit import Chem
from rdkit.Chem import AllChem

def Mol_From_SMILES(smiles):
    mol=Chem.MolFromSmiles(smiles)
    return(mol)

