#mcandrew

import sys

from mods.data import data
from mods.plots import mm2inch,stamp

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
    
    efficacyQids = d.efficacyQids()
    efficacy = predictions.loc[ efficacyQids ]

    gd = data("./consensusPredictionData/")
    indivForecasts = gd.importIndividualForecasts()

    resolutions = indivForecasts.reset_index()
    resolutions = resolutions[["qid","resolution"]].drop_duplicates().set_index(["qid"])


    plt.style.use("fivethirtyeight")
    fig,axs = plt.subplots(4,2,gridspec_kw={"height_ratios":[5,1,5,1]})

    ax=axs[0,0]

    thresh = efficacy.loc[4638]
    thresh["bin"] = thresh["bin"].astype('datetime64[ns]')
    ax.plot( thresh.bin.values , thresh.dens.values, lw=2 )

    ax.tick_params(which="both",labelsize=6)
    ax.set_xlim(thresh["bin"].iloc[0]-datetime.timedelta(days=7), thresh["bin"].iloc[-1]+datetime.timedelta(days=7))

    
    ax.set_ylabel("Consensus prob. dens.",fontsize=10)
    ax.text(0.10,0.99,s="\n".join(textwrap.wrap(r"When will a COVID-19 vaccine show $\geq$ 70% efficacy",30))
            ,ha="left",va="top",transform=ax.transAxes,fontsize=10)


    minbin, maxbin = min(thresh.bin.values), max(thresh.bin.values)
    truth = minbin + resolutions.loc[4638,"resolution"]*(maxbin-minbin)

    scaledValues = (thresh.bin.values - minbin) / (maxbin - minbin)
    f = spline( scaledValues, thresh.dens.values )

    densTru = f(resolutions.loc[4638,"resolution"])
    ax.scatter( truth,densTru , s=30 ) 

    ax.text(pd.to_datetime("2020-12-10") + datetime.timedelta(days=14)
            , 2.5*densTru ,"Truth", ha="left", va="center", fontsize=10,color="blue")
    ax.plot([ pd.to_datetime("2020-12-10"), pd.to_datetime("2020-12-10") + datetime.timedelta(days=28)]
            ,[densTru*1.15,  2.*densTru]
            , lw=1
            ,color="blue")
    ax.set_xticks( thresh["bin"].values[10::45]  )
    
    stamp("A.",ax) 


    ax=axs[1,0]
    quants = quantiles.loc[4638]
    quants = quants.set_index("quantile")

    quantiles2Use = [convert2date(x) for x in quants.loc[["0.1","0.25","0.5","0.75","0.9"]].value]

    ax.plot([ quantiles2Use[0]  , quantiles2Use[-1]]   ,[0.5]*2, lw=10, alpha=0.4,color="blue" )
    ax.plot([ quantiles2Use[1]  , quantiles2Use[-2]]   ,[0.5]*2, lw=5 , alpha=0.4, color="blue")
    ax.scatter( quantiles2Use[2], [0.5]*1           ,s=30 , alpha=1., color="blue")

    ax.set_xticklabels([])
    ax.set_yticks([])

    ax.set_ylim([0.25,0.75])

    ax.set_xlim(thresh["bin"].iloc[0]-datetime.timedelta(days=7), thresh["bin"].iloc[-1]+datetime.timedelta(days=7))
    ax.set_xticks( thresh["bin"].values[10::45]  )
    
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

    F = 0.6
    colors = ["blue","red"]
   
    ylim = [0,1.5]
    dy   = 0.9*(ylim[-1]-ylim[0])/len(colors)
    ypos = 0.45 

    platformQids = [5056,5057]
    legends = ["Normal process","Emergency auth."]
    for i,qid in enumerate( platformQids ):
        platform = efficacy.loc[qid]

        ax = axs[2,1]
        domain = [ float(x) for x in platform.bin]
        ax.plot(domain , platform.dens.values, lw=2, color= colors[i],label=legends[i] )

        ax.tick_params(which="both",labelsize=6)

        ax.set_xlim(0,100)
        ax.set_xticks(np.arange(0,100+1,10))
        
        ax = axs[3,1]
        quants  = quantiles.loc[qid].set_index("quantile")
        quantiles2Use = [ float(x) for x in quants.loc[["0.1","0.25","0.5","0.75","0.9"]].value]
        
        ax.plot( [ quantiles2Use[0]  , quantiles2Use[-1]], [ypos]*2 , lw=10*F, alpha=0.4, color= colors[i]  )
        ax.plot( [ quantiles2Use[1]  , quantiles2Use[-2]], [ypos]*2 , lw=5*F , alpha=0.4, color= colors[i]  )
        ax.scatter( [ quantiles2Use[2]], [ypos]*1 , s=30 , alpha=1., color= colors[i]  )

        ypos+=dy
        
        ax.set_xlim(0,100)
        ax.set_xticks(np.arange(0,100+1,10))
       
        ax.set_xticklabels([])
        ax.set_yticks([])

        ax.set_ylim(ylim)

    ax=axs[2,1]

    thisRes = resolutions.loc[5057]
    f = spline(domain , platform.dens.values )
    ax.scatter( 100*thisRes["resolution"], f(100*thisRes["resolution"]), s=30, color="red" ) 

    densTru = f(100*thisRes["resolution"])
    
    ax.text(70*0.99,0.5,"Truth",fontsize=10,ha="right",va="top",color="red")
    ax.plot([70,95*0.99],[densTru, densTru], lw=1, color="red")

    
    ax.text(0.10,0.99,s="\n".join(textwrap.wrap("Efficacy at approval",25))
            ,ha="left",va="top",transform=ax.transAxes,fontsize=10)
    ax.legend(loc="center left",fontsize=9,frameon=False,bbox_to_anchor=(-0.045,0.75),labelspacing=0)
    stamp("D.",ax)
   

    # CHAD OX
    ax=axs[0,1]

    efOx = efficacy.loc[4639]
    ax.plot( efOx["bin"].astype(float).values, efOx.dens.values, lw=2 )

    ax.tick_params(which="both",labelsize=6)
    ax.set_xticks(np.arange(0,100+1,10))
    ax.set_xlim(0,100)
    
    
    ax.text(0.10,0.99,s="\n".join(textwrap.wrap("Efficacy of trial to test Oxford/Astrazeneca ChAdOx1 vaccine",25))
            ,ha="left",va="top",transform=ax.transAxes,fontsize=10)
    stamp("B.",ax)

    ax=axs[1,1]
    quants = quantiles.loc[4639]
    quants = quants.set_index("quantile")

    quantiles2Use = [float(x) for x in quants.loc[["0.1","0.25","0.5","0.75","0.9"]].value]

    ax.plot([ quantiles2Use[0]  , quantiles2Use[-1]]   ,[0.5]*2, lw=10, alpha=0.4,color="blue" )
    ax.plot([ quantiles2Use[1]  , quantiles2Use[-2]]   ,[0.5]*2, lw=5 , alpha=0.4, color="blue")
    ax.scatter( quantiles2Use[2], [0.5]*1           ,s=30 , alpha=1., color="blue")

    ax.set_xticklabels([])
    ax.set_yticks([])

    ax.set_ylim([0.25,0.75])

    ax.set_xticks(np.arange(0,100+1,10))
    ax.set_xlim(0,100)

    
    F = 0.4
    d=0.25
    colors = ["blue","red",'black',"orange"]
  
    ylim = [0,2.5]
    dy   = ( (ylim[-1])-d -(ylim[0]+d) )/len(colors)
    ypos = 0.55 

    platformQids = [4827,4824,4825,4823]
    legends = ["Non-repl viral","Protein subunit","Inact. virus","DNA/RNA"]
    for i,qid in enumerate( platformQids ):
        platform = efficacy.loc[qid]

        ax = axs[2,0]
        ax.plot( [ float(x) for x in platform.bin], platform.dens.values, lw=2, color= colors[i],label=legends[i] )

        ax.tick_params(which="both",labelsize=6)

        ax.set_xlim(0,100)
        ax.set_xticks(np.arange(0,100+1,10))
        
        ax = axs[3,0]
        quants  = quantiles.loc[qid].set_index("quantile")
        quantiles2Use = [ float(x) for x in quants.loc[["0.1","0.25","0.5","0.75","0.9"]].value]
        
        ax.plot( [ quantiles2Use[0]  , quantiles2Use[-1]], [ypos]*2 , lw=10*F, alpha=0.4, color= colors[i]  )
        ax.plot( [ quantiles2Use[1]  , quantiles2Use[-2]], [ypos]*2 , lw=5*F , alpha=0.4, color= colors[i]  )
        ax.scatter( [ quantiles2Use[2]], [ypos]*1 , s=20 , alpha=1., color= colors[i]  )

        ypos+=dy
        
        ax.set_xlim(0,100)
        ax.set_xticks(np.arange(0,100+1,10))
       
        ax.set_xticklabels([])
        ax.set_yticks([])

        ax.set_ylim(ylim)

    ax=axs[2,0]
    ax.text(0.10,0.99,s="\n".join(textwrap.wrap("Efficacy by platform",25))
            ,ha="left",va="top",transform=ax.transAxes,fontsize=10)
    ax.legend(loc="center left",fontsize=9,frameon=False,bbox_to_anchor=(0,0.65),labelspacing=0)

    ax.set_ylabel("Consensus prob. dens.",fontsize=10)

    stamp("C.",ax)
    
    w = mm2inch(183)
    
    fig.set_tight_layout(True)
    fig.set_size_inches(w,w/1.6)

    plt.savefig("./efficacy4panel.png",dpi=350)
    plt.close()
