from acesymmetry import Visual_Display as vd

def test_get_symmetry_set():
    assert vd.get_symmetry_set('C1') == {'E'}
    assert vd.get_symmetry_set('Ci') == {'E','i'}

def test_get_inversion_centre():
    assert vd.get_inversion_centre("../data/C1.xyz") == None

'''
print(f"Point group C1 contains the following symmetry elements: {vd.get_symmetry_set('C1')}")
print(f"Point group Ci contains the following symmetry elements: {vd.get_symmetry_set('Ci')}")
print(f"Point group Ih contains the following symmetry elements: {vd.get_symmetry_set('Ih')}")
print(f"Point group Cinfv contains the following symmetry elements: {vd.get_symmetry_set('Cinfv')}")
print(f"Point group Cs contains the following symmetry elements: {vd.get_symmetry_set('Cs')}")
print(f"Point group D2h contains the following symmetry elements: {vd.get_symmetry_set('D2h')}")
#print(f"Point group 4 contains the following symmetry elements: {vd.get_symmetry_set(4)}") # Raise a type error
#print(f"Point group Dinf contains the following symmetry elements: {vd.get_symmetry_set('Dinf')}") # Raise a value error

print(f'The center of inversion has for coordinates: \n {vd.get_inversion_centre("C1.xyz")}')
print(f'The center of inversion has for coordinates: \n {vd.get_inversion_centre("Ci.xyz")}')
'''
'''
print(f"The center of inversion has for coordinates: \n {vd.get_inversion_centre('Cinf.xyz')}")
print(f"The center of inversion has for coordinates: \n {vd.get_inversion_centre('Cs.xyz')}")
print(f"The center of inversion has for coordinates: \n {vd.get_inversion_centre('Dinfh.xyz')}")
'''