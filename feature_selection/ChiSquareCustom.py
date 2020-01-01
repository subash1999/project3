import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2_contingency
import os,sys
sys.path.append(os.path.abspath(""))
sys.path.append(os.path.abspath("../"))
import helper.SeriesHelper as series_helper


class ChiSquare:
    def __init__(self, dataframe):
        self.df = dataframe
        self.p = None #P-Value
        self.chi2 = None #Chi Test Statistic
        self.dof = None
        
        self.dfObserved = None
        self.dfExpected = None
        self.colY = series_helper.get_relapse_value_from_series_matrix(self.df)
    def _print_chisquare_result(self, colX, alpha):
        result = ""
        if self.p<alpha:
            return True
            result="{0} is IMPORTANT for Prediction".format(colX)
        else:
            return False
            result="{0} is NOT an important predictor. (Discard {0} from model)".format(colX)

        print(result)   

    def TestIndependence(self,colX,alpha=0.05):
        X = self.df[colX].astype(str)
        Y = self.colY.astype(str)
        
        self.dfObserved = pd.crosstab(Y,X) 
        chi2, p, dof, expected = stats.chi2_contingency(self.dfObserved.values)
        self.p = p
        self.chi2 = chi2
        self.dof = dof 
        
        self.dfExpected = pd.DataFrame(expected, columns=self.dfObserved.columns, index = self.dfObserved.index)
        
        return self._print_chisquare_result(colX,alpha)
