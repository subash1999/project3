import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(""))
sys.path.append("../")
from KCrossValidation import KCrossValidation
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectPercentile, chi2, SelectKBest,f_classif

from sklearn import datasets
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

class FeatureSelection():
    def __init__(self):
        pass
    
    def variance_thershold(self,X):
        sel = VarianceThreshold(threshold=(.9 * (1 - .9)))
        return sel.fit_transform(X)

    def select_k_best(self,X,Y):
        # return SelectKBest(chi2).fit_transform(X, Y)
        return SelectPercentile(f_classif, percentile=0.1).fit_transform(X, Y)
    
    def rfe(self):
        # Recursive Feature Elimination
      
        # load the iris datasets
        dataset = datasets.load_iris()
        # create a base classifier used to evaluate a subset of attributes
        model = LogisticRegression()
        # create the RFE model and select 3 attributes
        rfe = RFE(model, 3)
        rfe = rfe.fit(dataset.data, dataset.target)
        # summarize the selection of the attributes
        print(rfe.support_)
        print(rfe.ranking_)
