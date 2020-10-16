#mcandrew

import sys
import numpy as np
import pandas as pd

from helperfunctions import data

if __name__ == "__main__":

    """ This code counts the number of unique experts and trained forecasters who participated in any of the four surveys.
    """

    predictions, qdata, forecasters = data.data().importdata()

    uniqExperts = forecasters.loc[forecasters.expert==1,"forecaster"].drop_duplicates()
    numUniqExperts = len(uniqExperts)
    print("Unique Experts = {:d}".format(numUniqExperts))
    
    uniqTFs     = forecasters.loc[forecasters.tf==1,"forecaster"].drop_duplicates()
    numUniqTFs  = len(uniqTFs)
    print("Unique TFs = {:d}".format(numUniqTFs))
