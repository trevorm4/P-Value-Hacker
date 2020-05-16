import pandas as pd
import numpy as np
from scipy import stats as st

def create_df(path) -> pd.DataFrame:
    return pd.read_csv(path)

def get_t_stat(df,column,null_value):
    return st.ttest_1samp(df[column],null_value) # (t score, prob)

def get_critical_value(df,p):
    return st.t.ppf(1-p,df=df)

def get_desired_mean(df,column,p,h_null):
    critical_val = get_critical_value(len(df.index),p)
    return critical_val * (df[column].std()/np.sqrt(len(df.index))) + h_null

def refine(df,column,h_null,threshold):
    cur_t = get_t_stat(df,column,h_null)[0]
    t_star = get_critical_value(df,.05)
    step = desired_mean/100
    n = len(df.index)
    while cur_t > threshold:
        cur_t = get_t_stat(df,column,h_null)[0]
        row_to_modify = np.random.randint(0,n)
        multiplier = 1
        if cur_t > p_star:

if __name__ == "__main__":
    df = #..
    desired_mean = get_desired_mean(df,"one",.05,34.5)