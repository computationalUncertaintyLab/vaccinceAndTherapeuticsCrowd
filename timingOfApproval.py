#mcandrew

import sys

from mods.data import data
from mods.plots import mm2inch

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import textwrap

def grabMonths(bins):
    dts = []
    ids = []

    for id,b in enumerate(bins):
        b = pd.to_datetime(b)
        month = b.month
        yr    = b.year

        dt = "{:04d}-{:02d}".format(yr,month)
        if dt not in dts:
            ids.append(id)
            dts.append(dt)
    return ids,dts

def convert2date(x,fmt="%Y-%m-%d %H:%M:%S"):
    from datetime import datetime as dt
    return dt.strptime(x.split(".")[0],fmt).date()

import datetime

from scipy.interpolate import interp1d as spline

if __name__ == "__main__":

    d = data("./consensusPredictionData")
    predictions = d.importPredictions()

    d = data("./analysisData/")
    quantiles   = d.importQuantiles()

    toaQids = d.timingOfApprovalQids()

    toaPreds  = predictions.loc[ toaQids ]
    toaQuants = quantiles.loc[toaQids]
    toaQuants["value"] = toaQuants["value"].astype("datetime64[ns]")

    gd = data("./consensusPredictionData/")
    indivForecasts = gd.importIndividualForecasts()

    resolutions = indivForecasts.reset_index()
    resolutions = resolutions[["qid","resolution"]].drop_duplicates().set_index(["qid"])

    plt.style.use("fivethirtyeight")
    fig,axs = plt.subplots(1,2)

    ax=axs[0]

    whenApproved = toaQuants.loc[[4640,4822],:] 

    i = 0
    colors = ["blue","red"]
    for qid,subset in whenApproved.groupby(whenApproved.index):

        for lo,hi in [ ("0.05","0.95"),("0.25","0.75") ]:
            low,high = subset.loc[subset["quantile"]==lo,"value"].values, subset.loc[subset["quantile"]==hi,"value"].values
            ax.plot( [i]*2, [low,high], lw=10, alpha=0.35,color=colors[i] )
        med = subset.loc[subset["quantile"]=="0.5","value"].values
        ax.scatter([i],[med],s=35,color=colors[i])
        i+=1
    
    ax.axhline(pd.to_datetime("2020-12-11"), color="black",linestyle="--",lw=2)
    ax.text(1.,0.1225,"Truth",fontsize=10,va="bottom",ha="right",transform=ax.transAxes)
    
    ax.tick_params(which="both",labelsize=8)
    ax.set_ylabel("Predicted time of approval of COVID-19 vaccine",fontsize=10)
    ax.set_xlabel("Survey issued",fontsize=10)

    ax.set_xticks([0,1])
    ax.set_xticklabels(["2020-06","2020-07"],fontsize=8)

    ax.set_xlim(-0.5,1.5)
    ax.set_ylim(pd.to_datetime("2020-06-01"),pd.to_datetime("2024-12-31"))


    ax.text(0.01,0.99
            ,"\n".join(textwrap.wrap("When will a SARS-CoV-2 vaccine candidate be approved for use in the United States or European Union?",37))
                       ,ha="left",va="top",fontsize=10,transform=ax.transAxes)
    
    ax = axs[1]
    normalAndEUA = toaQuants.loc[[5054,5055,5288,5289],:] 

    fromQID2x = {5054:0.1,5055:0.2, 5288:0.7, 5289:0.8}

    i=0
    colors = ["blue","red"]
    for qid,subset in normalAndEUA.groupby(normalAndEUA.index):
        x = fromQID2x[qid]

        for lo,hi in [ ("0.05","0.95"),("0.25","0.75") ]:
            low,high = subset.loc[subset["quantile"]==lo,"value"].values, subset.loc[subset["quantile"]==hi,"value"].values

            ax.plot( [x]*2, [low,high], lw=10, alpha=0.35,color=colors[i%2] )
                
        med = subset.loc[subset["quantile"]=="0.5","value"].values
        ax.scatter([x],[med],s=35,color=colors[i%2])
        i+=1


    toa5055 = toaPreds.loc[5055]
    toa5055["bin"] = toa5055.bin.astype("datetime64")
    
    minbin, maxbin = min(toa5055["bin"]), max(toa5055["bin"])
    truth1 = minbin + resolutions.loc[5055,"resolution"]*(maxbin-minbin)

    toa5289 = toaPreds.loc[5289]
    toa5289["bin"] = toa5289.bin.astype("datetime64")
    
    minbin, maxbin = min(toa5289["bin"]), max(toa5289["bin"])
    truth2 = minbin + resolutions.loc[5289,"resolution"]*(maxbin-minbin)
    
    ax.axhline(truth2, color="black",linestyle="--",lw=2)
    ax.text(1.,0.1225,"Truth",fontsize=10,va="bottom",ha="right",transform=ax.transAxes)

    
    ax.tick_params(which="both",labelsize=8)
    ax.set_xlabel("Survey issued",fontsize=10)

    ax.set_xticks([0.15,0.75])
    ax.set_xticklabels(["2020-08","2020-09"],fontsize=8)

    ax.set_xlim(-0.5,1.5)

    ax.set_ylim(pd.to_datetime("2020-06-01"),pd.to_datetime("2024-12-31"))

    ax.text(0.01,0.99
            ,"\n".join(textwrap.wrap("When will a SARS-CoV-2 vaccine candidate be approved for use in the US through",37))
                       ,ha="left",va="top",fontsize=10,transform=ax.transAxes)

    ax.text(0.1,0.40,"Normal\n approval\n process",fontsize=10,ha="center",va="center",transform=ax.transAxes,color="blue")
    ax.plot([0.15,0.275],[0.35,0.30],color="blue",lw=1,transform=ax.transAxes)

    ax.text(0.145,0.80,"Emergency\n authorization",fontsize=10,ha="center",va="center",transform=ax.transAxes,color="red")
    ax.plot([0.15,0.325],[0.765,0.70],color="red",lw=1,transform=ax.transAxes)


    
    def mm2inch(x):
        return x/25.4
    w = mm2inch(183)
    fig.set_size_inches(w,w/1.5)
    fig.set_tight_layout(True)

    plt.savefig("timingOfApproval_2panel.png",dpi=350)
    plt.close()
