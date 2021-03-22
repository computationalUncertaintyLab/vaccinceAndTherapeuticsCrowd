#mcandrew

import sys
from mods.data import data

from mods.probTools import interpolateDensity

import numpy as np
import pandas as pd

if __name__ == "__main__":

    gd = data("./consensusPredictionData/")
    consForecasts  = gd.importExpertSpecificConsensusForecasts()
    resData        = gd.importResolutionData() 

    consForecasts = consForecasts.merge(resData,left_index=True,right_index=True)
    
    #forecasts with resolution only
    resCasts = consForecasts.loc[ ~np.isnan(consForecasts.resolution) ]

    consScores = {"score":[],"surveynum":[],"expert":[],"qid":[]}

    def scoreForecast(forecast):
        f = interpolateDensity(forecast.scaledBin, forecast.dens)
        resolution = forecast.iloc[0]["resolution"]

        logOfDens = f(resolution)

        return pd.Series({"logscore":float(logOfDens)})

    consScores = resCasts.groupby([resCasts.index,"surveynum","expert"]).apply(scoreForecast)
    consScores = consScores.reset_index()

    consScores.to_csv("./consensusPredictionData/expertSpecificConsensusScores.csv",index=False)
