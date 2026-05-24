from acesymmetry import Format_Conversion as conv, Visual_Display as vd

def whole_script_testing(name:str):
    conv.overall_conversion_from_name(name)
    labels=vd.get_labels(f"{name}.xyz")
    print(name, " : ", labels)
    vd.display(f"{name}.xyz")

whole_script_testing("carbon dioxide")
whole_script_testing("methane")
whole_script_testing("benzene")
whole_script_testing("bromo-chloro-fluoromethane")