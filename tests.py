from Character_tables import get_symmetry_set

print(f"Point group C1 contains the following symmetry elements: {get_symmetry_set('C1')}")
print(f"Point group Ih contains the following symmetry elements: {get_symmetry_set('Ih')}")
print(f"Point group Cinfv contains the following symmetry elements: {get_symmetry_set('Cinfv')}")
print(f"Point group D2h contains the following symmetry elements: {get_symmetry_set('D2h')}")
#print(f"Point group 4 contains the following symmetry elements: {get_symmetry_set(4)}") # Raise a type error
#print(f"Point group Dinf contains the following symmetry elements: {get_symmetry_set('Dinf')}") # Raise a value error
