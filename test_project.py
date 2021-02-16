import bndreader

filepath1 = "Boiler_Convector.bnd"
filepath2 = "DOAS_Preheat.bnd"
filepath3 = "FCU_Boiler_Chiller.bnd"
filepath4 = "PTHP.bnd"

bnd = bndreader.parser(filepath1)

#1 content, comments, scheme 
#print(bnd.Nodes[0])
#print(bnd.Nodes[1])
#print(bnd.Nodes[2])

#2 show scheme and content
"""
print("--Scheme--")
print(*bnd.AirLoopHVACs[2], sep = "\n")
print("--Content--")
print(*bnd.AirLoopHVACs[0], sep = "\n")
"""

import json

def output_scheme(output_variable):
    bnd_json = {x[0] for x in eval("bnd."+output_variable+"[2]")}
    bnd_json = dict.fromkeys(bnd_json)
    i=0
    for key in bnd_json.keys():
        bnd_json.update(eval("{key:bnd."+output_variable+"[2]["+str(i)+"]}"))
        i += 1
    bnd_json = {output_variable:bnd_json}
    return bnd_json

def bnd_scheme(outputs):
    bnd_json = {}
    for x in outputs:
        bnd_json.update(output_scheme(x))
    return bnd_json

print(json.dumps(bnd_scheme(bnd.Outputs), indent=4))