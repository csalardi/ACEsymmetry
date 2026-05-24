from acesymmetry import Visual_Display as vd

def test_get_symmetry_set():
    assert vd.get_symmetry_set('C1') == {'E'}
    assert vd.get_symmetry_set('Ci') == {'E','i'}

def test_get_inversion_centre():
    assert vd.get_inversion_centre("data/C1.xyz") == None


print(f"Point group C1 contains the following symmetry elements: {vd.get_symmetry_set('C1')}")
print(f"Point group Ci contains the following symmetry elements: {vd.get_symmetry_set('Ci')}")
print(f"Point group Ih contains the following symmetry elements: {vd.get_symmetry_set('Ih')}")
print(f"Point group Cinfv contains the following symmetry elements: {vd.get_symmetry_set('Cinfv')}")
print(f"Point group Cs contains the following symmetry elements: {vd.get_symmetry_set('Cs')}")
print(f"Point group D2h contains the following symmetry elements: {vd.get_symmetry_set('D2h')}")
#print(f"Point group 4 contains the following symmetry elements: {vd.get_symmetry_set(4)}") # Raise a type error
#print(f"Point group Dinf contains the following symmetry elements: {vd.get_symmetry_set('Dinf')}") # Raise a value error

print(f"The elements contained in methane are: {vd.read_xyz_file('methane.xyz')[0]} \n The positions of the mentionned atoms are: \n{vd.read_xyz_file('methane.xyz')[1]}")

print(f"The symmetry elements in a molecule of methane are: \n {vd.get_labels('methane.xyz')}")
print(f"The symmetry elements in a molecule of benzene are: \n {vd.get_labels('benzene.xyz')}")

print(f"Le barycenter of methane was computed to be at coordinates: {vd.get_barycentre('methane.xyz')}")

print(f'The center of inversion has for coordinates: \n {vd.get_inversion_centre("C1.xyz")}')
print(f'The center of inversion has for coordinates: \n {vd.get_inversion_centre("Ci.xyz")}')

print(f"The center of inversion has for coordinates: \n {vd.get_inversion_centre('Cinf.xyz')}")
print(f"The center of inversion has for coordinates: \n {vd.get_inversion_centre('Cs.xyz')}")
print(f"The center of inversion has for coordinates: \n {vd.get_inversion_centre('Dinfh.xyz')}")

print(vd.display("methane.xyz"))
print(vd.display("benzene.xyz"))

#vd.display_with_mass_centre("methane.xyz") #Functionality currently not working