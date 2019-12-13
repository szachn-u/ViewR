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

import functions as func
      
###################
#  get arguments  #
###################    

args = {}

# working dir
args['wd'] = os.getcwd()
#args['wd'] = "/home/ugo/python_browser/work_in_progress"

# chromosome
args['chr'] = sys.argv[1] 

#args['chr'] = "chr01"

# start
args['start'] = int(sys.argv[2])

#args['start'] = 30000

# stop
args['stop'] = int(sys.argv[3])

#args['stop'] = 30010

# sample names
args['samples'] = sys.argv[4]
args['samples'] = np.array(args['samples'].split(",")) 

#args['samples'] = np.array(['WT.G1.A238', 'xrn1.G1.4', 'WT.G1.1', 'rad50set1.G1.A237', 'xrn1.G1.3', 'xrn1.G1.1', 'rad50.G1.A237'])

# visu type
args['visu'] = sys.argv[5]
args['visu'] = args['visu'].split(",")

#args['visu'] = ['heatmap', 'fill', 'fill', 'fill', 'line', 'line', 'line']

if len(args['visu']) == 1:
    
    args['visu'] = args['visu']*len(args['samples'])

args['visu'] = np.array(args['visu'])

# scale
args['scale'] = sys.argv[6]
args['scale'] = args['scale'].split(",")

#args['scale'] = ['log', 'log', 'linear', 'linear', 'log', 'log', 'log']

if len(args['scale']) == 1:
    
    args['scale'] = args['scale']*len(args['samples'])

args['scale'] = np.array(args['scale'])

# library type
args['libType'] = sys.argv[7]
args['libType'] = args['libType'].split(",")

#args['libType'] = ['stranded', 'unstranded', 'stranded', 'unstranded', 'stranded', 'stranded', 'stranded']

if len(args['libType']) == 1:
    
    args['libType'] = args['libType']*len(args['samples'])
    
args['libType'] = np.array(args['libType'])

# normalization
args['normalized'] = sys.argv[8]
args['normalized'] = args['normalized'].split(",")

#args['normalized'] = ["True", "True", "False", "False", "True", "True", "True"]

if len(args['normalized']) == 1:
    
    args['normalized'] = args['normalized']*len(args['samples'])

args['normalized'] = np.array(args['normalized'])

args['normalized'] = ['normalized'] == "True"

##########################
#  get description_data  #
##########################
# description : file names, sample name, group name, norm coeff, strand, color, line type

description_file = args['wd'] + '/data/description_data.tab'

description_data = func.readDescriptionData(description_file = description_file)

##############################
#  get annotation and style  #
##############################
# gff file
annot_file = args['wd'] + "/data/annotation.gff"

style_file = args['wd'] + "/data/style.tab"

data_annot = func.getAnnotData(annot_file = annot_file, style_file = style_file, chr = args['chr'], start = args['start'], stop = args['stop'])

is_annot_to_plot = len(data_annot['textAnnot']['text']) > 0

##############################
#   Visualisation parameters #
##############################

i_axis = 1

top_y_domain = 1

samples_left = args['samples']

visus = ['fill','line','heatmap']

samples_visu = {}

for visu in visus:

    samples_visu[visu] = np.where(args['visu'] == visu)[0]
    
is_heatmap_stranded = len(np.where((args['visu'] == 'heatmap') & (args['libType'] == 'stranded') == True)[0]) > 0  

param_visu = {
    'line' : 500,
    'fill' : 200,
    'heatmap' : 50,
    'margin' : 50,
    'annot' : max(data_annot['textAnnot']['y'])*50
    }

window_height = func.calculateWindowHeight(param_visu = param_visu, samples_visu = samples_visu, is_heatmap_stranded = is_heatmap_stranded, is_annot_to_plot = is_annot_to_plot)

for p in param_visu.keys():
        
    param_visu[p] = param_visu[p]/window_height

param_visu['margins_out'] = { 'l': 100,'r': 100,'b': 100,'t': 100 }

##########################
#  get data for plotly   #
##########################

data = []

layout = {}

shapes = []

print(shapes)
print("")
n_bloc_layout = 0

