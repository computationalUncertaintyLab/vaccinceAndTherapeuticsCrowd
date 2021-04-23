#mcandrew

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def mm2inch(x):
    return x/25.4

def stamp(s,ax,x=0.01,y=0.99):
    ax.text(x,y,s
            ,weight="bold"
            ,fontsize=10,ha="left",va="top",transform=ax.transAxes)

class plotDist(object):

    def __init__(self,d,fig,ax,outfil):
        self.d = d

        self.fig = fig
        self.ax  = ax

    def drawDensity(self,c):
        nbins = len(self.d)
        binvals = self.d.bin
        ax.fill_between(binvals, [0]*nbins, self.d.dens,alpha = 0.50,color=c)
        ax.plot(binvals, self.d.dens,lw=2.,color=c)
        
        self.formatAx()
        
    def formatAx(self):
        self.ax.tick_params(labelsize=12.)
        self.ax.set_ylim(0,self.ax.get_ylim()[-1])
        self.ax.set_ylabel("Prob Dens",fontsize=10)
        
    def formatXticksForDates(self):
        reformattedList = []
        for dat in self.d.bin:
            dat = pd.to_datetime(dat)
            rdat = "{:04d}/{:02d}".format(int(dat.year),int(dat.month))
            reformattedList.append(rdat)

        #find where the year and month change in the list of all times
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
        self.ax.set_xticks(labels)
        self.ax.set_xticklabels(labels,rotation=90)

    def thinXticks(self):
        from matplotlib.ticker import FormatStrFormatter
        self.ax.set_xticks( ax.get_xticks()[::20])
        self.ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))

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

        plt.savefig( outfil )
        plt.close()
       
def setColorsForPlot(numColors=20):
    plt.style.use('fivethirtyeight')
    
    colors = []
    fig,ax = plt.subplots()
    for x in range(numColors+1):
        ax.plot([0],[0])
    for n,x in enumerate(ax.get_children()):
        if n>numColors:
            break
        colors.append(x.get_color())
    plt.close()
    return colors

if __name__ == "__main__":

    pass
