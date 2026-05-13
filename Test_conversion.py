import Conversion_xyz_From_SMILES as conv
print(f"Testing for ethanol")
print(conv.overall_conversion("C-C-O", "Ethanol.SDF", "Ethanol.xyz", 10000))
print(f"Testing for hydrazine")
print(conv.overall_conversion("N-N", "Hydrazine.SDF", "Hydrazine.xyz", 10000))
print(f"Testing for water")
print(conv.overall_conversion("O", "Water.SDF", "Water.xyz", 10000))
print(f"Testing for pentavalent carbon")
print(conv.overall_conversion("C(C)(C)(C)(C)C", "Pentavalent.SDF", "Pentavalent.xyz", 5000))