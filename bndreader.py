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
        self.filepath = filepath
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

def Output_schemesf(bnd, Output):
    return getattr(bnd, Output)[0]

def Output_contentsf(bnd, Output):
    return getattr(bnd, Output)[1]

def PropertyValues(bnd, Output, SchemeNr, Property):
        Output_contents = Output_contentsf(bnd, Output)
        Output_scheme = Output_schemesf(bnd, Output)[SchemeNr]
        index = Output_scheme.index(Property)
        ListOfValues = [Output_content[index] for Output_content in Output_contents if Output_content[0] == Output_scheme[0]]
        return ListOfValues

def Output_to_json(bnd, Output):
    Output_scheme_names = [x[0] for x in Output_schemesf(bnd, Output)]
    SchemeNr=0
    Output_json = {}
    for Output_scheme_name in Output_scheme_names:
        Output_scheme = Output_schemesf(bnd, Output)[SchemeNr]
        PropertiesValues = {Property:PropertyValues(bnd, Output, SchemeNr, Property) for Property in Output_scheme[1:]}
        Output_json.update({Output_scheme_name:PropertiesValues})
        SchemeNr += 1
        #print(Output, "-", SchemeNr) #test how many schemes are in each output
    return Output_json

def bnd_json(bnd):
    bnd_json = {Output:Output_to_json(bnd, Output) for Output in bnd.Outputs}
    bnd_json['ProgramVersion'] = bnd.ProgramVersion[1][0][2].strip()
    return bnd_json

def save_as_json(filepath):
    bnd = parser(filepath)
    from os.path import splitext 
    filename = splitext(filepath)[0]
    with open(filename+'.json', 'w+') as file:
        from json import dump
        dump(bnd_json(bnd), file, indent=4)
        print(filename+'.json saved')