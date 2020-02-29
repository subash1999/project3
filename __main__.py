# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import pandas as pd
import numpy as np
import os,time,sys
import pickle
from sklearn.model_selection import train_test_split


# %%
from preprocessing.Normalize import Normalize
import helper.SeriesHelper as series_helper


# %%
normal_matrix = Normalize().get_normalized_data()


# %%
cols = normal_matrix.columns
index = normal_matrix.index
X = normal_matrix.to_numpy()
y = series_helper.get_relapse_value_from_series_matrix(normal_matrix)


# %%
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)


# %%
from sklearn.feature_selection import SelectKBest, SelectPercentile, SelectFdr, SelectFpr, SelectFwe
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import RFE,RFECV
from sklearn.feature_selection import chi2,f_classif, mutual_info_classif
from sklearn.model_selection import ParameterGrid, GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression,LassoCV
from sklearn.ensemble import ExtraTreesClassifier, BaggingClassifier
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV


# %%
score_func = [chi2,f_classif,mutual_info_classif]
k = [num for num in range(100,2050,50)]
percentile = [perc for perc in range(5,55,4)]
alpha = [alpha/1000 for alpha in range(0,55,5)]
penalty = ['l1','l2']
estimator = [LinearSVC(penalty=x,dual=False) for x in penalty] + [LogisticRegression(penalty=x,dual=False) for x in penalty] + [LassoCV(cv=10),ExtraTreesClassifier(bootstrap=True,n_jobs=4),ExtraTreesClassifier(n_jobs=4),BaggingClassifier(bootstrap=True,n_jobs=4),BaggingClassifier(n_jobs=4)]


# %%
# feature selection
select_k_best_grid = [{'score_func': score_func,'k': k}]
select_percentile_grid = [{'score_func': score_func,'percentile': percentile}]
select_fdr_grid = [{'score_func': score_func,'alpha': alpha}]
select_fpr_grid = [{'score_func': score_func,'alpha': alpha}]
select_fwe_grid = [{'score_func': score_func,'alpha': alpha}]
# doesnot goes with the GridSearchCV, cross_val_score
select_from_model_grid = [{'estimator' : estimator}]
rfe_grid  = [{'estimator' : estimator,'n_features_to_select' : k, 'step' : [50]}]
rfecv_grid = [{'estimator' : estimator, 'min_features_to_select' : [100], 'cv' : [10],'n_jobs' : [4]}]


# %%
param_grid = [
# {
#     'feature_selection': [SelectFdr()],
#     'feature_selection__score_func': select_fdr_grid[0]['score_func'],
#     'feature_selection__alpha' : select_fdr_grid[0]['alpha'], 
#     'model' : estimator  
# },
# {
#     'feature_selection': [SelectFpr()],
#     'feature_selection__score_func': select_fpr_grid[0]['score_func'],
#     'feature_selection__alpha' : select_fpr_grid[0]['alpha'], 
#     'model' : estimator  
# },
# {
#     'feature_selection': [SelectFwe()],
#     'feature_selection__score_func': select_fwe_grid[0]['score_func'],
#     'feature_selection__alpha' : select_fwe_grid[0]['alpha'], 
#     'model' : estimator  
# },
{
    'feature_selection': [SelectKBest()],
    'feature_selection__score_func': select_k_best_grid[0]['score_func'],
    'feature_selection__k' : select_k_best_grid[0]['k'], 
    # 'feature_selection__dual' : [False], 
    'model' : estimator
},
{
    'feature_selection': [SelectPercentile()],
    'feature_selection__score_func': select_percentile_grid[0]['score_func'],
    'feature_selection__percentile' : select_percentile_grid[0]['percentile'], 
    'model' : estimator  
},

]


# %%
pipeline = Pipeline(steps = [('feature_selection',SelectKBest()),('model',estimator[0])])


# %%
parameter = ParameterGrid(param_grid)


# %%
grid_search = GridSearchCV(pipeline,param_grid=param_grid,cv=10)


# %%
grid_search.fit(X_train,y_train)


# %%


