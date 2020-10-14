#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class plotDist(object):

    def __init__(self,d,fig,ax):
        self.d = d

        self.fig = fig
        self.ax  = ax

    def drawDensity(self):
        nbins = len(self.d)
        try:
            ax.plot(self.d.bin.astype(float), self.d.dens,lw=2.)
            ax.fill_between(self.d.bin.astype(float), [0]*nbins, self.d.dens,alpha = 0.50)
        except:
            ax.plot(self.d.bin, self.d.dens,lw=2.)
            ax.fill_between(self.d.bin, [0]*nbins, self.d.dens,alpha = 0.50)
        
        self.formatAx()
        
    def formatAx(self):
        self.ax.tick_params(labelsize=6.)
        self.ax.set_ylim(0,self.ax.get_ylim()[-1])

        self.ax.set_ylabel("Probability Density Function")
        
    def formatXticksForDates(self):
        reformattedList = []
        for dat in self.d.bin:
            dat = pd.to_datetime(dat)
            rdat = "{:04d}/{:02d}".format(int(dat.year),int(dat.month))
            reformattedList.append(rdat)

        numAndLabel = []
        for n,rdat in enumerate(reformattedList):
            if n==0:
                numAndLabel.append( (n,rdat) )
                n=0
                currentRdat = rdat
            else:
                if rdat == currentRdat:
                    continue
                else:
                    numAndLabel.append( (n,rdat) )
                    currentRdat = rdat
                    
        nums,labels = zip(*numAndLabel)
        self.ax.set_xticks(nums)
        self.ax.set_xticklabels(labels,rotation=90)

    def thinXticks(self):
        from matplotlib.ticker import FormatStrFormatter
        self.ax.set_xticks( ax.get_xticks()[::20])
        self.ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    def sizeFig(self):
        def mm2inch(x):
            return x/25.4
        w = mm2inch(183)
        
        self.fig.set_size_inches(w,w/1.6)
        self.fig.set_tight_layout(True)

    def addQuestionText(self,txt):
        import textwrap
        s = "\n".join(textwrap.wrap(text=txt,width=50))
        self.ax.text(x=0.01,y=0.99,s=s,fontsize=10,ha="left",va="top",transform=ax.transAxes)

    def outputGraph(self):
        qid =self.d.iloc[0].qid 
        surveyNum = self.d.iloc[0].surveynum

        plt.savefig( "./figs/probDensity__Survey{:d}_QID_{:04d}.pdf".format(surveynum,qid) )
        plt.close()
        
if __name__ == "__main__":

    plt.style.use("fivethirtyeight")
    consensusData = pd.read_csv("./consensusPredictionData/predictiondata.csv")
    qidData = pd.read_csv("./consensusPredictionData/qdata.csv")

    for (surveynum,qid),data in consensusData.groupby(["surveynum","qid"]):
        print(qid)

        questionData = qidData.loc[qidData.qid==qid]
        
        fig,ax = plt.subplots()

        plot = plotDist(data,fig,ax)
        plot.drawDensity()

        qtext = str(questionData.question.values[0])
        if "when" in qtext.lower():
            try:
                plot.formatXticksForDates()
            except:
                pass
        else:
            if len(ax.get_xticks())>20:
                pass
                #print("think")
                #plot.thinXticks()
            else:
                pass

        plot.addQuestionText(qtext)
        plot.sizeFig()
        plot.outputGraph()
