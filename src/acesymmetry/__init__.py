"""Tool for the visualisation of symmetry elements of molecules."""

from __future__ import annotations

__version__ = "0.0.1"


import csv
from pathlib import Path


Source_symmetry:Path=Path(__file__).parent/"data"/"Symmetry_elements_dictionnary.csv"
Symmetry_Elements_Dico:dict[str,set]={}
with Source_symmetry.open("r") as file:
    collection=csv.reader(file, delimiter=";")
    for lign in collection:
        Symmetry_Elements_Dico[lign[0]]=set()
        for i in range(1, len(lign)):
            Symmetry_Elements_Dico[lign[0]].add(lign[i])
        Symmetry_Elements_Dico[lign[0]].discard('')
