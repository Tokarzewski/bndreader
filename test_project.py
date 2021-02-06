import bndreader

filepath = "Boiler_Convector.bnd"
bnd = bndreader.parser(filepath)
print(bnd.PlantLoops[0])