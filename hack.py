import pandas as pd
import numpy as np
from scipy import stats as st
from scipy.special import stdtrit
def create_df(path) -> pd.DataFrame:
    return pd.read_csv(path)

def get_t_stat(df,column,null_value):
    
    return st.ttest_1samp(df[column],null_value) # (t score, prob)

def get_critical_value(df,p):
    return stdtrit(df,1-p)

def get_desired_mean(df,column,p,h_null):
    critical_val = get_critical_value(len(df.index) - 1 ,p)
    return critical_val * (df[column].std()/np.sqrt(len(df.index))) + h_null

def refine(df,column,h_null,threshold,left=True):
    desired_mean = get_desired_mean(df,"a",.05,34.5)
    t_star = get_critical_value(len(df.index) - 1,.05)
    cur_t = get_t_stat(df,column,h_null)[0]
    step = desired_mean/100
    n = len(df.index)
    print(f"t_star={t_star} cur_t={cur_t}")
    while (left and cur_t > t_star) or (not left and cur_t < t_star):
        cur_t = get_t_stat(df,column,h_null)[0]
        print(f"cur_t:{cur_t}")
        row_to_modify = np.random.randint(0,n)
        multiplier = 1
        if cur_t > t_star and left:
            multiplier = -1    
        df.iloc[row_to_modify][column] += step * multiplier
    return df
            
        
if __name__ == "__main__":
    df = pd.DataFrame({"a":[32.5,34.5,37.3,35.6,36.5]})
    
    new = refine(df,"a",34.5,.05,False)
    print(get_t_stat(new,"a",34.5))