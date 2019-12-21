import pandas as pd
import numpy as np
from scipy import stats

class CheckNormal():
    def __init__(self):
        pass
    
    def normal_test(self,alpha : int,series_matrix : pd.DataFrame):
        not_normal = []
        normal = []
        for x in series_matrix.columns[1:]:    
            k2,p = stats.normaltest(list(series_matrix[x]))
            if p < alpha:  # null hypothesis: x comes from a normal distribution
                not_normal.append(x)
                # print("The null hypothesis can be rejected : Not Normal Distribution, P : ",p)
            else:
                normal.append(x)
                # print("The null hypothesis cannot be rejected : Normal Distribution, P : ",p)
        normal_ratio = len(normal)/(len(normal)+len(not_normal))
        not_normal_ratio = len(not_normal)/(len(normal)+len(not_normal))
        return len(normal),len(not_normal)

    

    def shaprio(self,alpha : int,series_matrix : pd.DataFrame):
        not_normal = []
        normal = []
        for x in series_matrix.columns[1:]:    
            k2,p = stats.shapiro(list(series_matrix[x]))
            if p < alpha:  # null hypothesis: x comes from a normal distribution
                not_normal.append(x)
                # print("The null hypothesis can be rejected : Not Normal Distribution, P : ",p)
            else:
                normal.append(x)
                # print("The null hypothesis cannot be rejected : Normal Distribution, P : ",p)
        normal_ratio = len(normal)/(len(normal)+len(not_normal))
        not_normal_ratio = len(not_normal)/(len(normal)+len(not_normal))
        return normal_ratio,not_normal_ratio

    
    def anderson(self,series_matrix : pd.DataFrame):
        not_normal = []
        normal = []
        print("---"*3,"Anderson Normality Check","---"*3)
        for x in series_matrix.columns[1:]:    
            result = stats.anderson(list(series_matrix[x]))
            print('Statistic: %.3f' % result.statistic)
            for i in range(len(result.critical_values)):
                sl, cv = result.significance_level[i], result.critical_values[i]
                if result.statistic < result.critical_values[i]:
                    normal.append(x)
                    print('%.3f: %.3f, data looks normal (fail to reject H0)' % (sl, cv))
                else:
                    not_normal.append(x)
                    print('%.3f: %.3f, data does not look normal (reject H0)' % (sl, cv))
        print("---"*3,"End Anderson Normality Check","---"*3)
        normal_ratio = len(normal)/(len(normal)+len(not_normal))
        not_normal_ratio = len(not_normal)/(len(normal)+len(not_normal))
        return normal_ratio,not_normal_ratio
    
   