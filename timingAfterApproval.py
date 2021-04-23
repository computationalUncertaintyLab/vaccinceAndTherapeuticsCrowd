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

import datetime

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



if __name__ == "__main__":

    d = data("./consensusPredictionData")
    predictions = d.importPredictions()

    d = data("./analysisData/")
    quantiles   = d.importQuantiles()

    taaQids = d.timingAfterApprovalQids()

    taaPreds  = predictions.loc[ taaQids ]
    taaQuants = quantiles.loc[taaQids]
    

    plt.style.use("fivethirtyeight")

    top    = plt.GridSpec(4,1,top=0.95,hspace=0.3,height_ratios=[5,1,5,1])
    bottom = plt.GridSpec(4,1,top=0.95,hspace=0.5,height_ratios=[5,1,5,1])
    fig = plt.figure()#,axs = plt.subplots(3,1, gridspec_kw = {"height_ratios":[5,1,5]})

    ax=fig.add_subplot(top[0])

    preds = predictions.loc[4641]
    preds["bin"] = preds["bin"].astype("datetime64[ns]")

    quants = quantiles.loc[4641]
    quants["value"] = quants["value"].astype("datetime64[ns]")

    ax.set_xlim(pd.to_datetime("2020-06-01"),pd.to_datetime("2023-12-01"))
    
    ax.plot( preds["bin"], preds["cprobs"], lw=2)

    ax.tick_params(which="both",labelsize=8)

    ax.set_ylabel("Cumulative dens. value",fontsize=10)

    ax.text(0.01,0.99, "\n".join(textwrap.wrap("When will the first SARS-CoV-2 vaccine to be approved in the US or EU be administered to >100k people?",35))
            ,ha="left",va="top",transform=ax.transAxes,fontsize=10)
    
    ax=fig.add_subplot(top[1])
   
    for (lo,hi) in [("0.05","0.95"),("0.25","0.75")]:
        l,h = quants.loc[ quants["quantile"] == lo,"value" ].values,quants.loc[ quants["quantile"] == hi,"value" ].values
        ax.plot( [l,h], [0.50]*2, lw=10, color="blue",alpha=0.30)
    m = quants.loc[ quants["quantile"] == "0.5","value" ].values
    ax.scatter(m,0.5,s=30,color="blue")

    ax.set_xticklabels([])

    ax.set_xlim(pd.to_datetime("2020-06-01"),pd.to_datetime("2023-12-01"))

    ax.tick_params(which="both",labelsize=8)
    ax.set_yticks([])

    #5th
    ax.text( quants.loc[quants["quantile"]=="0.05","value"].values ,0.50, "5th",ha="right",va="center",fontsize=8)

    #95th
    ax.text( quants.loc[quants["quantile"]=="0.95","value"].values ,0.50, "95th",ha="left",va="center",fontsize=8)

    # 50th
    ax.text( quants.loc[quants["quantile"]=="0.5","value"].values ,0.55, "50th",ha="center",va="bottom",fontsize=8)

    # 75th
    ax.text( quants.loc[quants["quantile"]=="0.75","value"].values ,0.55, "75th",ha="center",va="bottom",fontsize=8)

    # 25th
    ax.text( quants.loc[quants["quantile"]=="0.25","value"].values ,0.55, "25th",ha="center",va="bottom",fontsize=8)

  
    ax.set_ylim(0.4,0.6)
    
    ax=fig.add_subplot(top[2])
    
    subset = taaPreds.loc[[5058,5059]]
    subset["bin"] = subset.bin.astype("float")
    
    i=0
    colors=["purple","red"]
    for qid,sub in subset.groupby(subset.index):
        ax.plot(sub["bin"],sub["cprobs"],color=colors[i],alpha=0.75,lw=2)
        i+=1

    ax.set_xticks(np.arange(0,100+1,10))
    ax.set_xlim(0,100)
    ax.tick_params(which="both",labelsize=8)

    ax.set_ylabel("Cumulative dens. value",fontsize=10)

    ax.text(0.50,0.05, "\n".join(textwrap.wrap("How many weeks after approval will the first 100 million doses of the first US- or EU- approved SARS-CoV-2 vaccine candidate",45))
            ,ha="left",va="bottom",transform=ax.transAxes,fontsize=10)

    ax.text(8,0.8,"DNA/RNA platform",fontsize=10, ha="left",va="center",color="purple")
    ax.plot([17,20],[0.75,0.55],lw=1,color="purple")
    
    ax.text(21,0.1,"Viral vector platform",fontsize=10, ha="left",va="center",color="red")
    ax.plot([31,28],[0.2,0.375],lw=1,color="red")
    
    ax=fig.add_subplot(top[3])

    quants = quantiles.loc[[5058,5059]]
    quants["value"] = quants["value"].astype("float")

    i=0
    fromi2y={0:0.25,1:0.75}
    for qid,subQuant in quants.groupby(quants.index):
        for (lo,hi) in [("0.05","0.95"),("0.25","0.75")]:
            l,h = subQuant.loc[ subQuant["quantile"] == lo,"value" ].values,subQuant.loc[ subQuant["quantile"] == hi,"value" ].values
            ax.plot( [l,h], [fromi2y[i]]*2, lw=10, color=colors[i],alpha=0.30)
        m = subQuant.loc[ subQuant["quantile"] == "0.5","value" ].values
        ax.scatter(m,fromi2y[i],s=30,color=colors[i])
        i+=1
    ax.set_ylim(0,1)

    ax.set_xticks(np.arange(0,100+1,10))
    ax.set_xlim(0,100)
    ax.tick_params(which="both",labelsize=8)
 
    ax.set_xticklabels([]) 
    #ax.set_xlim(pd.to_datetime("2020-06-01"),pd.to_datetime("2023-12-01"))


   
    ax.tick_params(which="both",labelsize=8)
    ax.set_yticks([])

    w = mm2inch(183)
    fig.set_size_inches(w,w/1.5)

    plt.savefig("./figs/timingAfterApproval.pdf") 
    plt.savefig("./figs/timingAfterApproval.png",dpi=350)
    plt.close()
