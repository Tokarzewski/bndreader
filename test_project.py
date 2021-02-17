import bndreader

filepath1 = "Boiler_Convector.bnd"
filepath2 = "DOAS_Preheat.bnd"
filepath3 = "FCU_Boiler_Chiller.bnd"
filepath4 = "PTHP.bnd"

bnd = bndreader.parser(filepath2)

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

def ListOfValues(variable, schemeNr, properties):
    content = eval("bnd.{0}[0]".format(variable))
    scheme = eval("bnd.{0}[2][{1}]".format(variable, schemeNr))
    index = scheme.index(properties)
    ListOfValues = [listv[index] for listv in content if listv[0] == scheme[0]]
    return ListOfValues

def variable_json(variable):
    # schemes 0-9
    schemes = [x[0] for x in eval("bnd.{0}[2]".format(variable))]
    i=0
    variable_json = {}
    for scheme in schemes:
        # properties 2-10
        properties = eval("bnd.{0}[2][{1}]".format(variable, i))
        properties = properties[1:] #remove name Node:['Node','Node',...]
        PropertiesValues = {prop:ListOfValues(variable,i,prop) for prop in properties}
        variable_json.update({scheme:PropertiesValues})
        i += 1
    return {variable:variable_json}

def bnd_json(variables):
    # variables 15
    bnd_json = {}
    for variable in variables:
        bnd_json.update(variable_json(variable))
    if 'ProgramVersion' in variables:
        bnd_json['ProgramVersion'] = bnd.ProgramVersion[0][0][2].strip()
    return bnd_json

bnd_json = bnd_json(bnd.Outputs)

import json
save = False
if save:
    with open('BND.json', 'w+') as json_file:
        json.dump(bnd_json, json_file, indent=4)
else: #print
    print(json.dumps(bnd_json, indent=4))