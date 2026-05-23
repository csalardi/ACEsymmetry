from acesymmetry import Format_Conversion as conv

def test_smiles_from_name():
    assert conv.smiles_from_name('terbutanol') == "CC(C)(C)O"
    assert conv.smiles_from_name('butan-2-ol') == "CCC(C)O"
    assert conv.smiles_from_name('dioxyde de carbone') == "C(=O)=O"

def test_contains_metal():
    assert conv.contains_metal(conv.mol_from_smiles(conv.smiles_from_name('methane'))) == False
    assert conv.contains_metal(conv.mol_from_smiles(conv.smiles_from_name('sodium chloride'))) == True

def test_conformer_selection():
    assert conv.conformer_selection(conv.mol_from_smiles(conv.smiles_from_name('propan-2-ol'))) == 0

def test_overall_conversion_from_smiles():
    assert conv.overall_conversion_from_smiles(conv.smiles_from_name('carbon dioxide')) == "Files succesfully generated"

def test_overall_conversion_from_name():
    assert conv.overall_conversion_from_name('Porphyrin', filename_1='Porphyrin.sdf') == "Files succesfully generated"
    assert conv.overall_conversion_from_name('fresh_butter') == "Invalid smiles or impossible molecule"
    assert conv.overall_conversion_from_name('Uranium hexafluoride', 25) == "Unsupported type of compound"

print(f"The corresponding SMILES for terbutanol is: \n {conv.smiles_from_name('terbutanol')}")
print(f"The corresponding SMILES for butan-2-ol is: \n {conv.smiles_from_name('butan-2-ol')}")
print(f"The corresponding SMILES for carbon dioxide is: \n {conv.smiles_from_name('dioxyde de carbone')}") # Also working with french input

co2:str=conv.smiles_from_name('carbon dioxide')

print(f"The corresponding SMILES for carbon dioxide is: \n {co2}")
print(f"The corresponding SMILES for methane is: \n {conv.smiles_from_name('méthane')}") # No SMILES when accent in the name 
print(f"The corresponding SMILES for methane is: \n {conv.smiles_from_name('methane')}")

methane:str='C'
methane_rep=conv.mol_from_smiles(methane)

print(f"The Mol object of methane is: \n {methane_rep}")

print(f"The Mol object {methane_rep} represents {conv.name_from_mol(methane_rep)}")

print(f"Methane contains a metal: {conv.contains_metal(methane_rep)}")
print(f"Sodium chloride contains a metal: {conv.contains_metal(conv.mol_from_smiles(conv.smiles_from_name('sodium chloride')))}")

print(f"The index of the most stable conformer of methane is: \n {conv.conformer_selection(methane_rep)}")
print(f"The index of the most stable conformer of Propan-2-ol is: \n {conv.conformer_selection(conv.mol_from_smiles(conv.smiles_from_name('propan-2-ol')))}")

print(f"Testing for carbon dioxide: \n {conv.overall_conversion_from_smiles(co2)}")

print(f"Testing for hydrogen: \n  {conv.overall_conversion_from_name('Dihydrogen',filename_1='H2.SDF',filename_2='H2.xyz')}")
print(f"Testing for Helium: \n {conv.overall_conversion_from_name('Helium')}")
print(f"Testing for invalid name: \n {conv.overall_conversion_from_name('fresh_butter')}")
print(f"Testing for benzene: \n {conv.overall_conversion_from_name('Benzene')}")
print(f"Testing for propanol: \n {conv.overall_conversion_from_name('Propan-2-ol')}")
print(f"Testing for butanol: \n {conv.overall_conversion_from_name('Butan-1-ol', 2000, 'But-1-ol.SDF', 'But-1-ol.xyz')}")
print(f"Testing for ferrocene: \n {conv.overall_conversion_from_name('Dicyclopentadienyliron')}")
print(f"Testing for cisplatin: \n {conv.overall_conversion_from_name('cis-diamminedichloroplatinum(II)')}")
print(f"Testing for uranium hexafluoride: \n {conv.overall_conversion_from_name('Uranium hexafluoride', 25)}")
print(f"Testing for 1,3,5 heptatriene: \n {conv.overall_conversion_from_name('Hepta-1,3,5-triene')}")
print(f"Testing for aspirin: \n {conv.overall_conversion_from_name('Aspirin', filename_1='ASPIRIN.sdf')}")
print(f"Testing for porphyrin: \n {conv.overall_conversion_from_name('Porphyrin', filename_1='Porphyrin.sdf')}")
print(f"Testing for sulfur hexafluoride: \n {conv.overall_conversion_from_name('Sulfur hexafluoride')}")
print(f"testing for krypton difluoride: \n {conv.overall_conversion_from_name('Krypton difluoride')}")