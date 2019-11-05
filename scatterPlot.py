# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 21:04:29 2019

@author: ugo
"""

import numpy as np
import sys
import json
import os

wd = os.getcwd()
#wd = "/home/ugo/Documents/CURIE/python_javascript/"

table_file = wd + "/data/counts_raw.tab"
tmp = np.genfromtxt(table_file, delimiter = "\t", dtype = 'str')
table_colnames = tmp[0,].tolist()
table = tmp[1:len(tmp),]

description_file = wd + "/data/description_data.tab"
tmp = np.genfromtxt(description_file, delimiter = "\t", dtype = None, comments='##')
description_colnames = tmp[0,].tolist()
description_data = tmp[1:len(tmp),]


#samples = ['Dal80_P_MYC_IP-1', 'Dal80_P_MYC_IP-2']
#Types = ['gene', 'mRNA', 'snoRNA']
#scale = 'log2'
#count_type = 'densities'
#normalized = "True"

samples = sys.argv[1]
samples = samples.split(",") 
Types = np.unique(table[:,1])
scale = sys.argv[2]
count_type = sys.argv[3]
normalized = sys.argv[4]

if normalized == "True":
    normalized = True
else:
    normalized = False

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

type_ind = ['']*len(Types)
for i in range(0,len(Types)):
    type_ = Types[i]
    type_ind[i] = np.where(table[:,table_colnames.index('Type')]==type_)[0]

data = ['']*(len(Types)+1)
min_lim = 0
max_lim = 0

for i_type in range(0,len(Types)):

    table_ = table[type_ind[i_type],:]

    exprs = [0]*2
    exprs[0] = np.array([0]*np.shape(table_)[0])
    exprs[1] = np.array([0]*np.shape(table_)[0])
    
    for i_sample in [0,1]:   
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
        if scale == 'log':
            exprs[i_sample] = np.log2(exprs[i_sample])
    
    is_finite = ((exprs[0] != float('-inf')).astype('float') 
             + (exprs[1] != float('-inf')).astype('float') - 1) > 0
    exprs[0] = exprs[0][is_finite]
    exprs[1] = exprs[1][is_finite] 
    
    if max_lim < max([max(exprs[0]), max(exprs[1])]):
        max_lim = max([max(exprs[0]), max(exprs[1])])
    if min_lim > min([min(exprs[0]), min(exprs[1])]):
        min_lim = min([min(exprs[0]), min(exprs[1])])
        
    data[i_type] = {
        'x': exprs[0].tolist(),
        'y': exprs[1].tolist(),
        'mode': 'markers',
        'type': 'scatter',
        'name': Types[i_type],
        'text': table_[:,5].tolist(),
        'marker': { 'size': 8 },
        'hoverinfo' : "all"
        }
 
data[len(data)-1] = {
    'x' : [min_lim - (max_lim - min_lim)*0.2,
           max_lim + (max_lim - min_lim)*0.2],
    'y' : [min_lim - (max_lim - min_lim)*0.2,
           max_lim + (max_lim - min_lim)*0.2],
    'mode' : 'lines',
    'line' : { 'color' : 'Black',
               'width' : 1},
    'showlegend' : False           
} 
# layout
s1 = samples[0] + " " + count_type
s2 = samples[1] + " " + count_type
if scale == "log":
    s1 = "log2 " + s1
    s2 = "log2 " + s2
if normalized:
    s1 = "normalized " + s1
    s2 = "normalized " + s2
else:
    s1 = "raw " + s1
    s2 = "raw " + s2
    
layout = {
    'xaxis':{
        'title': { 'text' : s1 }
    },
    'yaxis':{
        'title': { 'text' : s2 }
    },
    'hovermode' : 'closest',
    'margin': { 
        'l': 50,
        'r': 25,
        'b': 50,
        't': 25
    }
}

res = [data, layout]

print(json.dumps(res, separators = (",", ":")))
