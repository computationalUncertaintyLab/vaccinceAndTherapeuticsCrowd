#mcandrew;

class buildconsensus( object ):
    def __init__(self,indivpreds,xname,densname):
        self.indivpreds = indivpreds
        self.xname = xname
        self.densname = densname
        
    def build(self):
        import pandas as pd
        import numpy as np
        from scipy.interpolate import interp1d as spline
        
        cons = self.indivpreds.groupby([self.xname]).apply(lambda d: pd.Series({"consdens": np.mean(d[self.densname]) }) )
        f = spline(cons.index,cons.consdens)

        self.consensus = f
        return f
    
    def __call__(self,x):
        return self.consensus(x)

 
