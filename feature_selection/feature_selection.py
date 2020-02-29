# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython


# %%
# pipeline recommended for the feature selection e.g.
# clf = Pipeline([
#   ('feature_selection', SelectFromModel(LinearSVC(penalty="l1"))),
#   ('classification', RandomForestClassifier())
# ])
# clf.fit(X, y)


# %%
# Change working directory
import os,sys
sys.path.append(os.path.abspath("../"))
sys.path.append(os.path.abspath(""))
# os.chdir("../")


# %%
# ignore warnings
import warnings
warnings.simplefilter("ignore")


# %%
#importing libraries
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
# get_ipython().run_line_magic('matplotlib', 'inline')
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from numpy import set_printoptions
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import chi2
from sklearn.linear_model import Ridge
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import tensorflow as tensorflow
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import VarianceThreshold
from dask import dataframe as dd 
import time

# %%
# get the custom models
from preprocessing.Normalize import Normalize
import helper.SeriesHelper as series_helper


# %%
n = Normalize()
normal_matrix = n.get_normalized_data()


# %%
required_features = 1000


# %%
X = normal_matrix.to_numpy()
y = series_helper.get_relapse_value_from_series_matrix(normal_matrix)

# %% [markdown]
# # Filter Method

# %%
# finding correlation using the pandas dataframe function
def correlation():
    t = time.time()
    print("***** CORRELATION *****")
    ddf = dd.from_pandas(normal_matrix)
    cor = ddf.corr()
    print("***** END CORRELATION TIME : ",time.time()-t," *****")
    return cor
    #Correlation with output variable
    # cor_target = abs(cor[list(normal_matrix.columns)[col_no]])
    #Selecting highly correlated features
    # relevant_features = cor_target[cor_target>0.5]
    # print("Relevent Features : \n",relevant_features)
    # return (corr,relevant_features)

# %% [markdown]
# # Wrapper Methods

# %%
#Backward Elimination
def backward_elimination():    
    print("***** BACKWARD ELIMINATION *****")
    cols = list(normal_matrix.columns)
    pmax = 1
    count = 0
    while (len(cols)>0):
        p= []
        X_1 = normal_matrix[cols]
        X_1 = sm.add_constant(X_1)
        model = sm.Poisson(y,X_1).fit()
        p = pd.Series(model.pvalues.values[1:],index = cols)      
        pmax = max(p)
        feature_with_p_max = p.idxmax()
        if(pmax>0.05):
            cols.remove(feature_with_p_max)
        else:
            break
        print("Count : ",count)
    selected_features_BE = cols
    print("Selected features BE : \n",selected_features_BE)
    return (selected_features_BE)

# %% [markdown]
# # Embedded Method

# %%
# embedded method using lassoCV
def lassoCV():
    reg = LassoCV()
    reg.fit(X, y)
    print("***** LASSO CV *****")
    print("Best alpha using built-in LassoCV: %f" % reg.alpha_)
    print("Best score using built-in LassoCV: %f" %reg.score(X,y))
    coef = pd.Series(reg.coef_, index = X.columns)
    print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other " +  str(sum(coef == 0)) + " variables")
    return (reg)

# %% [markdown]
# # Select K Best

# %%
def f_classif_select_k_best():
    # feature extraction
    test = SelectKBest(score_func=f_classif, k=required_features)
    fit = test.fit(X, y)
    # summarize scores
    set_printoptions(precision=3)
    print("***** SELECT K BEST f_classif*****")
    print(fit.scores_)
    features = fit.transform(X)
    # summarize selected features
    print("summarize selected features f_classif")
    print(features[0:5,:])
    return (features,fit.scores_)


# %%
def chi2_select_k_best():
    # feature extraction
    test = SelectKBest(score_func=chi2, k=required_features)
    fit = test.fit(X, y)
    # summarize scores
    set_printoptions(precision=3)
    print("***** SELECT K BEST chi2*****")
    print(fit.scores_)
    features = fit.transform(X)
    # summarize selected features
    print("summarize selected features chi2")
    print(features[0:5,:])
    return (features,fit.scores_)

# %% [markdown]
# # RFE

# %%
def rfe():
    # Feature extraction
    model = LogisticRegression()
    rfe = RFE(model, required_features)
    fit = rfe.fit(X, y)
    print("***** RFE *****")
    print("Num Features: %s" % (fit.n_features_))
    print("Selected Features: %s" % (fit.support_))
    print("Feature Ranking: %s" % (fit.ranking_))
    return (fit,fit.ranking_)

# %% [markdown]
# # Ridge

# %%
# A helper method for pretty-printing the coefficients
def pretty_print_coefs(coefs, names = None, sort = False):
    if names == None:
        names = ["X%s" % x for x in range(len(coefs))]
    lst = zip(coefs, names)
    if sort:
        lst = sorted(lst,  key = lambda x:-np.abs(x[0]))
    return " + ".join("%s * %s" % (round(coef, 3), name)
                                   for coef, name in lst)


# %%
def ridge():
    ridge = Ridge(alpha=1.0)
    ridge.fit(X,Y)
    print ("Ridge model:", pretty_print_coefs(ridge.coef_))
    return (ridge,ridge.coef_)

# %% [markdown]
# # PCA

# %%
def pca():
    # feature extraction
    pca = PCA(n_components=required_features)
    fit = pca.fit(X)
    # summarize components
    print("Explained Variance: %s" % fit.explained_variance_ratio_)
    print(fit.components_)
    return (fit,fit.components_)

# %% [markdown]
# # Feature Importance

# %%
def feature_importance():
     # feature extraction
    model = ExtraTreesClassifier(n_estimators=required_features)
    model.fit(X, y)
    print("************Feature Importances ************\n",model.feature_importances_)
    return (model,model.feature_importances_)

# %% [markdown]
# # Select From Model

# %%
def select_from_model(model):
    model = SelectFromModel(model, prefit=True)
    X_new = model.transform(X)
    print("Select From Model, New Shape : ",X_new.shape)
    return X_new

# %% [markdown]
# # Variance Threshold

# %%
def variance_thershold(pval = 0.8):
        sel = VarianceThreshold(threshold=(threshold * (1 - threshold)))
        return sel.fit_transform(X)


# %%

