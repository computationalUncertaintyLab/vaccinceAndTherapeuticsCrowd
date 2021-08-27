#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from mods.data import data
from mods.plots import mm2inch,stamp


if __name__ == "__main__":

    gd = data("./consensusPredictionData/")
    ranks = gd.importRanks()

    ranks["cons"] = 0
    ranks.loc[ranks.standin_id == 900 , "cons"] = 1
    ranks.loc[ranks.standin_id == 901 , "cons"] = 2
    ranks.loc[ranks.standin_id == 902 , "cons"] = 3
    
    consRanks  = ranks.loc[ranks.standin_id>=900]
    indivRanks = ranks.loc[ranks.standin_id<900]

    plt.style.use("fivethirtyeight")
    
    fig,ax =plt.subplots()
   
    sns.stripplot(y="cons",x="logscore",orient="h",data = ranks,ax=ax,edgecolor="k",linewidth=1)
    sns.boxplot(  y="cons",x="logscore",orient="h",data = ranks,ax=ax,linewidth=1,fliersize=0)

    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .5))
    
    
    ax.set_ylabel("")
    ax.tick_params(which="both",labelsize=8)

    ax.set_xticks([0,2,4,6,8])
    plt.subplots_adjust(left=0.185,bottom=0.10)

    ax.set_yticklabels(["Individuals","Consensus\n of\n trained forecasters","Consensus\n of\n experts","Consensus\n of\n all forecasters"],fontsize=10, ha="center")
    ax.tick_params(axis="y",pad=40)

    ax.set_xlabel("Log score",fontsize=10)
    
    w = mm2inch(183)
    fig.set_size_inches(w,w/1.6)

    fig.savefig("scoreSpread.tiff",dpi=300)
    fig.savefig("scoreSpread.png" ,dpi=300)
    fig.savefig("scoreSpread.pdf" ,dpi=300)

    plt.close()
