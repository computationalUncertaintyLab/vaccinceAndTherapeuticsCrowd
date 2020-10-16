import pandas as pd

class data(object):
    def __init__(self):
        predictions = pd.read_csv("./consensusPredictionData/predictiondata.csv")
        qdata       = pd.read_csv("./consensusPredictionData/qdata.csv")
        forecasters = pd.read_csv("./consensusPredictionData/forecasters.csv")

        self.predictions = predictions
        self.qdata = qdata
        self.forecasters = forecasters

    def importdata(self):
        return (self.predictions, self.qdata, self.forecasters)
