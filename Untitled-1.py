# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from preprocessing.Normalize import Normalize
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math


# %%
n = Normalize()
normal_matrix = n.get_normalized_data()
del n 


# %%
for x in list(normal_matrix.columns):
    l = []
    for y in normal_matrix[x]:
        l.append(10**y)
    normal_matrix[x] = l
normal_matrix.head()


# %%
from FeatureSelection import FeatureSelection
from helper.SeriesHelper import SeriesHelper
s = SeriesHelper()


# %%
f = FeatureSelection()
a = f.select_k_best(normal_matrix.to_numpy(),s.get_relapse_value_from_series_matrix(normal_matrix))


# %%
a = pd.DataFrame(a)
a.shape


# %%
#get correlations of each features in dataset
corrmat = a.corr()
top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
#plot heat map


# %%
g=sns.heatmap(a[top_corr_features].corr(),annot=True,cmap="RdYlGn")
g.show()
