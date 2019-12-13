# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:08:22 2019

@author: ugo
"""

##########
#  libs  #
##########

import numpy as np
import os
import pyBigWig

###############
#  functions  #   
############### 

def plotRectangle(start, stop, yPos, color):
    res = {
      'xref' : 'x' + str(i_xaxs_ref),
      'yref' : 'y' + str(i_xaxs_ref),
      'type': 'rect',
      'x0': start,
      'y0': yPos-0.1,
      'x1': stop,
      'y1': yPos + 1,
      'line': {
        'color': color
      },
      'fillcolor': color
    }
    return(res)

def plotArrow(start, stop, yPos, xSpan, strand, color):
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
      }
    }
    return(res)
     
def plotBox(start, stop, yPos, xSpan, strand, color):
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
      }
    }
    return(res)  

def setShapeRefAxis(shape, i_ref_axis):
	
	for i in range(0,len(shape)):
		
		shape[i]['xref'] = 'x' + str(i_ref_axis)
		shape[i]['yref'] = 'y' + str(i_ref_axis)
		
	return(shape)

def readGff(f, info = ["ID","Name","Parent","gene","Alias","orf_classification","Ontology_term","Note","GO"]):
    tmp = np.genfromtxt(f, dtype = 'str', delimiter = "\t", comments='#')
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


def getAnnotData(annot_file, style_file, chr, start, stop):

    # style
    style = np.genfromtxt(style_file, dtype = None, delimiter = "\t", comments='##')

    # all annot file
    tmp = readGff(annot_file)

    parking = [np.array([0]*(stop-start))]
    
    textAnnot = {
        'x':[],
        'y':[],
        'text':[],
        'mode':'text',
        'textfont': {
            'size': 10
        },
        'showlegend': False
    }    
    
    shapesAnnot = []    
    
    xSpan = stop - start    
    
    types = style[:,0].tolist()
    
    for i in range(1,len(tmp)):
        
        if tmp[i][0] == chr:
            
            if tmp[i][4] > tmp[i][3]: 
                
                if int(tmp[i][3]) < stop and int(tmp[i][4]) > start:                                      
                    
                    # if start annot < start window 
                    if int(tmp[i][3]) < start:
                        start_ = 0
                    else:
                        start_= int(tmp[i][3]) - start

                    # if stop annot > stop window
                    if int(tmp[i][4]) > stop:
                        stop_ = xSpan -1
                    else:
                        stop_ = int(tmp[i][4]) - start

                    # get y position
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
                
                    textAnnot['y'].append(yPos_+1.3)                
                
                    # get transcript ID
                    if tmp[i][9] == '':
                        i_id = 8
                    else:
                        i_id = 9
                    
                    textAnnot['text'].append(tmp[i][i_id])
                    
                    # get x position
                    textAnnot['x'].append(start + (start_ + (stop_ - start_)/2))
                    
                    # get color and shape
                    try:
                        col_annot = style[types.index(tmp[i][2])][1]
                        shape_annot = style[types.index(tmp[i][2])][2]
                    except:
                        col_annot = "LightGray"
                        shape_annot = "box"
                    
                    if shape_annot == 'box':
                        shapesAnnot.append(plotBox(int(tmp[i][3]), int(tmp[i][4]), (yPos_+1), xSpan, tmp[i][6], col_annot))
                    elif shape_annot == 'rectangle':
                        shapesAnnot.append(plotRectangle(int(tmp[i][3]), int(tmp[i][4]), (yPos_+1), col_annot))
                    else:
                        shapesAnnot.append(plotArrow(int(tmp[i][3]), int(tmp[i][4]), (yPos_+1), xSpan, tmp[i][6], col_annot))
    
    res = {
        'textAnnot' : textAnnot,
        'shapesAnnot' : shapesAnnot
    }
    
    return(res)

def setTopYDomain(top_y_domain, height):

    res = top_y_domain - height
    
    if res < 0:
		
        res = 0
		
    return(res)

def calculateWindowHeight(param_visu, samples_visu, is_heatmap_stranded, is_annot_to_plot):
    
    n_bloc_layout = 0
    
    window_height = 0
    
    for visu in samples_visu.keys():

        if n_bloc_layout > 0:

            window_height = window_height + param_visu['margin']

        if len(samples_visu[visu]) > 0:

            n_bloc_layout = n_bloc_layout + 1

            if visu == 'line':

                window_height = window_height + param_visu['line']

            if visu == 'fill':

                window_height = window_height + len(samples_visu['fill']) * param_visu['fill'] + (len(samples_visu['fill']) - 1) * param_visu['margin']

            if visu == 'heatmap':

                window_height = window_height + len(samples_visu['heatmap']) * param_visu['heatmap'] + param_visu['annot']

                if is_heatmap_stranded:

                    window_height = window_height + len(samples_visu['heatmap']) * param_visu['heatmap'] + param_visu['margin'] * is_annot_to_plot
    
                window_height = window_height + param_visu['margin'] * 2 # for heatmap scale
    
    window_height = window_height + param_visu['annot']   

    return(window_height)

def get_color_scale(col_min = [1,1,0.667], col_max = [0,0.33,0.33]):
    N = 16
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

def get_signal(chr_, start_, stop_, sample_name_, strand_, scale_, description_data_, wd_, reverseNegative = True):

    sample_index = np.where(description_data_["replicate_name"] == sample_name_)[0]

    if(len(sample_index) == 0):
            
        sample_index = np.where(description_data_["cond_name"] == sample_name_)[0]

    n_samples = len(sample_index)

    signal = np.array([0]*(stop_-start_))    
    
    for i in range(0,n_samples):
        
        coeff = float(description_data_["norm_coeff"][sample_index][i])    
        
        if strand_ == 'both':

            for file_str in ['file_F', 'file_R']:
                
                file = wd_ +  "/data/" + description_data_[file_str][sample_index][i]

                if os.path.exists(file) == False:
                    
                    print("file " + file + " was not found")
                    
                    signal = np.array([0]*(stop_-start_)) 

                else:

                    bw = pyBigWig.open(file)

                    signal = signal + np.array(bw.values(chr_, start_, stop_))*coeff

                    bw.close()
                
        else:
            
            if strand_ == 'F':            
            
                file = wd_ + "/data/" + description_data_['file_F'][sample_index][i]
            
            else:
                
                file = wd_ + "/data/" + description_data_['file_R'][sample_index][i]
            
            if os.path.exists(file) == False:
                    
                    print("file " + file + " was not found")
                    
                    signal = np.array([0]*(stop_-start_)) 

            else:            
            
                bw = pyBigWig.open(file)
            
                signal = signal + np.array(bw.values(chr_, start_, stop_))*coeff
            
                bw.close()
            
    signal = signal/n_samples
    
    if scale_ == 'log':
        
        signal = np.log2(signal+1)
    
    if reverseNegative:    
    
        if strand_ == 'R':
        
            signal = -signal
        
    signal = signal.tolist()
    
    return(signal)    
 
def readDescriptionData(description_file):

    # description data all samples
    tmp = np.genfromtxt(description_file, dtype = None, delimiter = "\t", comments='##')
    
    description_data = {}
    
    for i_field in range(0,len(tmp[0])):
        
        description_data[tmp[0,i_field].decode('utf8')] = np.array([tmp[i, i_field].decode('utf8') for i in range(1, (np.shape(tmp)[0])-1)])

    return(description_data) 

def getSampleCol(description_data, sample_name):

    sample_index = np.where(description_data['replicate_name'] == sample_name)[0]
	
    if len(sample_index) == 1:

        col = description_data['replicate_col'][sample_index][0]            
                        
    else:
            
        sample_index = np.where(description_data['cond_name'] == sample_name)[0]
            
        col = description_data['cond_col'][sample_index][0]   
    
    return(col)

def getSampleLty(description_data, sample_name):

    sample_index = np.where(description_data['replicate_name'] == sample_name)[0]

    if len(sample_index) == 1:

        lty = description_data['replicate_line'][sample_index][0]            
                        
    else:
            
        sample_index = np.where(description_data['cond_name'] == sample_name)[0]
            
        lty = description_data['cond_col'][sample_index][0]          

    return(lty)

def getSampleMax(description_data, sample_name):

    sample_index = np.where(description_data["replicate_name"] == sample_name)[0]

    if(len(sample_index) == 1):

        max_ = np.max(float(description_data['max_val'][sample_index][0]) * float(description_data['norm_coeff'][sample_index][0]))            
                        
    else:
            
        sample_index = np.where(description_data["cond_name"] == sample_name)[0]
        
        max_ = np.max([float(description_data['max_val'][i]) * float(description_data['norm_coeff'][i]) for i in sample_index])

    return(max_)

def getLineTrace(chr, start, stop, sample_name, scale, strand, description_data, wd, xaxis, yaxis, col = None, lty = None, legendGroup = None):

    signal = get_signal(chr_ = chr, start_ = start, stop_ = stop, sample_name_ = sample_name, strand_ = strand, scale_ = scale, 
                        description_data_ = description_data, wd_ = wd)
        
    trace = {
        'x' : list(range(start,stop)), 
        'y' : signal,
        'mode' : 'lines',
        'name' : sample_name,
        'line' : {
            'color' : col,
            'dash' : lty
        },
        'xaxis' : xaxis,
        'yaxis' : yaxis
    }
    
    if strand == 'R':
        
        trace['showlegend'] = False
    
    if legendGroup is not None:
        
        trace['legendgroup'] = legendGroup
        
    return(trace)

def getFillTrace(chr, start, stop, sample_name, scale, strand, description_data, wd, xaxis, yaxis):

    signal = get_signal(chr_ = chr, start_ = start, stop_ = stop, sample_name_ = sample_name, strand_ = strand, scale_ = scale, 
                        description_data_ = description_data, wd_ = wd)

    if strand == 'both' or strand == 'F':
        
        fillcolor = 'FireBrick'
        
    else:
        
        fillcolor = 'CornflowerBlue'

    trace = {
        'x' : list(range(start,stop)), 
        'y' : signal,
        'fillcolor': fillcolor,
        'fill': 'tozeroy',
        'line': {
            'color':fillcolor
        },
        'xaxis' : xaxis,
        'yaxis' : yaxis,
        'showlegend' : False
    }    
    
    return(trace)

def getHeatmapTrace(chr, start, stop, sample_names, scale, strand, description_data, wd, i_axis, cmap, zmax):

    mat = ['']*len(sample_names)

    for i in range(0,len(sample_names)):

        mat[i] = get_signal(chr_ = chr, start_ = start, stop_ = stop, sample_name_ = sample_names[i], strand_ = strand, scale_ = scale, 
                            description_data_ = description_data, wd_ = wd, reverseNegative = False)
        
    scale_title = 'tag/nt'
    if scale == 'log':
        scale_title = 'log2 ' + scale_title
       
    trace = {
        'z' : mat,
        'x' : list(range(start,stop)),
        'y' : sample_names.tolist(),
        'xaxis' : 'x' + str(i_axis),
        'yaxis' : 'y' + str(i_axis),
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
    
    return(trace)

def getHeatmapLegend(zmax, cmap, i_axis):
    
    legend = {
        'z' : [list(range(0, zmax))],
        'type' : 'heatmap',
        'zmin' : 0,
        'zmax' : zmax,
        'colorscale' : cmap,
        'showscale' : False,
        'xaxis' : 'x' + str(i_axis),
        'yaxis' : 'y' + str(i_axis)
    }
    
    return(legend)
