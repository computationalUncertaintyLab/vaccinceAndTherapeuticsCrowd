import pandas as pd

class data(object):
    def __init__(self,root):
        self.root = root

    def importPredictions(self):
        import os
        fil = os.path.join(self.root,"predictiondata.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported predictions")
        return d

    def importQdata(self):
        import os
        fil = os.path.join(self.root,"qdata.csv")
        d = pd.read_csv(fil)
        
        print("Imported Question data")
        return d

    def importForecasters(self):
        import os
        fil = os.path.join(self.root,"forecasters.csv")
        d = pd.read_csv(fil)
        
        print("Imported forecasters")
        return d

    def importQuantiles(self):
        import os
        fil = os.path.join(self.root,"quantilesFromConsensusPredictions.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported forecasters")
        return d

    def importIndividualForecasts(self):
        import os
        fil = os.path.join(self.root,"individualPredictionsLong.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported individual forecasts")
        return d

    def importmostRecentIndividualForecasts(self):
        import os
        fil = os.path.join(self.root,"mostRecentIndividualPredictions.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported individual forecasts")
        return d

    def importExpertSpecificConsensusForecasts(self):
        import os
        fil = os.path.join(self.root,"expertSpecificConsensusPreds.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported expert specific forecasts")
        return d

    def importResolutionData(self):
        import os
        fil = os.path.join(self.root,"resolutiondata.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported resolution data")
        return d

    def importIndividualScores(self):
        import os
        fil = os.path.join(self.root,"individualScores.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported individual scores data")
        return d

    def importConsensusScores(self):
        import os
        fil = os.path.join(self.root,"expertSpecificConsensusScores.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported individual scores data")
        return d
    
    def importRanks(self):
        import os
        fil = os.path.join(self.root,"individualAndConsensusRanks.csv")
        d = pd.read_csv(fil).set_index("qid")
        
        print("Imported individual and consensus ranked scores data")
        return d


    def safetyQids(self):
        return [4642,4828,4829,5060,5291,5292]

    def efficacyQids(self):
        return [4639,4638,4827,4824,4825,4823,5056,5057]

    def timingOfApprovalQids(self):
        return [4640,4822,5054,5055,5288,5289]

    def timingAfterApprovalQids(self):
        return [4641,5058,5059]

      