for visu in visus:

    which_samples = samples_visu[visu]
    
    if len(samples_visu[visu]) > 0:

        sample_visu = args['samples'][which_samples]        
            
        lib_type_visu = args['libType'][which_samples]
    
        scale_visu = args['scale'][which_samples]    
    
        if n_bloc_layout > 0:
            
                top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['margin'])

        n_bloc_layout = n_bloc_layout + 1

        if visu == 'line':

            scale_visu_ = scale_visu[0]

            # get data                       
            for i_sample in range(0, len(sample_visu)):
                
                col = func.getSampleCol(description_data = description_data, sample_name = sample_visu[i_sample])
                
                lty = func.getSampleLty(description_data = description_data, sample_name = sample_visu[i_sample])
        
                if lib_type_visu[i_sample] == 'unstranded':        
        
                    d = func.getLineTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_name = sample_visu[i_sample], 
                    scale = scale_visu[i_sample], strand = 'both', description_data = description_data, wd = args['wd'], 
                    xaxis = 'x' + str(i_axis), yaxis = 'y' + str(i_axis), legendGroup = 'group' + str(i_sample + 1), col = col, lty = lty)
        
                    data.append(d)        
        
                else:
            
                    d = func.getLineTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_name = sample_visu[i_sample], scale = scale_visu_, 
                    strand = 'F', description_data = description_data, wd = args['wd'], xaxis = 'x' + str(i_axis), yaxis = 'y' + str(i_axis), 
                    legendGroup = 'group' + str(i_sample + 1), col = col, lty = lty)
                    
                    data.append(d)                    
                    
                    d = func.getLineTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_name = sample_visu[i_sample], scale = scale_visu_, 
                    strand = 'R', description_data = description_data, wd = args['wd'], xaxis = 'x' + str(i_axis), yaxis = 'y' + str(i_axis), 
                    legendGroup = 'group' + str(i_sample + 1), col = col, lty = lty)
     
                    data.append(d)
            
            # get layout                     
            
            layout['xaxis' + str(i_axis)] = {
                'domain' : [0.1,1],
                'anchor' : 'y' + str(i_axis),
                'range' : [args['start'],args['stop']]
                }
        
            layout['yaxis' + str(i_axis)] = {
                'domain' : [func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['line']), top_y_domain],
                'anchor' : 'x' + str(i_axis),
                'title' : 'log2 ' * (scale_visu_ == 'log') + 'tag/nt',
                }
    
            top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['line'])            

            i_axis = i_axis + 1
            
            # add annotation if no visu after
            samples_left[which_samples] = ''

            if len(np.where(samples_left != '')[0]) == 0:
            
                if is_annot_to_plot: 
                 
                    n_bloc_layout = n_bloc_layout + 1

                    # data
                    textAnnot = data_annot['textAnnot'].copy()   
                        
                    textAnnot['xaxis'] = 'x' + str(i_axis)
                    textAnnot['yaxis'] = 'y' + str(i_axis)
                        
                    data.append(textAnnot)
                    
                    # layout
                    layout['xaxis' + str(i_axis)] = {
                        'range': [args['start'], args['stop']],
                        'zeroline': False,
                        'showgrid': False,
                        'domain' : [0.1,1],
                        'anchor' : 'y' + str(i_axis),
                        'showticklabels': False
                        }
                    
                    layout['yaxis' + str(i_axis)] = {
                        'range': [-0.25, max(data_annot['textAnnot']['y'])+1],
                        'showgrid': False,
                        'zeroline': False,
                        'ticks':'',
                        'showticklabels': False,
                        'domain' : [func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['annot']), top_y_domain],
                        'anchor' : 'x' + str(i_axis)
                        }
                    
                    # shapes
                    for i_shape in range(0, len(data_annot['shapesAnnot'])):

                        s = data_annot['shapesAnnot'][i_shape].copy()

                        s['xref'] = 'x' + str(i_axis)
                        s['yref'] = 'y' + str(i_axis)
	
                        shapes.append(s)

                    i_axis = i_axis + 1
					
                    top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['annot'])	
          
        if visu == 'fill':
    
            for i_sample in range(0, len(sample_visu)):
 
                if i_sample > 0: 
                
                    top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['margin'])

                if lib_type_visu[i_sample] == 'unstranded':        
        
                    d = func.getFillTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_name = sample_visu[i_sample], 
                    scale = scale_visu[i_sample], strand = 'both', description_data = description_data, wd = args['wd'], 
                    xaxis = 'x' + str(i_axis), yaxis = 'y' + str(i_axis))
        
                    data.append(d)
                    
                else:
            
                    d = func.getFillTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_name = sample_visu[i_sample], 
                    scale = scale_visu[i_sample], strand = 'F', description_data = description_data, wd = args['wd'], 
                    xaxis = 'x' + str(i_axis), yaxis = 'y' + str(i_axis))
        
                    data.append(d)
                    
                    d = func.getFillTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_name = sample_visu[i_sample], 
                    scale = scale_visu[i_sample], strand = 'R', description_data = description_data, wd = args['wd'], 
                    xaxis = 'x' + str(i_axis), yaxis = 'y' + str(i_axis))
        
                    data.append(d)
        
                layout['xaxis' + str(i_axis)] = {
                    'domain' : [0.1,1],
                    'anchor' : 'y' + str(i_axis),
                    'range' : [args['start'],args['stop']]
                    }

                layout['yaxis' + str(i_axis)] = {
                    'domain' : [func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['fill']), top_y_domain],
                    'anchor' : 'x' + str(i_axis),
                    'title' : {'text' : 'log2 ' * (scale_visu[i_sample] == 'log') + 'tag/nt \n' + str(sample_visu[i_sample])}
                    }
                
                i_axis = i_axis + 1
                
                top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['fill'])
             
            samples_left[which_samples] = ''

            if len(np.where(samples_left != '')[0]) == 0:                      
                    
                if is_annot_to_plot:                   

                    n_bloc_layout = n_bloc_layout + 1

                    textAnnot = data_annot['textAnnot'].copy()    
                        
                    textAnnot['xaxis'] = 'x' + str(i_axis)
                    textAnnot['yaxis'] = 'y' + str(i_axis)
                    
                    data.append(textAnnot)
                    
                    layout['xaxis' + str(i_axis)] = {
                        'range': [args['start'], args['stop']],
                        'zeroline': False,
                        'showgrid': False,
                        'domain' : [0.1,1],
                        'anchor' : 'y' + str(i_axis),
                        'showticklabels': False
                        }
                    
                    layout['yaxis' + str(i_axis)] = {
                        'range': [-0.25, max(data_annot['textAnnot']['y'])+1],
                        'showgrid': False,
                        'zeroline': False,
                        'ticks':'',
                        'showticklabels': False,
                        'domain' : [func.setTopYDomain(top_y_domain = top_y_domain, height =  param_visu['annot']), top_y_domain],
                        'anchor' : 'x' + str(i_axis)
                        }
                        
                    # shapes
                    for i_shape in range(0, len(data_annot['shapesAnnot'])):

                        s = data_annot['shapesAnnot'][i_shape].copy()

                        s['xref'] = 'x' + str(i_axis)
                        s['yref'] = 'y' + str(i_axis)
	
                        shapes.append(s)

                    i_axis = i_axis + 1
					
                    top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['annot'])
						
						        
        if visu == 'heatmap':                
  
            cmap = func.get_color_scale()         

            scale_visu_ = scale_visu[0]

            zmax = np.max([func.getSampleMax(description_data = description_data, sample_name = s) for s in sample_visu])                
            
            if scale_visu_ == 'log':

                zmax = np.log2(zmax)

            # data heatmap
            
            if is_heatmap_stranded:            
            
                d = func.getHeatmapTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_names = sample_visu, scale = scale_visu_, 
                strand = 'F',description_data = description_data, wd = args['wd'], i_axis = i_axis, cmap = cmap, zmax = zmax)           

                title = "+ strand"
            
            else :
                
                d = func.getHeatmapTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_names = sample_visu, scale = scale_visu_,
                strand = 'both', description_data = description_data, wd = args['wd'], i_axis = i_axis, cmap = cmap, zmax = zmax)               

                title = ""                
                
            data.append(d)                
            
            # layout heatmap 
            layout['xaxis' + str(i_axis)] = {
                'range': [args['start'], args['stop']],
                'domain' : [0.1,1],
                'anchor' : 'y' + str(i_axis)
                }
            
            layout['yaxis' + str(i_axis)] = {
                'domain' : [func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['heatmap']), top_y_domain],
                'anchor' : 'x' + str(i_axis),
                'title' : title
                }
           
            top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['heatmap'])

            i_axis = i_axis + 1
           
            if is_annot_to_plot:
                
                n_bloc_layout = n_bloc_layout + 1

                # data annot
                textAnnot = data_annot['textAnnot'].copy()    
                        
                textAnnot['xaxis'] = 'x' + str(i_axis)
                textAnnot['yaxis'] = 'y' + str(i_axis)
                        
                data.append(textAnnot)

                # layout annot
                layout['xaxis' + str(i_axis)] = {
                    'range': [args['start'], args['stop']],
                    'zeroline': False,
                    'showgrid': False,
                    'domain' : [0.1,1],
                    'anchor' : 'y' + str(i_axis),
                    'showticklabels': False
                    }
                    
                layout['yaxis' + str(i_axis)] = {
                    'range': [-0.25, max(data_annot['textAnnot']['y'])+1],
                    'showgrid': False,
                     'zeroline': False,
                    'ticks':'',
                    'showticklabels': False,
                    'domain' : [func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['annot']), top_y_domain],
                    'anchor' : 'x' + str(i_axis)
                    }
               
                # shapes
                for i_shape in range(0, len(data_annot['shapesAnnot'])):

                    s = data_annot['shapesAnnot'][i_shape].copy()

                    s['xref'] = 'x' + str(i_axis)
                    s['yref'] = 'y' + str(i_axis)
	
                    shapes.append(s)

                i_axis = i_axis + 1
					
                top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['annot'])
            
            if is_heatmap_stranded:

                n_bloc_layout = n_bloc_layout + 1
                
                if len(data_annot['textAnnot']['text']) == 0:
                
                    top_y_domain = top_y_domain - param_visu['margin']

                # data heat map reverse
                d = func.getHeatmapTrace(chr = args['chr'], start = args['start'], stop = args['stop'], sample_names = sample_visu, scale = scale_visu_, 
                strand = 'R', description_data = description_data, wd = args['wd'], i_axis =  i_axis, cmap = cmap, zmax = zmax)                    

                data.append(d)
                           
                # layout heatmap 
                layout['xaxis' + str(i_axis)] = {
                    'range': [args['start'], args['stop']],
                    'domain' : [0.1,1],
                    'anchor' : 'y' + str(i_axis)
                    }
            
                layout['yaxis' + str(i_axis)] = {
                    'domain' : [(top_y_domain - param_visu['heatmap']), top_y_domain],
                    'anchor' : 'x' + str(i_axis),
                    'title' : "- strand"
                    }
           
                top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['heatmap'])

                i_axis = i_axis + 1    
  
            samples_left[which_samples] = ''

            # legend heatmap
            n_bloc_layout = n_bloc_layout + 1

            if is_heatmap_stranded == False and is_annot_to_plot == False:

                top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['margin'])
            
            # data           
            d = func.getHeatmapLegend(zmax = int(np.ceil(zmax).tolist()), cmap = cmap, i_axis = i_axis)            
 
            data.append(d)            
            
            # layout
            layout['xaxis' + str(i_axis)] = {
                'domain' : [0.3,0.8],
                'anchor' : 'y' + str(i_axis), 
                'ticks' : "",
                'title' : 'log2 ' * (scale_visu[0] == 'log') + 'tag/nt',
                'side' : 'bottom'
					}
            
            layout['yaxis' + str(i_axis)] = {                    
                'domain' : [func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['margin']), top_y_domain],
                'anchor' : 'x' + str(i_axis),
                'showticklabels': False,
                'ticks' : ""
					}            
            
            i_axis = i_axis + 1

            top_y_domain = func.setTopYDomain(top_y_domain = top_y_domain, height = param_visu['margin']) 

#nrow_annot = (len(data_annot['textAnnot']['text']) > 0) * 1 
#nrow_line = (len(samples_visu['line']) > 0) * 1
#nrow_fill = len(samples_visu['fill']) 
#nrow_heatmap = (len(samples_visu['heatmap']) > 0) * 2 + is_heatmap_stranded * 1 

#nrow = nrow_line + nrow_fill + nrow_annot + nrow_heatmap

nrow = n_bloc_layout

layout['grid'] = {
    'rows' : nrow, 
    'columns' : 1, 
    'pattern' : 'independent'
		}

if is_annot_to_plot:

    layout['shapes'] = shapes

layout['margin'] = param_visu['margins_out']

res = [data, layout, window_height]

print(json.dumps(res, separators=(',',':')))

#for i in range(1,i_axis):

#    print(layout['xaxis'+str(i)]['domain'])
#    print(layout['yaxis'+str(i)]['domain'])

#print(layout['grid'])
