#mcandrew

import sys
import numpy as np
import pandas as pd

from helperfunctions import data

if __name__ == "__main__":

    """ This code analyzes data for Table1. 
        The number of predictions, questions asked, comments, made etc are startified by survey number
    """

    predictions, qdata, forecasters = data.data().importdata()

    numberOfQuestionsAsked = qdata.groupby(["surveynum"]).apply(len)

    numberOfPredictionsMade = qdata.groupby(["surveynum"]).apply(sum)["numOfPredictions"]
    numberOfCommentsMade    = qdata.groupby(["surveynum"]).apply(sum)["numcomments"]
    numberOfVotesMade       = qdata.groupby(["surveynum"]).apply(sum)["numvotes"]
