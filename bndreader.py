import networkx as nx 
from os import startfile
from os.path import splitext 

def preprocess(fragment):
    fragment = fragment.strip().split("\n")
    content, scheme = [], []
    for line in fragment:
        line=line.strip()
        if "#" not in line[0] and "!" not in line[0]:
            content.append(line.split(","))
        else:
            if "! <" in line[0:3] and "! <#" not in line[0:4]:
                char_to_replace = {'! ': '','# ': '',' #' : '', '<':'', '>':''}
                for key, value in char_to_replace.items():
                    line = line.replace(key, value)
                scheme.append(line.split(","))
    return scheme, content 

class parser:
    def __init__(self, filepath):
        file_content = open(filepath, "r").read()
        separator = "! ==============================================================="
        Outputs = file_content.split(separator)

        self.ProgramVersion             = preprocess(Outputs[0])  #scheme count
        self.Nodes                      = preprocess(Outputs[1])  #1
        self.SuspiciousNodes            = preprocess(Outputs[2])  #1
        self.BranchLists                = preprocess(Outputs[3])  #2
        self.SupplyAirPaths             = preprocess(Outputs[4])  #3-4
        self.ReturnAirPaths             = preprocess(Outputs[5])  #3-4
        self.OutdoorAirNodes            = preprocess(Outputs[6])  #0-1
        self.ComponentSets              = preprocess(Outputs[7])  #1
        self.PlantLoops                 = preprocess(Outputs[8])  #6
        self.CondenserLoops             = preprocess(Outputs[9])  #6
        self.ControlledZones            = preprocess(Outputs[10]) #3
        self.ZoneEquipmentLists         = preprocess(Outputs[11]) #2
        self.AirLoopHVACs               = preprocess(Outputs[12]) #9
        self.ParentNodeConnections      = preprocess(Outputs[13]) #1
        self.NonParentNodeConnections   = preprocess(Outputs[14]) #1
        
        self.Outputs = ['ProgramVersion','Nodes', 'SuspiciousNodes', 'BranchLists',
            'SupplyAirPaths', 'ReturnAirPaths', 'OutdoorAirNodes',
            'ComponentSets', 'PlantLoops', 'CondenserLoops', 
            'ControlledZones', 'ZoneEquipmentLists', 'AirLoopHVACs',
            'ParentNodeConnections', 'NonParentNodeConnections']
        
    def bnd_json(self):
        bnd_json = {Output:parser.output_to_json(self, Output) for Output in self.Outputs}
        bnd_json['ProgramVersion'] = self.ProgramVersion[1][0][2].strip()
        return bnd_json

    def output_schemesf(self, Output):
        return getattr(self, Output)[0]

    def output_contentsf(self, Output):
        return getattr(self, Output)[1]

    def property_values(self, Output, SchemeNr, Property):
            Output_contents = parser.output_contentsf(self, Output)
            Output_scheme = parser.output_schemesf(self, Output)[SchemeNr]
            index = Output_scheme.index(Property)
            ListOfValues = [Output_content[index] for Output_content in Output_contents if Output_content[0] == Output_scheme[0]]
            return ListOfValues

    def output_to_json(self, Output):
        Output_scheme_names = [x[0] for x in parser.output_schemesf(self, Output)]
        SchemeNr=0
        Output_json = {}
        for Output_scheme_name in Output_scheme_names:
            Output_scheme = parser.output_schemesf(self, Output)[SchemeNr]
            PropertiesValues = {Property:parser.property_values(self, Output, SchemeNr, Property) for Property in Output_scheme[1:]}
            Output_json.update({Output_scheme_name:PropertiesValues})
            SchemeNr += 1
            #print(Output, "-", SchemeNr) #test how many schemes are in each output
        return Output_json

    def save_bnd_as_json(self, filepath):
        filename = splitext(filepath)[0]
        with open(filename+'.json', 'w+') as file:
            from json import dump
            dump(parser.bnd_json(self), file, indent=4)
            print(filename+'.json saved')

    def graph(self):

        json = parser.bnd_json(self)
        G = nx.Graph()

        ParentNodeConnections = json['ParentNodeConnections']['Parent Node Connection']
        ParentNodeConnectionsEdges = list(zip(ParentNodeConnections['Node Name'], 
                                              ParentNodeConnections['Node ObjectName'])) 

        NonParentNodeConnections = json['NonParentNodeConnections']['Non-Parent Node Connection']
        NonParentNodeConnectionsEdges = list(zip(NonParentNodeConnections['Node Name'], 
                                                 NonParentNodeConnections['Node ObjectName']))
        
        for node, ObjectType in zip(ParentNodeConnections['Node ObjectName'], ParentNodeConnections['Node ObjectType']): 
            G.add_node(node, ObjectType=ObjectType)
        for node, ObjectType in zip(NonParentNodeConnections['Node ObjectName'], NonParentNodeConnections['Node ObjectType']): 
            G.add_node(node, ObjectType=ObjectType)

        G.add_edges_from(ParentNodeConnectionsEdges)                                         
        G.add_edges_from(NonParentNodeConnectionsEdges)

        return G

    def graph_image(self, filepath, open=True):
        import matplotlib.pyplot as plt
        nx.draw(self.graph())
        plt.savefig(splitext(filepath)[0]+'.png')
        if open:
            startfile(splitext(filepath)[0]+'.png')
        plt.close()