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
    
    safetyQids = d.safetyQids()
    safety = predictions.loc[ safetyQids ]

    gd = data("./consensusPredictionData/")
    indivForecasts = gd.importIndividualForecasts()

    resolutions = indivForecasts.reset_index()
    resolutions = resolutions[["qid","resolution"]].drop_duplicates().set_index(["qid"])

    plt.style.use("fivethirtyeight")
    fig,axs = plt.subplots(2,3,gridspec_kw={"height_ratios":[5,1]})

    ax=axs[0,0]

    statSignBen = safety.loc[4642]
    dats = [ convert2date(x) for x in statSignBen.bin]
    ax.plot(dats , statSignBen.dens.values, lw=2 )

    ax.tick_params(which="both",labelsize=6)
    
    ids,dts = grabMonths(statSignBen.bin)

    ax.set_xlim(convert2date(dts[0],"%Y-%m"), convert2date(dts[-1],"%Y-%m"))

    xticks = [convert2date(x,"%Y-%m") for x in dts][::6]
    ax.set_xticks(xticks)
    ax.set_xticklabels([ x if i%2 else "" for i,x in enumerate(xticks)])

    ax.set_ylabel("Consensus probability density",fontsize=10)
    ax.text(0.05,0.99,s="\n".join(textwrap.wrap("When a COVID-19 therapy will show a significant survival benefit",25))
            ,ha="left",va="top",transform=ax.transAxes,fontsize=10)

    ax.set_xlim(convert2date(dts[0],"%Y-%m") - datetime.timedelta(days=30)
                , convert2date(dts[-1],"%Y-%m") + datetime.timedelta(days=30))


    minbin, maxbin = min(dats), max(dats)
    truth = minbin + resolutions.loc[4642,"resolution"]*(maxbin-minbin)

    dats = np.array(dats)
    scaledValues = (dats - minbin) / (maxbin - minbin)
    f = spline( scaledValues, statSignBen.dens.values )

    densTru = f(resolutions.loc[4642,"resolution"])
    ax.scatter( truth,densTru , s=30 )

    ax.plot([truth+datetime.timedelta(weeks=3*4),truth],[0.80*densTru,densTru], lw=1, color="blue")

    ax.text(truth+datetime.timedelta(weeks=3*4), 0.80*densTru, "Truth",fontsize=10,color="blue",va="top")
    
    ax=axs[1,0]
    quants = quantiles.loc[4642]

    dates = []
    for x in quants.value:
        date = convert2date(x)
        dates.append(date)
    quants["date"] = dates
    quants = quants.set_index("quantile")

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

    quantiles2Use = [ convert2date(x) for x in quants.loc[["0.1","0.25","0.5","0.75","0.9"]].value]

    ax.plot([ quantiles2Use[0]  , quantiles2Use[-1]]   ,[0.5]*2, lw=10, alpha=0.3,color="blue" )
    ax.plot([ quantiles2Use[1]  , quantiles2Use[-2]]   ,[0.5]*2, lw=5 , alpha=0.3, color="blue")
    ax.scatter( quantiles2Use[2], [0.5]*1           ,s=30 , alpha=1., color="blue")
    
    ax.set_xlim(convert2date(dts[0],"%Y-%m") - datetime.timedelta(days=30)
                , convert2date(dts[-1],"%Y-%m") + datetime.timedelta(days=30))

    ax.set_xticks([convert2date(x,"%Y-%m") for x in dts[::6]])
    
    ax.set_xticklabels([])
    ax.set_yticks([])

    ax.set_ylim([0.25,0.75])

    
    ax.plot([quantiles2Use[0] - datetime.timedelta(days=10) , quantiles2Use[0]],[ 0.45, 0.50]
            ,color = "blue", lw=1)
    ax.text( quantiles2Use[0] - datetime.timedelta(days=20)
             ,0.40
             ,"10th pct",
             ha="right", color="blue",fontsize=9 )


    ax.plot([quantiles2Use[1] - datetime.timedelta(days=1) , quantiles2Use[1]],[ 0.60, 0.52]
            ,color = "blue", lw=1)
    ax.text( quantiles2Use[1] - datetime.timedelta(days=60)
             ,0.61
             ,"25th",
             ha="left", color="blue",fontsize=9 )

    ax.plot([quantiles2Use[2] - datetime.timedelta(days=1) , quantiles2Use[2]],[ 0.40, 0.48]
            ,color = "blue", lw=1)
    ax.text( quantiles2Use[2] - datetime.timedelta(days=0)
             ,0.41
             ,"50th",
             ha="left", va="top", color="blue",fontsize=9 )

    ax.plot([quantiles2Use[3] - datetime.timedelta(days=1) , quantiles2Use[3]],[ 0.40, 0.48]
            ,color = "blue", lw=1)
    ax.text( quantiles2Use[3] - datetime.timedelta(days=0)
             ,0.41
             ,"75th",
             ha="left", va="top", color="blue",fontsize=9 )

    ax.plot([quantiles2Use[4] + datetime.timedelta(days=10) , quantiles2Use[4]],[ 0.64, 0.55]
            ,color = "blue", lw=1)
    ax.text( quantiles2Use[4] + datetime.timedelta(days=10)
             ,0.61
             ,"90th",
             ha="left", color="blue",fontsize=9 )

    colors = ["blue","red",'black']
    ypos = [0.33,0.66,0.99]
    platformQids = [4828,4829,5060]
    legends = ["Antiviral","Monoclonal antibody","Orally admin."]
    for i,qid in enumerate( platformQids ):
        platform = safety.loc[qid]

        ax = axs[0,1]
        ax.plot( [ convert2date(x) for x in platform.bin], platform.dens.values, lw=2, color= colors[i],label=legends[i] )

        ax.tick_params(which="both",labelsize=6)

        ids,dts = grabMonths(statSignBen.bin)

        ax.set_xlim(convert2date(dts[0],"%Y-%m") - datetime.timedelta(days=30)
                , convert2date(dts[-1],"%Y-%m") + datetime.timedelta(days=30))
 
        xticks = [convert2date(x,"%Y-%m") for x in dts][::6]
        ax.set_xticks(xticks)
        ax.set_xticklabels([ x if i%2 else "" for i,x in enumerate(xticks)])
        
        ax = axs[1,1]
        quants  = quantiles.loc[qid].set_index("quantile")
        quantiles2Use = [ convert2date(x) for x in quants.loc[["0.1","0.25","0.5","0.75","0.9"]].value]
        
        ax.plot( [ quantiles2Use[0]  , quantiles2Use[-1]], [ypos[i]]*2 , lw=10, alpha=0.3, color= colors[i]  )
        ax.plot( [ quantiles2Use[1]  , quantiles2Use[-2]], [ypos[i]]*2 , lw=5 , alpha=0.3, color= colors[i]  )
        ax.scatter( [ quantiles2Use[2]], [ypos[i]]*1 , s=30 , alpha=0.3, color= colors[i]  )

        ax.set_xlim(convert2date(dts[0],"%Y-%m") - datetime.timedelta(days=60)
                , convert2date(dts[-1],"%Y-%m") + datetime.timedelta(days=60))
 

        ax.set_xticks([convert2date(x,"%Y-%m") for x in dts[::6]])
        
        ax.set_xticklabels([])
        ax.set_yticks([])

        ax.set_ylim([0,1.25])


    ax=axs[0,1]
    ax.text(0.05,0.99,s="\n".join(textwrap.wrap("Significant survival benefit by platform",25))
            ,ha="left",va="top",transform=ax.transAxes,fontsize=10)
    ax.legend(loc="right",fontsize=9,frameon=False,bbox_to_anchor = (1.,0.70))
    
    saeIds =[5291,5292]
    
    colors = ["blue","red"]
    ypos = [0.33,0.66]
    legends = ["Normal approval","Emergency approval"]
    for i,qid in enumerate( saeIds):
        sae = safety.loc[qid]
        sae["bin"] = sae.bin.astype(float)
        
        ax = axs[0,2]
        ax.plot(  sae.bin.values, sae.dens.values, lw=2, color= colors[i], label = legends[i] )

        ax.set_xticks([0,0.25,0.50,0.75,1.0])
        ax.set_xlim(0,1.1)
        
        ax.tick_params(which="both",labelsize=6)

        ax = axs[1,2]
        quants  = quantiles.loc[qid].set_index("quantile")
        quantiles2Use = [ float(x) for x in quants.loc[["0.1","0.25","0.5","0.75","0.9"]].value]

        ax.plot( [ quantiles2Use[0]  , quantiles2Use[-1]], [ypos[i]]*2 , lw=10, alpha=0.3, color= colors[i]  )
        ax.plot( [ quantiles2Use[1]  , quantiles2Use[-2]], [ypos[i]]*2 , lw=5 , alpha=0.3, color= colors[i]  )
        ax.scatter( [ quantiles2Use[2]], [ypos[i]]*1 , s=30 , alpha=0.3, color= colors[i]  )

        ax.set_xticks([0,0.25,0.50,0.75,1.0])
        ax.set_xlim(0,1.1)
        
        ax.set_xticklabels([])
        ax.set_yticks([])

        ax.set_ylim([0,1.])
        
    ax = axs[0,2]
    ax.legend(loc="right",fontsize=9,frameon=False,bbox_to_anchor = (0.95,0.75))

    ax.text(0.05,0.99,s="\n".join(textwrap.wrap(r"$\geq$ 10 SAEs within 1 year of approval",25))
            ,ha="left",va="top",transform=ax.transAxes,fontsize=10)
    
    w = mm2inch(183)
    
    fig.set_tight_layout(True)
    fig.set_size_inches(w,w/1.6)

    plt.savefig("./safety3panel.png",dpi=350)
    plt.close()
