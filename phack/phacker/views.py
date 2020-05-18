from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

import pandas as pd
import numpy as np
from scipy import stats as st
from scipy.special import stdtrit

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

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

def isfloatlist(value):
    try:
        possible_list = value.split(',')
        for f in possible_list:
            float(f)
        return True
    except ValueError:
        return False

def index(request):
    if request.method == "POST":
        desired_p = request.POST.get('p')
        hyp = request.POST.get('h')
        possible_csv = request.POST.get('data')
        if len(desired_p) > 0:
            if isfloat(desired_p):
                desired_p = float(desired_p)
                # check for valid p-value
                if desired_p > 1 or desired_p < 0:
                    error = {'err_msg' : "Invalid p-value!"}
                    return render(request, 'failed.html', error)

                # check for valid hypothesis
                if len(hyp) < 0:
                    error = {'err_msg' : "Couldn't find hypothesis!"}
                    return render(request, 'failed.html', error)
                
                if not isfloat(hyp):
                    error = {'err_msg' : "Hypothesis could not be resolved to a float!"}
                    return render(request, 'failed.html', error)

                # check for valid data
                if len(possible_csv) < 0:
                    error = {'err_msg' : "Couldn't find data!"}
                    return render(request, 'failed.html', error)

                if not isfloatlist(possible_csv):
                    error = {'err_msg' : "Data could not be resolved to a list of floats!"}
                    return render(request, 'failed.html', error)            

                data_list = possible_csv.split(',')
                for i in range(len(data_list)):
                    data_list[i] = float(data_list[i])

                df = pd.DataFrame({"a": data_list})
                new = refine(df,"a", float(hyp), float(desired_p), False)
                new_str = ""
                for data in new["a"]:
                    new_str += str(data) + ","
                new_str = new_str[:-1]

                result_context = {'res_data': new_str}
                return render(request, 'result.html', result_context)
            else:
                error = {'err_msg' : "P-value could not be resolved to a float!"}
                return render(request, 'failed.html', error)
        else:
            return redirect('/phacker/failed')
    return render(request, 'index.html', {})

def failed(request):
    error = {'err_msg' : "Couldn't find any input!"}
    return render(request, 'failed.html', error)

def success(request):
    return render(request, 'result.html', {'res_data': "1.03082,49393\n29384.2,98\n22.54,2842.0\n"})