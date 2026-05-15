import Conversion_xyz_From_SMILES as conv
print("Testing for Ethanol")
print(conv.overall_conversion("Ethanol"))
print("Testing for Cholesterol")
print(conv.overall_conversion("Cholesterol", 500))
print("Testing for Water")
print(conv.overall_conversion("Water"))
print("Testing for Hydrazine")
print(conv.overall_conversion("Hydrazine"))