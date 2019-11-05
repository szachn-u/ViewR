# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:46:25 2019

@author: ugo
"""

import os
import sys
import numpy as np
import json

wd = os.getcwd()
#wd = "/home/ugo/python_browser/for_server"    
    
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
# plot type : exprs or fc
plot_type = sys.argv[1]

if plot_type == "exprs":
    # sample type : main or replicates
    sample_type = sys.argv[2]
    
    if sample_type == "main":
        samples = np.sort(np.unique(description_data[:,6])).tolist()
    else:
        samples = np.sort(np.unique(description_data[:,1])).tolist()          
        
else:
    samples = sys.argv[2]
    samples = samples.split(",")   

# group by : sample or type
group_by = sys.argv[3]

# count type : readcount or densities
count_type = sys.argv[4]

# normalization : True or False
normalized = sys.argv[5]
if normalized == "True":
    normalized = True
else:
    normalized = False   
    
Types = np.unique(table[:,1])
scale = 'log'

# function to get expression values from count table
def get_exprs(which_samples_, table_, 
              count_type_ = count_type, normalized_ = normalized, scale_ = scale,
              description_data_ = description_data, table_colnames_ = table_colnames):      
    exprs = np.array([0]*np.shape(table_)[0])
    for i in range(0,len(which_samples_)):
        sample_name = description_data_[which_samples_[i],1]
        ind_col = table_colnames_.index(sample_name + " readcount")
        i_exprs = table_[:,ind_col].astype(float)
        if normalized:
            coeff = float(description_data_[which_samples_[i],2])
            i_exprs = i_exprs*coeff
        exprs = exprs + i_exprs
    exprs = exprs/len(which_samples_)
    if count_type_ == "densities":
        l = table_[:,3].astype(float) - table_[:,2].astype(float)
        exprs = exprs/l
    if scale_ == 'log':
        tmp = []
        for i in range(0, len(exprs)):
            if (exprs[i] != 0):
                tmp.append(np.log2(exprs[i]))
        exprs = tmp
    return(exprs)

def get_ratio(which_samples__, table__, 
              normalized__ = normalized, scale__ = scale,
              description_data__ = description_data, table_colnames__ = table_colnames):
    exprs1 = get_exprs(which_samples_ = which_samples__[0], table_ = table__,
                       count_type_ = "readcount", normalized_ = normalized__, scale_ = "linear",
                       description_data_ = description_data__, table_colnames_ = table_colnames__)
    exprs2 = get_exprs(which_samples_ = which_samples__[1], table_ = table__,
                       count_type_ = "readcount", normalized_ = normalized__, scale_ = "linear",
                       description_data_ = description_data__, table_colnames_ = table_colnames__)   
    if(scale__ == "log"):
        ratio = np.log2((exprs1 + 1) / (exprs2 + 1))
    else:
        ratio = (exprs1 + 1) / (exprs2 + 1)
    
    return(ratio)

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

# get expression 
if plot_type == "exprs":
    if group_by == 'Samples':
        data = ['']*len(Types)
        for i_type in range(0,len(Types)):
            y = []
            x = []
            for i_sample in range(0,len(samples)):
                exprs = get_exprs(which_samples_ = which_samples[i_sample], table_ = table[type_ind[i_type],:])
                y.extend(exprs)
                x.extend([samples[i_sample]]*len(exprs))

            data[i_type] = {
                'y' : y,
                'x' : x,
                'name' : Types[i_type],
                'type' : 'box'
                }
    
    if group_by == 'Types':
        data = ['']*len(samples)
        for i_sample in range(0, len(samples)):
            x = []
            y = []
            for i_type in range(0, len(Types)):
                exprs = get_exprs(which_samples_ = which_samples[i_sample], table_ = table[type_ind[i_type],:])
                y.extend(exprs)
                x.extend([Types[i_type]]*len(exprs))

            data[i_sample] = {
                'y' : y,
                'x' : x,
                'name' : samples[i_sample],
                'type' : 'box'
                }
else:
    data = ['']*len(Types)
    for i_type in range(0,len(Types)):
        y = []
        x = []
        ratio = get_ratio(which_samples__ = which_samples, table__ = table[type_ind[i_type],:])
        y.extend(ratio.tolist())
        x.extend(['']*len(ratio))
        data[i_type] = {
            'y' : y,
            'x' : x,
            'name' : Types[i_type],
            'type' : 'box'
        }

if plot_type == "exprs":
    ylab = scale + " " + count_type
else:
    ylab = scale + " " + samples[0] + " / " + samples[1]
          
layout = {
    'yaxis': {
        'title': ylab
    },
    'boxmode': 'group',
    'margin': { 
        'l': 50,
        'r': 25,
        'b': 50,
        't': 25
    }
} 
   
res = [data, layout]

print(json.dumps(res, separators = (",", ":")))   
