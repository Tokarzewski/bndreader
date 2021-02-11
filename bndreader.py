
def preprocess(fragment):
    fragment = fragment.strip().split("\n")
    content, comments, scheme = [], [], []
    for line in fragment:
        line=line.strip()
        if "#" not in line[0] and "!" not in line[0]:
            content.append(line.split(","))
        else:
            comments.append(line.split(","))
            if "! <" in line[0:3] and "! <#" not in line[0:4]:
                char_to_replace = {'! ': '','#': '', '<':'', '>':''}
                for key, value in char_to_replace.items():
                    line = line.replace(key, value)
                scheme.append(line.split(","))
    return content, comments, scheme

class parser:
    def __init__(self, filepath):

        file_conent = open(filepath, "r").read()
        separator = "! ==============================================================="
        fragments = file_conent.split(separator)

        self.ProgramVersion             = preprocess(fragments[0])  #scheme count
        self.Nodes                      = preprocess(fragments[1])  #1
        self.SuspiciousNodes            = preprocess(fragments[2])  #1
        self.BranchLists                = preprocess(fragments[3])  #2
        self.SupplyAirPaths             = preprocess(fragments[4])  #3-4
        self.ReturnAirPaths             = preprocess(fragments[5])  #3-4
        self.OutdoorAirNodes            = preprocess(fragments[6])  #0-1
        self.ComponentSets              = preprocess(fragments[7])  #1
        self.PlantLoops                 = preprocess(fragments[8])  #6
        self.CondenserLoops             = preprocess(fragments[9])  #6
        self.ControlledZones            = preprocess(fragments[10]) #3
        self.ZoneEquipmentLists         = preprocess(fragments[11]) #2
        self.AirLoopHVACs               = preprocess(fragments[12]) #9
        self.ParentNodeConnections      = preprocess(fragments[13]) #1
        self.NonParentNodeConnections   = preprocess(fragments[14]) #1