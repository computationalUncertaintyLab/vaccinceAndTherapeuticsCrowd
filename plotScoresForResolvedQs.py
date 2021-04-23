#mcandrew

import sys
import numpy as np
import pandas as pd

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

import seaborn as sns

from mods.data import data
from mods.plots import mm2inch


def plotData(individualRanks,consRanks,ax,W,legend,txtlabel):
    from textwrap import wrap
    
    sns.stripplot(x="qid",y="rank"
                  ,hue="expert"
                  ,dodge=True
                  ,data=individualRanks
                  ,palette = {0:"red",1:"blue"},ax=ax)

    for _ in ax.collections:
        _.set_label(s=None)   
    
    sns.boxplot(x="qid",y="rank"
                  ,hue="expert"
                  ,dodge=True
                  ,data=individualRanks
                  ,linewidth=1
                  ,fliersize=0
                  ,palette = {0:"red",1:"blue"},ax=ax)

    for patch in ax.artists:
        r, g, b, a = patch.get_facecolor()
        patch.set_facecolor((r, g, b, .3))


    ls = ["Trained forecaster","Subject matter expert"]
    for l,patch in zip(ls,ax.patches):
        patch.set_label(l)
        
 
        
    def fromqid2order(x):
        x = x.sort_values("qid")
        x["order"] = np.arange(0,len(x))
        return x
    consRanks = consRanks.groupby(["expert"]).apply(fromqid2order).drop(columns=["expert"]).reset_index()

    palette = {0:"red",1:"blue",2:"black"}
    markers = ["d","s","x"]
    labels = ["Consensus of trained forecasters", "Consensus of subject matter experts","Consensus of all forecasters"]
    for expert in [0,1,2]:
        expertid= expert+900
        subset = consRanks.loc[consRanks.standin_id==expertid]

        if expert == 0:
            offset = -0.20
        elif expert==1:
            offset = 0.20
        elif expert == 2:
            offset = 0
        ax.scatter( subset["order"]+offset, subset["rank"],s=35, marker=markers[expert], color = palette[expert], edgecolors="black", alpha=0.80,label=labels[expert] )


    ax.tick_params(which="both",labelsize=8)
    ax.set_xlabel("")

    ax.set_ylabel("Scaled rank",fontsize=10)

    ax.set_yticks([0,0.25,0.50,0.75,1.0])
    ax.set_ylim(-0.025,1.050)

    fromtick2label = {4638:r"SARS-CoV-2 vaccine $\geq 70$% efficacy"
                      ,4642:"When will a COVID-19 therapeutic show a statistical significant survival benefit"
                      ,4643:"Num. of SARS-CoV-2 vaccine candidates in human trials by 2020-08-01"
                      ,5055 :"Date vaccine is approved (Aug.)"
                      ,5057:"Efficacy of first vaccine approved through EUA"
                      ,5289:"Date vaccine is approved (Sept.)"}
    lbls = []

    for x in ax.get_xticklabels():
        x = int(x.get_text())
        lbl = "\n".join(wrap(fromtick2label[x],W))
        lbls.append(lbl)
    ax.set_xticklabels(lbls)

    ax.text(0,1.01,txtlabel,transform=ax.transAxes,ha="left",va="center",fontsize=10,weight="bold")
    
    if legend:
        leg = ax.legend( loc="upper center",fontsize=10,ncol=3, bbox_to_anchor=(1.1,1.35),frameon=False, handletextpad = 0.075, labelspacing=0.01, columnspacing=0.15 )
    else:
        ax.get_legend().remove()

if __name__ == "__main__":


    gd = data("./consensusPredictionData/")
    individualScores = gd.importIndividualScores().reset_index()
    consensusScores  = gd.importConsensusScores().reset_index()
    consensusScores["standin_id"] = consensusScores.expert+900
    
    # rank scores
    def rankforecasters(x):
        x["rank"] = x.logscore.rank() / len(x)
        return x
    individualAndConsScores = individualScores.append(consensusScores)
    individualAndConsRanks = individualAndConsScores.groupby(["qid"]).apply(rankforecasters)

    individualRanks = individualAndConsRanks.loc[individualAndConsRanks.standin_id<900]
    consRanks = individualAndConsRanks.loc[individualAndConsRanks.standin_id>=900]
    
    plt.style.use("fivethirtyeight")
    fig,axs = plt.subplots(2,2)

    groupedQids = [ [4638,5057],[4642],[5055,5289],[4643]  ]

    Ws = [20,40,20,40]
    legends = [True,False,False,False]

    textLbls = ["Efficacy","Safety","Timing of approval","Number of candidates"]
    for qids,ax,w,leg,txt in zip(groupedQids,axs.flatten(),Ws,legends,textLbls):
        d = individualRanks.loc[ individualRanks.qid.isin(qids) ]
        dCons = consRanks.loc[consRanks.qid.isin(qids)]

        x = plotData(d,dCons,ax,w, leg, txt)
        
   
    w = mm2inch(183)
    fig.set_size_inches(w,w/1.6)

    plt.subplots_adjust(hspace=0.275)
    #fig.set_tight_layout(True)
    
    plt.savefig("./scores.pdf")
    plt.savefig("./scores.png",dpi=350)
    plt.savefig("./scores.tiff",dpi=350)
    



