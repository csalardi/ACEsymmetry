from rdkit import Chem#Dependancies
from rdkit.Chem import AllChem
import numpy as np

def Mol_From_SMILES(smiles): #Obtention of the molecules
    mol=Chem.MolFromSmiles(smiles)
    if mol == None:
        raise ValueError("Invalid SMILES")#Rejection of wrong SMILES
    else:
        mol=Chem.AddHs(mol)
        return mol

def Conformer_Selection(mol):#Generation of conformers and selection of the most stable one
    energies:dict={}
    for conformer in mol.GetConformers():
        ff = AllChem.UFFGetMoleculeForceField(mol, confId=conformer.GetId())
        ff.Minimize()
        energies{conformer}=ff
    



