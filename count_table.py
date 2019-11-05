# -*- coding: utf-8 -*-
"""
Created on Mon May 13 03:19:20 2019

@author: ugo
"""

import numpy as np
import sys
import json
import os

wd = os.getcwd()
#wd = "/home/ugo/python_browser/for_server"

table_file = wd + "/data/counts_raw_short.tab"
tmp = np.genfromtxt(table_file, delimiter = "\t", dtype = 'str')
table_colnames = tmp[0,].tolist()
table = tmp[1:len(tmp),]

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

#Types
Types = sys.argv[3]
if Types != "all":
    type_ind = np.where(table[:,table_colnames.index('Type')]==Types)[0]

# count type : readcount or densities
count_type = sys.argv[4]

# scale
scale = sys.argv[5]

# normalization : True or False
normalized = sys.argv[6]
if normalized == "True":
    normalized = True
else:
    normalized = False   
    
# sort by
sort_by = sys.argv[7]

which_sort_by = -1

if plot_type == "exprs":
    for i in range(0, len(samples)):
        if samples[i] == sort_by:       
            which_sort_by = i
else:
    which_sort_by = int(sort_by)

# sorting options
sort_sens = sys.argv[8]

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

# get expression 
if plot_type == "exprs":
    if Types != "all":
        table_ = table[type_ind,]
    else:
        table_ = table
    tmp = table_[:,0:9]
    for i_sample in range(0, len(samples)):
        exprs = get_exprs(which_samples_ = which_samples[i_sample], table_ = table_)
        tmp = np.insert(tmp, len(tmp[0]), exprs, axis = 1)
    if which_sort_by != -1:
        sorted_ind = tmp[:,(9 + which_sort_by)].astype(float).argsort()
        if sort_sens == "up":
            tmp = tmp[sorted_ind,:]
        else:
            if sort_sens == "down":
                tmp = tmp[sorted_ind[::-1],:]
    table_out = tmp
else:
    if Types != "all":
        table_ = table[type_ind,]
    else:
        table_ = table
    tmp = table_[:,0:9]
    for i_ratio in range(0, 2):
        if i_ratio == 0:
            ratio = get_ratio(which_samples__ = which_samples, table__ = table_)
        else:
            ratio = get_ratio(which_samples__ = [which_samples[1],which_samples[0]], 
                              table__ = table_)
        tmp = np.insert(tmp, len(tmp[0]), ratio.tolist(), axis = 1)
    if which_sort_by != -1:
        sorted_ind = tmp[:,(9 + which_sort_by)].astype(float).argsort()
        if sort_sens == "up":
            tmp = tmp[sorted_ind,:]
        else:
            if sort_sens == "down":
                tmp = tmp[sorted_ind[::-1],:]
            
    table_out = tmp

print(json.dumps(table_out.tolist(), separators = (",", ":"))) 