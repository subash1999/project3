import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(""))
sys.path.append("../")
from KCrossValidation import KCrossValidation
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile, chi2, SelectKBest


class FeatureSelection():
    def __init__(self):
        pass
    
    def variance_thershold(self,X):
        sel = VarianceThreshold(threshold=(.9 * (1 - .9)))
        return sel.fit_transform(X)

    def select_k_best(self,X,Y):
        # return SelectKBest(chi2).fit_transform(X, Y)
        return SelectPercentile(chi2, percentile=0.1).fit_transform(X, Y)
