
def preprocess(text):
    text = text.strip().split("\n")
    return [x.strip() for x in text if "#" not in x[0:2] and "!" not in x[0:2]]

class parser:
    def __init__(self, filepath):

        text = open(filepath, "r").read()
        separator = "! ==============================================================="
        text_list = text.split(separator)

        self.ProgramVersion             = preprocess(text_list[0])
        self.Nodes                      = preprocess(text_list[1])
        self.SuspiciousNodes            = preprocess(text_list[2])
        self.BranchLists                = preprocess(text_list[3])
        self.SupplyAirPaths             = preprocess(text_list[4])
        self.ReturnAirPaths             = preprocess(text_list[5])
        self.OutdoorAirNodes            = preprocess(text_list[6])
        self.ComponentSets              = preprocess(text_list[7])
        self.PlantLoops                 = preprocess(text_list[8])
        self.CondenserLoops             = preprocess(text_list[9])
        self.ControlledZones            = preprocess(text_list[10])
        self.ZoneEquipmentLists         = preprocess(text_list[11])
        self.AirLoopHVACs               = preprocess(text_list[12])
        self.ParentNodeConnections      = preprocess(text_list[13])
        self.NonParentNodeConnections   = preprocess(text_list[14])