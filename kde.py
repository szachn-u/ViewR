# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:22:59 2019

@author: ugo
"""

import sys
import numpy as np
from scipy.stats.kde import gaussian_kde
import json
import os

wd = os.getcwd()

# kernel density estimation
def density (data, log, xmin = None, xmax = None):

    if (isinstance(data, np.ndarray) != True):
        data = np.asarray(data)
    
    if (log == True):
        data = np.log2(data + 1)
    
    if(xmin is None):
        min_ = np.trunc(min(data))
    else :
        min_ = xmin
    
    if (xmax is None):
        max_ = np.ceil(max(data))
    else:
        max_ = xmax
        
    kde = gaussian_kde(data)
    
    x = np.linspace(min_,max_,100)
    y = np.array([0]*100, dtype = float)
    for i in range(0,len(x)):
        y[i]=kde(x[i])[0]
    
    res = {'x' : x, 'y' : y}
    return(res)

# counts
table_file = wd + "/data/counts_raw.tab"
tmp = np.genfromtxt(table_file, delimiter = "\t", dtype = 'str')
table_colnames = tmp[0,].tolist()
table = tmp[1:len(tmp),]

# description data
description_file = wd + "/data/description_data.tab"
tmp = np.genfromtxt(description_file, delimiter = "\t", dtype = None)
description_colnames = tmp[0,].tolist()
description_data = tmp[1:len(tmp),]

# get arguments

# plot type
plot_type = sys.argv[1]

# samples
#samples="Dal80_P_MYC_IP,WT_P_MYC_IP"
samples = sys.argv[2]
samples = samples.split(",") 

# count type
count_type = sys.argv[3] 

# normalization
#normalized=True
normalized = sys.argv[4]
if normalized == "True":
    normalized = True
else:
    normalized = False

Types = np.unique(table[:,1])

# which samples
which_samples = ['']
group = ['']
for i in range(0,len(samples)):
    try:
        to_append = [description_data[:,1].tolist().index(samples[i])]
        which_samples.append(to_append)
    except:
        for j in range(0,len(description_data)):
            if description_data[j,6] == samples[i]:
                group.append(j)
            if j == (len(description_data)-1):
                which_samples.append(group[1:len(group)])
                group = ['']

which_samples = which_samples[1:len(which_samples)]

# which Types
type_ind = ['']*len(Types)
for i in range(0,len(Types)):
    type_ = Types[i]
    type_ind[i] = np.where(table[:,table_colnames.index('Type')]==type_)[0]

# get fold-change or exprs
data_list = ['']*(len(Types))

for i_type in range(0,len(Types)):

    table_ = table[type_ind[i_type],:]

    exprs = [0]*len(samples)
    for i in range(0,len(samples)):
        exprs[i] = np.array([0]*np.shape(table_)[0])
    
    for i_sample in range(0,len(samples)):   
        for i in range(0,len(which_samples[i_sample])):
            sample_name = description_data[which_samples[i_sample][i],1]
            ind_col = table_colnames.index(sample_name + " readcount")
            i_exprs = table_[:,ind_col].astype(float)
            if normalized:
                coeff = float(description_data[which_samples[i_sample][i],2])
                i_exprs = i_exprs*coeff
            exprs[i_sample] = exprs[i_sample] + i_exprs
        
        exprs[i_sample] = exprs[i_sample]/len(which_samples[i_sample])
    
    if count_type == "densities":
        l = table_[:,3].astype(float) - table_[:,2].astype(float)
        exprs[i_sample] = exprs[i_sample]/l
    
    if plot_type == "fc":
        data_list[i_type] = np.log2((exprs[0]+1)/(exprs[1]+1))
    else:
        tmp = []
        for j in range(0,len(exprs[0])):
            if exprs[0][j] != 0:
                tmp.append(np.log2(exprs[0][j]))
        data_list[i_type] = tmp

data = ['']*(len(Types))
xmax = np.ceil(max(map(max, data_list)))
xmin = np.floor(min(map(min, data_list)))

# estimate density
for i_type in range(0,len(Types)): 
    dens = density(data_list[i_type], False, xmin = xmin, xmax = xmax)
    data[i_type] = {
        'x': dens['x'].tolist(),
        'y': dens['y'].tolist(),
        'mode': 'lines',
        'type': 'scatter',
        'name': Types[i_type],
        'hoverinfo' : 'none'
        }

# layout


if plot_type == "fc":
    title = "ratio " + samples[0] + " / " + samples[1] 
    if normalized:
        xlab = "normalized log2 fold-change"
    else:
        xlab = "raw log2 fold-change"
else:
    if normalized:
        title = "normalized " + count_type + " for " + samples[0]
        xlab = "normalized log2 " + count_type
    else:
        title = "raw " + count_type + " for " + samples[0]
        xlab = "raw log2 " + count_type
    
layout = {
    'title' : title,
    'xaxis':{
        'title': { 'text' : xlab }
    },
    'yaxis':{
        'title': { 'text' : 'density' }
    },
    'margin': { 
        'l': 50,
        'r': 25,
        'b': 50,
        't': 25
    }
}

res = [data, layout]

print(json.dumps(res, separators = (",", ":")))
