# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 21:04:29 2019

@author: ugo
"""

##########
#  libs  #
##########

import sys
import numpy as np
import os
import json
import pyBigWig

###############
#  functions  #   
###############        
def plotRectangle(start, stop, yPos, color, xref, yref):
    res = {
      'type': 'rect',
      'x0': start,
      'y0': yPos-0.1,
      'x1': stop,
      'y1': yPos + 1,
      'line': {
        'color': color
      },
      'fillcolor': color,
      'xref': xref,
      'yref':yref
    }
    return(res)

def plotArrow(start, stop, yPos, xSpan, strand, color, xref, yref):
    if strand == "+":
        if xSpan*0.01 < (stop-start):
            path = (' M ' + str(start) + ',' + str(yPos-0.01) + 
                   ' L ' + str(start) + ',' + str(yPos+0.01) +
                   ' L ' + str(stop - xSpan*0.01) + ',' + str(yPos+0.01) +
                   ' L ' + str(stop - xSpan*0.01) + ',' + str(yPos+0.05) +
                   ' L ' + str(stop) + ',' + str(yPos) +
                   ' L ' + str(stop - xSpan*0.01) + ',' + str(yPos-0.05) +
                   ' L ' + str(stop - xSpan*0.01) + ',' + str(yPos-0.01) + 
                   ' Z ')
        else:
            path = (' M ' + str(start) + ',' + str(yPos-0.01) + 
                   ' L ' + str(start) + ',' + str(yPos+0.01) +
                   ' L ' + str(stop) + ',' + str(yPos) +
                   ' Z ')
    else:
        if xSpan*0.01 < (stop-start):
            path = (' M ' + str(stop) + ',' + str(yPos-0.01) + 
                   ' L ' + str(stop) + ',' + str(yPos+0.01) +
                   ' L ' + str(start + xSpan*0.01) + ',' + str(yPos+0.01) +
                   ' L ' + str(start + xSpan*0.01) + ',' + str(yPos+0.05) +
                   ' L ' + str(start) + ',' + str(yPos) +
                   ' L ' + str(start + xSpan*0.01) + ',' + str(yPos-0.05) +
                   ' L ' + str(start + xSpan*0.01) + ',' + str(yPos-0.01) + 
                   ' Z ')
        else:
            path = (' M ' + str(stop) + ',' + str(yPos-0.01) + 
                   ' L ' + str(stop) + ',' + str(yPos+0.01) +
                   ' L ' + str(start) + ',' + str(yPos) +
                   ' Z ')
    res = {
      'type': 'path',
      'path': path,
      'fillcolor': color,
      'line': {
        'color': color
      },
      'xref': xref,
      'yref':yref
    }
    return(res)
     
def plotBox(start, stop, yPos, xSpan, strand, color, xref, yref):
    if strand == "+":
        if xSpan*0.01 < (stop-start):
            path = (' M ' + str(start) + ',' + str(yPos-0.1) + 
                   ' L ' + str(start) + ',' + str(yPos+0.1) +
                   ' L ' + str(stop - xSpan*0.01) + ',' + str(yPos+0.1) +
                   ' L ' + str(stop) + ',' + str(yPos) +
                   ' L ' + str(stop - xSpan*0.01) + ',' + str(yPos-0.1) + 
                   ' Z ')
        else:
            path = (' M ' + str(start) + ',' + str(yPos-0.1) + 
                   ' L ' + str(start) + ',' + str(yPos+0.1) +
                   ' L ' + str(stop) + ',' + str(yPos) +
                   ' Z ')
    else:
        if xSpan*0.01 < (stop-start):
            path = (' M ' + str(stop) + ',' + str(yPos-0.1) + 
                   ' L ' + str(stop) + ',' + str(yPos+0.1) +
                   ' L ' + str(start + xSpan*0.01) + ',' + str(yPos+0.1) +
                   ' L ' + str(start) + ',' + str(yPos) +
                   ' L ' + str(start + xSpan*0.01) + ',' + str(yPos-0.1) + 
                   ' Z ')
        else:
            path = (' M ' + str(stop) + ',' + str(yPos-0.1) + 
                   ' L ' + str(stop) + ',' + str(yPos+0.1) +
                   ' L ' + str(start) + ',' + str(yPos) +
                   ' Z ')
    res = {
      'type': 'path',
      'path': path,
      'fillcolor': color,
      'line': {
        'color': color
      },
      'xref': xref,
      'yref':yref
    }
    return(res)    

def get_signal(chr_, start_, stop_, files_, samples_, strand_, scale_, coeff_):
    signal = np.array([0]*(stop_-start_))    
    n_samples = np.shape(samples_)[0]
    if np.shape(coeff_) == ():
        coeff_ = [coeff_]
    for i in range(0,n_samples):
        if strand_ == 'both':
            for str_ in ['F', 'R']:
                file = wd + "/data/" + files_[i] + "_" + chr + "_" + str_ + "_strand_raw.bw"
                bw = pyBigWig.open(file)
                signal = signal + np.array(bw.values(chr_, start_, stop_))*float(coeff_[i])
                bw.close()
        else:
            file = wd + "/data/" + samples_[i] + "_" + chr + "_" + strand_ + "_strand_raw.bw"
            bw = pyBigWig.open(file)
            signal = signal + np.array(bw.values(chr_, start_, stop_))*float(coeff_[i])
            bw.close()
    signal = signal/n_samples
    if scale_ == 'log':
        signal = np.log2(signal+1)
    if strand_ == 'R':
        signal = -signal
    signal = signal.tolist()
    return(signal)  

def get_color_scale(col_min = [1,1,0.667], col_max = [0,0.33,0.33]):
    N = 1024
    r = np.linspace(col_min[0], col_max[0], N+1)
    g = np.linspace(col_min[1], col_max[1], N+1)
    b = np.linspace(col_min[2], col_max[2], N+1)
    v = np.linspace(0,1, N+1)
    colorscale = ['']*(N+1)

    for i in range(0,N+1):
        colorscale[i] = [str(v[i]), 
           str('rgb(' + 
           str(int(round(r[i]*255))) + ',' + 
           str(int(round(g[i]*255))) + ',' + 
           str(int(round(b[i]*255))) + ')')]
    return(colorscale)

def readGff(f, info = ["ID","Name","Parent","gene","Alias","orf_classification","Ontology_term","Note","GO"]):
    tmp = np.genfromtxt(f, dtype = 'str', delimiter = "\t", comments='##')
    coord = tmp[:,0:8]
    notes = tmp[:, 8]


    notes_ = ['']*len(notes)
    annot = ['']*(len(notes)+1)
    annot[0] = ["Chr", "Source", "Type", "Start", "Stop", "Score", "Strand", "Frame"] + info

    for i_line in range(0,len(notes)):
        info_ = ['']*len(info)
        line_ = notes[i_line].split(";")
        for col in line_:
            split = col.split("=")
            info_name = split[0]
            info_val = split[1]        
            try:
                ind_info = info.index(info_name)
                info_[ind_info] = info_val      
            except:
                pass
        notes_[i_line] = info_
        annot[i_line+1] = coord[i_line].tolist() + notes_[i_line]     
    return(annot)
    
    
###################
#  get arguments  #
###################    

# working dir
wd = os.getcwd()

# chromosome
chr = sys.argv[1] 

# start
start = int(sys.argv[2])

# stop
stop = int(sys.argv[3])

# sample names
samples = sys.argv[4]
samples = samples.split(",") 

# visu type
visu = sys.argv[5]

# scale
scale = sys.argv[6]

# library type
libType = sys.argv[7]

# normalization
normalized = sys.argv[8]
if normalized == "True":
    normalized = True
else:
    normalized = False
    
# max signal (for heatmap color scale)    
maxSignal = int(sys.argv[9])
if scale == 'linear':
    n_digit = len(str(maxSignal))
    if n_digit > 2:
        n_digit = n_digit - 2
        to_div = pow(10, n_digit)
    else:
        to_div = 1
    zmax = round(maxSignal/to_div)*to_div
else:
    zmax = round(np.log2(maxSignal))

#wd = '/home/ugo/Documents/CURIE/python_javascript/'
#chr="chr15"
#start = 1000
#stop = 1100
#samples = ['WT_P_MYC_IP-1','WT_P_MYC_IP-2']
#visu = "heatmap"
#scale="log"
#libType="unstranded"
#normalized="True"
#maxSignal=65000

##########################
#  get description_data  #
##########################
# description : file names, sample name, group name, norm coeff, strand, color, line type
description_file = wd + "/data/description_data.tab"
tmp = np.genfromtxt(description_file,dtype = None, delimiter = "\t", comments='##')
description_data = tmp[1:len(tmp),]

# which samples
which_samples = ['']
group = ['']
for i in range(0,len(samples)):
    try:
        which_samples.append(description_data[:,1].tolist().index(samples[i]))
    except:
        for j in range(0,len(description_data)):
            if description_data[j,6] == samples[i]:
                group.append(j)
            if j == (len(description_data)-1):
                which_samples.append(group[1:len(group)])
                group = ['']

which_samples = which_samples[1:len(which_samples)]

####################
#  get annotation  #
####################
# gff file
annot_file = wd + "/data/annotation.gff"
tmp = readGff(annot_file)

##########################
#  get annotation style  #
##########################
style_file = wd + "/data/style.tab"
style = np.genfromtxt(style_file, dtype = None, delimiter = "\t", comments='##')

# select annotation features to plot
annot = []
parking = [np.array([0]*(stop-start))]
yPos = []
start_ = 0
stop_ = 0
id = []

for i in range(1,len(tmp)):
    if tmp[i][0] == chr:
        if tmp[i][4] > tmp[i][3]: 
            if int(tmp[i][3]) < stop and int(tmp[i][4]) > start:                    
                
                annot.append(tmp[i])
                    
                if int(tmp[i][3]) < start:
                    start_ = 0
                else:
                    start_= int(tmp[i][3]) - start

                if int(tmp[i][4]) > stop:
                    stop_ = stop - start -1
                else:
                    stop_ = int(tmp[i][4]) - start

                yPos_ = -1
                j = 0
                while yPos_ == -1:
                    if max(parking[j][start_:stop_]) == 0:
                        yPos_ = j
                        parking[j][(start_):(stop_)] = parking[j][(start_):(stop_)] + [1]*(stop_-start_)
                    else:
                        j = j+1
                        if j == (len(parking)):
                            yPos_ = j+1 
                            parking.append(np.array([0]*(stop-start)))
                            parking[j][(start_):(stop_)] = parking[j][(start_):(stop_)] + [1]*(stop_-start_)
                                       
                
                yPos.append(yPos_+1)                
                
                if tmp[i][9] == '':
                    i_id = 8
                else:
                    i_id = 9
                    
                id.append(tmp[i][i_id])
                    
                

# get data for annotation plot
if len(yPos) != 0:    
    xSpan = stop - start    
    types = style[:,0].tolist()
    xText = ['']*len(id)
    shapes_annot = ['']*len(id)

    if visu == "fill":    
        xaxis_ = 'x' + str(len(samples)+1)
        yaxis_ = 'y' + str(len(samples)+1)
    elif visu == "heatmap" : 
        xaxis_ = 'x3'
        yaxis_ = 'y3'
    else : 
        xaxis_ = 'x2'
        yaxis_ = 'y2'
        
    for i in range(0,len(annot)):
    
        start_annot = int(annot[i][3])
        stop_annot = int(annot[i][4])
        strand_annot = annot[i][6]    
 
        xText[i] = start_annot + (stop_annot-start_annot)/2
        if xText[i] < start:
            xText[i] = start + xSpan*0.01
        elif xText[i] > stop:
            xText[i] = stop - xSpan*0.01

        try:
            col_annot = style[types.index(annot[i][2])][1]
            shape_annot = style[types.index(annot[i][2])][2]
        except:
            col_annot = "LightGray"
            shape_annot = "box"
        y = yPos[i]
        if shape_annot == 'box':
            shapes_annot[i] = plotBox(start_annot, stop_annot, y, xSpan, strand_annot, col_annot, xaxis_, yaxis_)
        elif shape_annot == 'rectangle':
            shapes_annot[i] = plotRectangle(start_annot, stop_annot, y, col_annot, xaxis_, yaxis_)
        else:
            shapes_annot[i] = plotArrow(start_annot, stop_annot, y, xSpan, strand_annot, col_annot, xaxis_, yaxis_)
  
    textAnnot = {
        'x':xText,
        'y':(np.array(yPos)+0.30).tolist(),
        'xaxis': xaxis_,
        'yaxis': yaxis_,
        'text':id,
        'mode':'text',
        'textfont': {
            'size': 10
        },
        'showlegend': False
    }

##########################
#   line visualization   #
##########################                       
if visu == 'lines': 
# get signal
    data = ['']

    samples_labels = ['']*len(samples)
    
    for i in range(0,len(samples)):
        if scale == 'log':
            samples_labels[i] = 'log2 ' + samples[i]
        else:
            samples_labels[i] = samples[i]
    
    
    for i in range(0,len(samples)):
        i_files = description_data[which_samples[i],0]
        i_samples = description_data[which_samples[i],1]
        if np.shape(i_samples) == ():         
            i_samples = [i_samples]
            col = description_data[which_samples[i],4]
            lty = description_data[which_samples[i],5]
        else:
            col = description_data[which_samples[i][0],7]
            lty = description_data[which_samples[i][0],5] 
        if normalized == True:
            coeff = description_data[which_samples[i],2]
        else:
            coeff = ['1']*len(i_samples)
        if libType == 'unstranded':                
            signal = get_signal(chr, start, stop, i_files, i_samples, 'both', scale, coeff) 
            trace = {'x' : range(start,stop), 
                     'y' : signal,
                     'mode' : 'lines',
                     'name' : samples_labels[i],
                     'line' : {'color' : col,
                               'dash' : lty
                              }
                    }
            data.append(trace)
            
        else:
            for str_ in ['F', 'R']:
                if libType == 'inverse' and str == 'F':
                    str_ = 'R'
                if libType == 'inverse' and str == 'R':
                    str_ = 'F'
                signal = get_signal(chr, start, stop, i_files, i_samples, str_, scale, coeff)  
                if str_ == 'R':
                    show_legend = False
                else:
                    show_legend = 'true'
                if i == 0:
                    legendgroup='group'
                else:
                    legendgroup='group'+str(i)
                trace = {'x' : range(start, stop), 
                         'y' : signal,
                         'mode' : 'lines',
                         'legendgroup' : legendgroup,
                         'showlegend': show_legend,
                         'name' : samples_labels[i],
                         'line' : {'color' : col,
                                   'dash' : lty
                                  }
                        }
                data.append(trace)
    data = data[1:len(data)] 
    
#############################
#   heatmap visualization   #
#############################
if visu == 'heatmap':
# get signal
    cmap = get_color_scale()
    matPlus = ['']*len(samples)
    matMinus = ['']*len(samples)
    for i in range(0,len(samples)):
        i_files = description_data[which_samples[i],0]
        i_samples = description_data[which_samples[i],1]
        if np.shape(i_samples) == ():         
            i_samples = [i_samples]
        if normalized == True:
            coeff = description_data[which_samples[i],2]
        else:
            coeff = ['1']*len(i_samples)
        if libType == 'unstranded':
            matPlus[i] = get_signal(chr, start, stop, i_files, i_samples, 'both', scale, coeff)
            nb_row = 2
        else:
            if libType == 'inverse':
                matPlus[i] = (-np.array(get_signal(chr, start, stop, i_files, i_samples, 'R', scale, coeff))).tolist()
                matMinus[i] = get_signal(chr, start, stop, i_files, i_samples, 'F', scale, coeff)
            else:
                matPlus[i] =  get_signal(chr, start, stop, i_files, i_samples, 'F', scale, coeff)
                matMinus[i] = (-np.array(get_signal(chr, start, stop, i_files, i_samples, 'R', scale, coeff))).tolist() 
            nb_row = 3
    
    scale_title = 'tag/nt'
    if scale == 'log':
        scale_title = 'log2 ' + scale_title
       
    plus = {
        'z' : matPlus,
        'x' : range(start,stop),
        'y' : samples,
        'xaxis' : 'x2',
        'yaxis' : 'y2',
        'type' : 'heatmap',
        'zmin' : 0,
        'zmax' : zmax,
        'colorscale' : cmap,
        'colorbar': {
            'title' : {
                'text' : scale_title
            }
        },
        'showscale' : False
    }
    
    if libType != 'unstranded':
        if yPos[0] == '':
            xaxis_ = 'x3'
            yaxis_ = 'y3'
        else:
            xaxis_ = 'x4'
            yaxis_ = 'y4'
            
        minus = {
            'z' : matMinus,
            'x' : range(start,stop),
            'y' : samples,
            'xaxis' : xaxis_,
            'yaxis' : yaxis_,
            'type' : 'heatmap',
            'zmin' : 0,
            'zmax' : zmax,
            'colorscale' : cmap,
            'showscale' : False
        }  
                 
    # legend colorscale             
    legend = {
        'z' : [range(0, int(zmax)+1)],
        'type' : 'heatmap',
        'zmin' : 0,
        'zmax' : zmax,
        'colorscale' : cmap,
        'showscale' : False
    }

##########################
#   fill visualization   #
##########################        
if visu == 'fill':    
    data = ['']
    for i in range(0,len(samples)):
        i_files = description_data[which_samples[i],0]
        i_samples = description_data[which_samples[i],1]
        if np.shape(i_samples) == ():         
            i_samples = [i_samples]
        if normalized == True:
            coeff = description_data[which_samples[i],2]
        else:
            coeff = ['1']*len(i_samples)
        if libType == 'unstranded':                
            signal = get_signal(chr, start, stop, i_files, i_samples, 'both', scale, coeff)    
            col = description_data[which_samples[i],4]
            lty = description_data[which_samples[i],5]
            if i==0:
                trace = {'x' : range(start,stop), 
                         'y' : signal,
                         'fillcolor': 'FireBrick',
                         'fill': 'tozeroy',
                         'line':{'color':'FireBrick'}
                        }
            else:
                trace = {'x' : range(start,stop), 
                         'y' : signal,
                         'fillcolor': 'FireBrick',
                         'fill': 'tozeroy',
                         'line':{'color':'FireBrick'},
                         'xaxis': 'x' + str(i+1),
                         'yaxis': 'y' + str(i+1) 
                        }                    
            data.append(trace)
        else:
            for str_ in ['F', 'R']:
                if libType == 'inverse' and str == 'F':
                    str_ = 'R'
                if libType == 'inverse' and str == 'R':
                    str_ = 'F'
                signal = get_signal(chr, start, stop, i_files, i_samples, str_, scale, coeff)
                lty = description_data[which_samples[i],5]   
                if str_ == 'R':
                    col = 'CornflowerBlue'
                else:
                    col = 'FireBrick'
                if i == 0:
                    trace = {'x' : range(start, stop), 
                             'y' : signal,
                             'fillcolor':col,
                             'line':{'color':col},
                             'fill': 'tozeroy'
                            }
                else:
                    trace = {'x' : range(start, stop), 
                             'y' : signal,
                             'fillcolor':col,
                             'line':{'color':col},
                             'fill': 'tozeroy',
                             'xaxis': 'x' + str(i+1),
                             'yaxis': 'y' + str(i+1) 
                            }
                data.append(trace)
    data = data[1:len(data)]  
    
################
#  get layout  #    
################

# plot margin
margins_out = { 'l': 100,'r': 100,'b': 100,'t': 100 }
    
    
if visu == 'lines':
    
    margin_out = 0
    margin_in = 50
    plot_height = 600

    if yPos[0] != '':
        
        annot_height = max(yPos)*75
        window_height = margin_out*2 + plot_height + margin_in + annot_height
 
        margin_out_frac = float(margin_out)/window_height
        margin_in_frac = float(margin_in)/window_height
        annot_height_frac = float(annot_height)/window_height
        plot_height_frac = float(plot_height)/window_height
          
        stop_1 = 1-margin_out_frac
        start_1 = stop_1-plot_height_frac
            
        stop_2 = start_1 - margin_in_frac
        start_2 = stop_2 - annot_height_frac         

        layout = {
            'xaxis' : {
               'domain' : [0.1,1],
               'anchor' : 'y',
               'range' : [start,stop]
            },
            'yaxis' : {
                'domain' : [start_1, stop_1],
                'anchor' : 'x'
            },
            'xaxis2': {
                'range': [start, stop],
                'zeroline': False,
                'showgrid': False,
                'domain' : [0.1,1],
                'anchor' : 'y2',
                'showticklabels': False
            },
            'yaxis2': {
                'range': [-0.25, max(yPos)+1],
                'showgrid': False,
                'zeroline': False,
                'ticks':'',
                'showticklabels': False,
                'domain' : [start_2, stop_2],
                'anchor' : 'x2'
            },
            'grid': {'rows': 2, 'columns': 1, 'pattern': 'independent'},
            'shapes':shapes_annot,
            'margin': margins_out
        }
  
        data.append(textAnnot)    
        
    else :
        
        window_height = margin_out*2 + plot_height
 
        margin_out_frac = float(margin_out)/window_height
        plot_height_frac = float(plot_height)/window_height
          
        stop_1 = 1-margin_out_frac
        start_1 = stop_1-plot_height_frac        

        layout = {            
            'xaxis' : {
               'domain' : [0.1,1],
               'anchor' : 'y',
               'range' : [start,stop]
            },
            'yaxis' : {
                'domain' : [start_1, stop_1],
                'anchor' : 'x'
            },
            'margin': margins_out
        }
    
    res = [data, layout, window_height]
    print(json.dumps(res, separators=(',',':')))

if visu == "heatmap":

    margin_out = 50
    plot_height = 50 * len(samples)    
    
    legend_height = 50        
    if scale == 'linear':
        legend_title = 'tag/nt' 
    else : 
        legend_title = 'log2 tag/nt'
   
    if yPos[0] != '':
           
        margin_in = 50
        annot_height = max(yPos)*75                      
   
        if libType != 'unstranded': 
            
            window_height = legend_height + margin_out*2 + plot_height*2 + margin_in*3 + annot_height
 
            legend_height_frac = float(legend_height)/window_height
            margin_out_frac = float(margin_out)/window_height
            margin_in_frac = float(margin_in)/window_height
            annot_height_frac = float(annot_height)/window_height
            plot_height_frac = float(plot_height)/window_height
            
            stop_1 = 1 - margin_out_frac              
            start_1 = stop_1 - legend_height_frac            
            
            stop_2 = start_1 - margin_in_frac
            start_2 = stop_2 - plot_height_frac
            
            stop_3 = start_2 - margin_in_frac
            start_3 = stop_3 - annot_height_frac
 
            stop_4 = start_3 - margin_in_frac
            start_4 = stop_4 - plot_height_frac 
            
            data = [legend, plus, textAnnot, minus]            
            
            layout = {
                'xaxis' : {
                    'domain' : [0.3,0.8],
                    'anchor' : 'y', 
                    'ticks' : "",
                    'title' : legend_title,
                    'side' : 'top'},
                'yaxis' : {                    
                    'domain' : [start_1, stop_1],
                    'anchor' : 'x',
                    'showticklabels': False,
                    'ticks' : ""},
                'xaxis2' : {
                    'range': [start, stop],
                    'domain' : [0.1,1],
                    'anchor' : 'y2'
                },
                'yaxis2' : {
                    'domain' : [start_2, stop_2],
                    'anchor' : 'x2',
                    'title' : '+ strand'
                },
                'xaxis3': {
                    'range': [start, stop],
                    'zeroline': False,
                    'showgrid': False,
                    'domain' : [0.1,1],
                    'anchor' : 'y3',
                    'showticklabels': False
                },
                'yaxis3': {
                    'range': [-0.25, max(yPos)+1],
                    'showgrid': False,
                    'zeroline': False,
                    'ticks':'',
                    'showticklabels': False,
                    'domain' : [start_3, stop_3],
                    'anchor' : 'x3',
                },
                'xaxis4' : {
                    'range': [start, stop],
                    'domain' : [0.1,1],
                    'anchor' : 'y4'
                },
                'yaxis4' : {
                   'domain' : [start_4, stop_4],
                   'anchor' : 'x4',
                   'title' : '- strand'
               },
                'grid': {'rows': 3, 'columns': 1, 'pattern': 'independent'},
                'shapes':shapes_annot,
                'margin': margins_out
            }
        else:

            window_height = legend_height + margin_out*2 + plot_height + margin_in*2 + annot_height
 
            legend_height_frac = float(legend_height)/window_height
            margin_out_frac = float(margin_out)/window_height
            margin_in_frac = float(margin_in)/window_height
            annot_height_frac = float(annot_height)/window_height
            plot_height_frac = float(plot_height)/window_height
            
                        
            stop_1 = 1 - margin_out_frac           
            start_1 =  stop_1 - legend_height_frac           
            
            stop_2 = start_1 - margin_in_frac 
            start_2 = stop_2 - plot_height_frac
            
            stop_3 = start_2 - margin_in_frac
            start_3 = stop_3 - annot_height_frac           
            
            data = [legend, plus, textAnnot]             
 
            layout = {
                'xaxis' : {
                    'domain' : [0.3,0.8],
                    'anchor' : 'y', 
                    'ticks' : "",
                    'title' : legend_title,
                    'side' : 'top'},
                'yaxis' : {
                    'domain' : [start_1, stop_1],
                    'anchor' : 'x',
                    'showticklabels': False,
                    'ticks' : ""},
                'xaxis2' : {
                    'range': [start, stop],
                    'domain' : [0.1,1],
                    'anchor' : 'y2'
                },
                'yaxis2' : {
                    'domain' : [start_2, stop_2],
                    'anchor' : 'x2'
                },
                'xaxis3': {
                    'range': [start, stop],
                    'zeroline': False,
                    'showgrid': False,
                    'domain' : [0.1,1],
                    'anchor' : 'y3',
                    'showticklabels': False
                },
                'yaxis3': {
                    'range': [-0.25, max(yPos)+1],
                    'showgrid': False,
                    'zeroline': False,
                    'ticks':'',
                    'showticklabels': False,
                    'domain' : [start_3, stop_3],
                    'anchor' : 'x3',
                },
                'grid': {'rows': 2, 'columns': 1, 'pattern': 'independent'},
                'shapes':shapes_annot,
                'margin': margins_out
            }
    else : 
        
        if libType != 'unstranded':

            margin_in = 100
            window_height = legend_height + margin_out*3 + plot_height*2 + margin_in
 
            legend_height_frac = float(legend_height)/window_height
            margin_out_frac = float(margin_out)/window_height
            margin_in_frac = float(margin_in)/window_height
            plot_height_frac = float(plot_height)/window_height
            
            stop_1 = 1 - margin_out_frac
            start_1 = stop_1 - legend_height_frac            
            
            stop_2 = start_1 - margin_out_frac
            start_2 = stop_2 - plot_height_frac
            
            stop_3 = start_2 - margin_in_frac
            start_3 = stop_3 - plot_height_frac             
            
            data = [legend, plus, minus]

            layout = {
                'xaxis' : {
                    'domain' : [0.3,0.8],
                    'anchor' : 'y', 
                    'ticks' : "",
                    'title' : legend_title,
                    'side' : 'top'},
                'yaxis' : {
                    'domain' : [start_1, stop_1],
                    'anchor' : 'x',
                    'showticklabels': False,
                    'ticks' : ""},
                'xaxis2' : {
                    'range': [start, stop],
                    'domain' : [0.1,1],
                    'anchor' : 'y2'
                },
                'yaxis2' : {
                    'domain' : [start_2, stop_2],
                    'anchor' : 'x2',
                    'title' : '+ strand'
                },
                'xaxis3' : {
                    'range': [start, stop],
                    'domain' : [0.1,1],
                    'anchor' : 'y3'
                },
                'yaxis3' : {
                    'domain' : [start_3, stop_3],
                    'anchor' : 'x3',
                    'title' : '- strand'
                },
                'grid': {'rows': 2, 'columns': 1, 'pattern': 'independent'},
                'margin': margins_out
            }
        else : 
            
            window_height = legend_height + margin_out*3 + plot_height
 
            legend_height_frac = float(legend_height)/window_height
            margin_out_frac = float(margin_out)/window_height
            plot_height_frac = float(plot_height)/window_height
            
            stop_1 = 1- margin_out_frac
            start_1 = stop_1 - legend_height_frac            
            
            stop_2 = start_1 - margin_out_frac
            start_2 = stop_2 - plot_height_frac            
            
            data = [legend, plus]

            layout = {
                'xaxis' : {
                    'domain' : [0.3,0.8],
                    'anchor' : 'y', 
                    'ticks' : "",
                    'title' : legend_title,
                    'side' : 'top'},
                'yaxis' : {
                    'domain' : [start_1, stop_1],
                    'anchor' : 'x',
                    'showticklabels': False,
                    'ticks' : ""},
                'xaxis2' : {
                    'range': [start, stop],
                    'domain' : [0.1,1],
                    'anchor' : 'y2'
                },
                'yaxis2' : {
                    'domain' : [start_2, stop_2],
                    'anchor' : 'x2'
                },
                'margin': margins_out
            }
                
    
    res = [data, layout, window_height]
    print(json.dumps(res, separators=(',',':')))
    
if visu == "fill":
    
    margin_in = 50
    plot_height = 200     
        
    samples_labels = ['']*len(samples)
    
    if scale == 'log':
        for i in range(0, len(samples)):
            samples_labels[i] = 'log2 ' + samples[i]
    
    if yPos[0] != '':
        
        annot_height = max(yPos)*75
        window_height = (len(samples) + 1)*margin_in + len(samples)*plot_height + margin_in + annot_height
        
        margin_in_frac = float(margin_in)/window_height
        plot_height_frac = float(plot_height)/window_height
        annot_height_frac = float(annot_height)/window_height        
        
        data.append(textAnnot)    
        
    else:
        
        window_height = (len(samples) + 1)*margin_in + len(samples)*plot_height
        
        plot_height_frac = float(plot_height)/window_height   
    
    layout = {}
        
    for i in range(0, len(samples)):

        xaxis_ = 'xaxis'+str(i+1)
        yaxis_ = 'yaxis'+str(i+1)
            
        layout[xaxis_] = {
            'range' : [start, stop],
            'domain' : [0.1,1], 
            'anchor' : 'y'+str(i+1)
        }

        domain_start = 1-(margin_in_frac + plot_height_frac)*(i+1)
        domain_stop = domain_start + plot_height_frac

        layout[yaxis_] = {
            'domain' : [domain_start,domain_stop], 
            'anchor' : 'x'+str(i+1),
            'title' : {'text' : samples_labels[i]}
        }
        
    if yPos[0] != '':
        
        xaxis_ = 'xaxis'+str(len(samples)+1)    
        yaxis_ = 'yaxis'+str(len(samples)+1)
        
        domain_start = 1-(plot_height_frac*len(samples) + annot_height_frac + margin_in_frac*len(samples)+ margin_in_frac)  
        domain_stop = domain_start + annot_height_frac        
        
        layout[xaxis_] = {
            'range': [start, stop],
            'zeroline': False,
            'showgrid': False,
            'domain' : [0.1,1],
            'anchor' : 'y'+str(len(samples)+1), 
            'showticklabels': False
        }
        layout[yaxis_] = {
            'range': [-0.25, max(yPos)+1],
            'showgrid': False,
            'zeroline': False,
            'ticks':'',
            'showticklabels': False,
            'domain' : [domain_start, domain_stop],
            'anchor' : 'x'+str(len(samples)+1) 
        }
        layout['grid'] = {
            'rows': len(samples)+1, 
            'columns': 1, 
            'pattern': 'independent'
        }
        layout['shapes'] = shapes_annot
    else : 
        layout['grid'] = {
            'rows': len(samples), 
            'columns': 1, 
            'pattern': 'independent'
        }
    
    
    layout['showlegend'] = False    
    layout['margin'] = margins_out
    
    res = [data, layout, window_height]
    print(json.dumps(res, separators=(',',':')))
        
