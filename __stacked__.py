import os,sys
import time
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, SelectPercentile, SelectFdr, SelectFpr, SelectFwe
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import RFE,RFECV
from sklearn.feature_selection import chi2,f_classif, mutual_info_classif
from sklearn.model_selection import ParameterGrid, GridSearchCV
from sklearn.svm import LinearSVC, NuSVC, SVC
from sklearn.linear_model import LogisticRegression,LassoCV, Lasso
from sklearn.ensemble import ExtraTreesClassifier, BaggingClassifier, VotingClassifier, RandomForestClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import PCA, NMF
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB, BernoulliNB
from sklearn.metrics import  accuracy_score,auc,average_precision_score,roc_auc_score, recall_score,f1_score, log_loss, fbeta_score, confusion_matrix, precision_recall_curve,classification_report
from xgboost import XGBClassifier
from tpot import TPOTClassifier
from ReliefF import ReliefF
import seaborn as sns
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE,SMOTENC,ADASYN, BorderlineSMOTE, KMeansSMOTE, SVMSMOTE,RandomOverSampler
from imblearn.combine import SMOTETomek, SMOTEENN
from sklearn.preprocessing import Normalizer,normalize
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,BaggingClassifier,ExtraTreesClassifier,GradientBoostingClassifier,StackingClassifier,VotingClassifier
from sklearn.feature_selection import SelectKBest, chi2, f_classif, mutual_info_classif
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.naive_bayes import BernoulliNB, ComplementNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pickle
from sklearn.model_selection import ParameterGrid
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from matplotlib import pyplot
import time

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    
from multiprocessing import Process,Pool,Manager

from preprocessing.Normalize import Normalize
import helper.SeriesHelper as series_helper

print("import completed")

X_train,X_test,y_train,y_test = Normalize().get_train_test()

print("train imported from normal ")

def add_pickle(obj,filename):
    with open(filename+'.pickle', 'wb') as config_dictionary_file:
        pickle.dump(obj,config_dictionary_file)

def get_scores(model,temp_X_train,temp_y_train,temp_X_test,temp_y_test):
 
    xtr = temp_X_train
    xte = temp_X_test
    ytr = temp_y_train
    yte = temp_y_test

    
    model = model.fit(xtr,temp_y_train)
    # knn = MLPClassifier().fit(xtr,temp_y_train)
    pred = model.predict(xte)

    acc  = accuracy_score(temp_y_test,pred)
    prec = average_precision_score(temp_y_test,pred)
    recall = recall_score(temp_y_test,pred)
    f1 = f1_score(temp_y_test,pred)
    roc_auc = roc_auc_score(temp_y_test,pred)

    return [acc,prec,recall,f1,roc_auc]

def job(args):
    try : 
        i = args[0]
        scores = args[1]
        temp_X_train = args[2]
        temp_y_train = args[3] 
        temp_X_test = args[4]
        temp_y_test = args[5]

        best  = SelectKBest(k=i,score_func=chi2).fit(temp_X_train,temp_y_train)
        xtr = best.transform(temp_X_train)
        ytr = temp_y_train
        xte = best.transform(temp_X_test)
        yte = temp_y_test
        mlp = LinearDiscriminantAnalysis()
        scores.append([i,"chi2"]+get_scores(mlp,xtr,ytr,xte,yte))

        best  = SelectKBest(k=i,score_func=f_classif).fit(temp_X_train,temp_y_train)
        xtr = best.transform(temp_X_train)
        ytr = temp_y_train
        xte = best.transform(temp_X_test)
        yte = temp_y_test
        mlp = LinearDiscriminantAnalysis()
        scores.append([i,"f_classif"]+get_scores(mlp,xtr,ytr,xte,yte))

        best  = SelectKBest(k=i,score_func=mutual_info_classif).fit(temp_X_train,temp_y_train)
        xtr = best.transform(temp_X_train)
        ytr = temp_y_train
        xte = best.transform(temp_X_test)
        yte = temp_y_test
        mlp = LinearDiscriminantAnalysis()
        scores.append([i,"mutual_info_classif"]+get_scores(mlp,xtr,ytr,xte,yte))

        print("Done process ",i," of 1000 ",len(scores)/3," of 1000")

    except Exception as e:
        print("Exception ::: ",e)

if __name__ == "__main__":
    st = time.time()
    # optimizing k for of selectkbest for boderline  
    borderline = BorderlineSMOTE(random_state=27,k_neighbors=30,n_jobs=5,m_neighbors=10)
    temp_X_train, temp_y_train = borderline.fit_sample(X_train, y_train)
    temp_X_test,temp_y_test = borderline.fit_sample(X_test, y_test)

    std_scale = normalize(temp_X_train)
    temp_X_train = normalize(temp_X_train)
    temp_X_test = normalize(temp_X_test)

    scores = Manager().list()
    
    args = []
    # for i in range(1,temp_X_train.shape[1],1):
    for i in [921,21,36]:
        args.append([i,scores,temp_X_train,temp_y_train,temp_X_test,temp_y_test])
    
    p  = Pool(processes=6)
    p.map(job,args)

    add_pickle(list(scores),"__stacked_lda__py__comparision_")

    print("total time required : ",time.time()-st)

        
        

