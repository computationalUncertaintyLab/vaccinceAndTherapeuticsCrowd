#mcandrew

import sys

import numpy as np
import pandas as pd

from mods.consensusTools import buildconsensus
from mods.data import data


def createConsensusData(c,d):
    densityvalues = []
    values = d["scaledBin"].unique()
    for value in values:
        consensusDensityValue = c(value)
        densityvalues.append(consensusDensityValue)
    return values,densityvalues

if __name__ == "__main__":

    gd = data("./consensusPredictionData/")
    d = gd.importIndividualForecasts()

    consenses = {"qid":[],"scaledBin":[],"dens":[],"expert":[]}
    for (qid,subset) in d.groupby([d.index]):
        def findNewestPrediction(x):
            times = sorted(x.time.unique())
            newestTime = times[-1]

            return x.loc[x.time==newestTime]

        recentPredictions = subset.groupby(["standin_id"]).apply( findNewestPrediction ).drop(columns=["standin_id"]).reset_index() # select the individual's most recent prediction
 
        for expert in [0,1,2]:
            if expert == 2:
                expertSpecificPredictions = recentPredictions
            else:
                expertSpecificPredictions = recentPredictions.loc[recentPredictions.expert==expert]

            if not len(expertSpecificPredictions):
                continue
                
            c = buildconsensus(expertSpecificPredictions,"scaledBin","dens")
            c.build() # build consensus interpolating function

            values,consDensityValues = createConsensusData(c,recentPredictions)

            N = len(values)
            consenses["qid"].extend( [qid]*N )
            consenses["expert"].extend( [expert]*N )
            consenses["scaledBin"].extend( values )
            consenses["dens"].extend( consDensityValues )
    consenses = pd.DataFrame(consenses)
    consenses.to_csv("./consensusPredictionData/expertSpecificConsensusPreds.csv",index=False)
