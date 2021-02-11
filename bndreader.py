
def preprocess(text):
    text = text.strip().split("\n")
    content, comments, scheme = [], [], []
    for x in text:
        x=x.strip()
        if "#" not in x[0] and "!" not in x[0]:
            content.append(x.split(","))
        else:
            comments.append(x.split(","))
            if "! <" in x[0:3] and "! <#" not in x[0:4]:
                char_to_replace = {'! ': '','#': '', '<':'', '>':''}
                for key, value in char_to_replace.items():
                    x = x.replace(key, value)
                scheme.append(x.split(","))
    return content, comments, scheme

class parser:
    def __init__(self, filepath):

        text = open(filepath, "r").read()
        separator = "! ==============================================================="
        text_list = text.split(separator)

        self.ProgramVersion             = preprocess(text_list[0])  #scheme count
        self.Nodes                      = preprocess(text_list[1])  #1
        self.SuspiciousNodes            = preprocess(text_list[2])  #1
        self.BranchLists                = preprocess(text_list[3])  #2
        self.SupplyAirPaths             = preprocess(text_list[4])  #3-4
        self.ReturnAirPaths             = preprocess(text_list[5])  #3-4
        self.OutdoorAirNodes            = preprocess(text_list[6])  #0-1
        self.ComponentSets              = preprocess(text_list[7])  #1
        self.PlantLoops                 = preprocess(text_list[8])  #6
        self.CondenserLoops             = preprocess(text_list[9])  #6
        self.ControlledZones            = preprocess(text_list[10]) #3
        self.ZoneEquipmentLists         = preprocess(text_list[11]) #2
        self.AirLoopHVACs               = preprocess(text_list[12]) #9
        self.ParentNodeConnections      = preprocess(text_list[13]) #1
        self.NonParentNodeConnections   = preprocess(text_list[14]) #1