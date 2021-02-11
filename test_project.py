import bndreader

filepath1 = "Boiler_Convector.bnd"
filepath2 = "DOAS_Preheat.bnd"
filepath3 = "FCU_Boiler_Chiller.bnd"
filepath4 = "PTHP.bnd"

bnd = bndreader.parser(filepath2)

#1 content
#print(bnd.Nodes[0])

#2 comments
#print(bnd.Nodes[1])

#3 scheme
#print(bnd.Nodes[2])

#4
#print(*bnd.AirLoopHVACs[2], sep = "\n")

#5
#print(*bnd.PlantLoops, sep="\n")

#6 test scheme
"""
outputs = {'Nodes':1, 'SuspiciousNodes':1, 'BranchLists':2,
            'SupplyAirPaths':4, 'ReturnAirPaths':4, 'OutdoorAirNodes':1,
            'ComponentSets':1, 'PlantLoops':6, 'CondenserLoops':6, 
            'ControlledZones':3, 'ZoneEquipmentLists':2, 'AirLoopHVACs':9,
            'ParentNodeConnections':1, 'NonParentNodeConnections':1}

for output, value in outputs.items():
    print(output,": ",value, len(eval('bnd.'+str(output)+'[2]')))
"""
#7 show scheme and content 
print("--Scheme--")
print(*bnd.AirLoopHVACs[2], sep = "\n")
print("--Content--")
print(*bnd.AirLoopHVACs[0], sep = "\n")