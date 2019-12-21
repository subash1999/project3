import pandas as pd
import numpy as np

def series_df_to_numpy(series_matrix : pd.DataFrame):
    return series_matrix[series_matrix != "ID_REF"].to_numpy()

