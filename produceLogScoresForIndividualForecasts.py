#mcandrew

import sys
from mods.data import data

from mods.probTools import interpolateDensity

import numpy as np
import pandas as pd

if __name__ == "__main__":

    gd = data("./consensusPredictionData/")
    indivForecasts = gd.importIndividualForecasts()

    #forecasts with resolution only
    resCasts = indivForecasts.loc[ ~np.isnan(indivForecasts.resolution) ]

    # most recent prediction
    def mostRecent(x):
        x["time"] = x.time.astype("datetime64[ns]")
        times = x.time.unique()

        return x.loc[x.time==max(times)]
    resRec = resCasts.reset_index().groupby(["standin_id","qid"]).apply(mostRecent)
    resRec = resRec.set_index(np.arange(len(resRec)))

    resRec.to_csv("./consensusPredictionData/mostRecentIndividualPredictions.csv",index=False)
    
    indivScores = {"standin_id":[], "score":[],"surveynum":[],"expert":[],"qid":[]}
    def scoreForecast(forecast):
        f = interpolateDensity(forecast.scaledBin, forecast.dens)
        resolution = forecast.iloc[0]["resolution"]

        logOfDens = f(resolution)

        return pd.Series({"logscore":float(logOfDens)})

    indivScores = resRec.groupby(["qid","standin_id","surveynum","expert"]).apply(scoreForecast)
    indivScores = indivScores.reset_index()

    indivScores.to_csv("./consensusPredictionData/individualScores.csv",index=False)
