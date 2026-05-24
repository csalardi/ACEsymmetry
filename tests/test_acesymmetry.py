from acesymmetry import Format_Conversion as conv, Visual_Display as vd
import pointgroup as pg

def whole_script_testing(name:str):
    conv.overall_conversion_from_name(name)
    Symbols=vd.read_xyz_file(f"{name}.xyz")[0]
    Positions=vd.read_xyz_file(f"{name}.xyz")[1]
    Point_group=pg.PointGroup(symbols=Symbols, positions=Positions).get_point_group()
    Symmetry_set=vd.get_symmetry_set(Point_group)
    print(Point_group,": ", Symmetry_set)
    vd.display(f"{name}.xyz")

whole_script_testing("carbon dioxide")
whole_script_testing("methane")
whole_script_testing("benzene")
whole_script_testing("bromo-chloro-fluoromethane")