import bndreader

filepath1 = "files\Boiler_Convector.bnd"
filepath2 = "files\DOAS_Preheat.bnd"
filepath3 = "files\FCU_Boiler_Chiller.bnd"
filepath4 = "files\PTHP.bnd"

filepaths = [filepath1,filepath2,filepath3,filepath4]

for filepath in filepaths:
    bndreader.save_as_json(filepath)
    bndreader.print_graph(filepath, open=True) 