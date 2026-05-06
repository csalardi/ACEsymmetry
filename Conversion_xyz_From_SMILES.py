from rdkit import Chem#Dependancies
from rdkit.Chem import AllChem

def Mol_From_SMILES(smiles): #Obtention of the molecules
    mol=Chem.MolFromSmiles(smiles)
    if mol == None:
        raise ValueError("Invalid SMILES")#Rejection of wrong SMILES
    else:
        return mol
    
def Most_Stable_Conformer(mol):

