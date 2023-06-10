# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 21:04:29 2019

@author: ugo
"""

##########
#  libs  #
##########

import os
import sys
import json
import numpy as np
import functions as func

###################
#  get arguments  #
###################

args = func.parseArgs()

# chromosome
CHROM = args['chr'] if 'chr' in args else None

# start window
START = int(args['start']) if 'start' in args else None

# stop windiw
STOP = int(args['stop']) if 'stop' in args else None

# samples
SAMPLES = np.array(args['samples'].split(",")) if 'samples' in args else None
n_samples = len(SAMPLES) 

# visualization
VISU = args['visu'].split(",") if 'visu' in args else ['line']*n_samples
if len(VISU) != n_samples:
    VISU = [VISU[0]]*n_samples

# scale
SCALE = args['scale'].split(",") if 'scale' in args else ['linear']*n_samples
if len(SCALE) != n_samples:
    SCALE = [SCALE[0]]*n_samples

# lib type
LIBTYPE = args['libType'].split(",") if 'libType' in args else ['stranded']*n_samples
if len(LIBTYPE) != n_samples:
    LIBTYPE = [LIBTYPE[0]]*n_samples

# normalization
NORMALIZED = args['norm'].split(",") if 'norm' in args else [True]*n_samples
if len(NORMALIZED) != n_samples:
    NORMALIZED = [NORMALIZED[0]]*n_samples
NORMALIZED = (np.array(NORMALIZED) == "yes").tolist()

# line color
COLOR = args['color'].split(",") if 'color' in args else ["#000000"]*n_samples
if len(COLOR) != n_samples:
    COLOR = [COLOR[0]]*n_samples

# line type
LINETYPE = args['lineType'].split(",") if 'libType' in args else ['solid']*n_samples
if len(LINETYPE) != n_samples:
    LINETYPE = [LINETYPE[0]]*n_samples

# annot file
ANNOT_FILE = args['annot'] if 'annot' in args else None

# description data file
DESCRIPTION_DATA_FILE = args['description_data'] if 'description_data' in args else None

# annot feature types to show
TYPES_TO_SHOW = args['types_to_show'].split(",") if 'types_to_show' in args else "all" 

# show transcript name
SHOW_TRANSCRIPT_NAME = args['show_transcript_name'] == 'yes' if 'show_transcript_name' in args else False

# show transcript name
COLLAPSE_TRANSCRIPTS = args['collapse_transcripts'] == 'yes' if 'collapse_transcripts' in args else False

##########################
#  get description_data  #
##########################
# description : 
#   file_F
#   file_R
#   replicate_name
#   cond_name
#   norm_coeff
#   stranded (not used)
#   replicate_col
#   replicate_line
#   cond_col
#   cond_line
#   group (not used)

description_data = func.descriptionData(DESCRIPTION_DATA_FILE)

##################################
#       get annotation file      #
##################################

annotation = func.Annotation(annotFile = ANNOT_FILE, chrWindow = CHROM, startWindow = START, stopWindow = STOP, types_allowed = TYPES_TO_SHOW, show_transcript_name = SHOW_TRANSCRIPT_NAME)

if os.path.exists(ANNOT_FILE):
    annotation.readAnnotFile()

##############################
#   Visualisation parameters #
##############################

visus_order = ['line','fill','heatmap']

index_samples_visu = {}

for visu in visus_order:
    
    index_samples_visu[visu] = [i for i in range(0, len(VISU)) if VISU[i] == visu] 

##########################
#  get data for plotly   #
##########################

coverageData = func.coverageData(chrWindow = CHROM, startWindow = START, stopWindow = STOP)

windowLayout = func.windowLayout(startWindow = START, stopWindow = STOP)

iBlockLayout = 0

samples_left = SAMPLES

for visu in visus_order:
    
    index_samples = index_samples_visu[visu]
    
    nb_sample_visu = len(index_samples)
    
    if nb_sample_visu > 0:
        
        sampleNames_visu = [SAMPLES[i] for i in index_samples]        
        
        lib_type_visu = [LIBTYPE[i] for i in index_samples] 
        
        scale_visu = [SCALE[i] for i in index_samples]   
        
        normalized_visu = [NORMALIZED[i] for i in index_samples]
        
        if iBlockLayout > 0:
            
            windowLayout.addMargin()
        
        if visu == 'line':
            
            iBlockLayout = iBlockLayout + 1
            
            scale_visu_ = scale_visu[0]
            
            colorLine = None
            
            if COLOR is not None:
                
                colorLine = [COLOR[i] for i in index_samples] 
            
            lineType = None
            
            if LINETYPE is not None:
                
                lineType = [LINETYPE[i] for i in index_samples]                
            
            coverageData.getLineTraces(sampleNames = sampleNames_visu, scale = scale_visu_, libraryTypes = lib_type_visu, normalized = normalized_visu, description_data = description_data, blockLayout = iBlockLayout, color = colorLine, lineType = lineType)
            
            windowLayout.setLineLayout(blockLayout = iBlockLayout, isLog = (scale_visu_ == 'log2'))
            
            samples_left = ['' if i in index_samples else samples_left[i] for i in range(0,len(samples_left))]
            
            if annotation.isAnnotToPlot and (samples_left.count('') == len(samples_left)): 
                
                # margin
                windowLayout.addMargin()
                
                iBlockLayout = iBlockLayout + 1
                
                annotation.setTraceAndShapes(blockLayout = iBlockLayout, collapse_transcripts = COLLAPSE_TRANSCRIPTS)
                
                # data
                coverageData.getAnnotData(annot = annotation, blockLayout = iBlockLayout)
                
                # layout
                windowLayout.setAnnotLayout(blockLayout = iBlockLayout, minY = min(annotation.trace['y']))
        
        if visu == 'fill':
            
            blockLayoutMem = iBlockLayout + 1
            
            yRange = [0,0]
            
            for i in range(0, nb_sample_visu):
                
                iBlockLayout = iBlockLayout + 1
                
                yRange_ = coverageData.getFillTrace(sampleName = sampleNames_visu[i], scale = scale_visu[i], libraryType = lib_type_visu[i], normalized = normalized_visu[i], description_data = description_data, blockLayout = iBlockLayout)
                
                if yRange[0] > yRange_[0]:
                    
                    yRange[0] = yRange_[0]
                    
                if yRange[1] < yRange_[1]:
                    
                    yRange[1] = yRange_[1]
                
                text = sampleNames_visu[i]
                
                if scale_visu[i] == 'log2':
                    
                    text = text + ', log2 read/nt'
                else:
                    text = text + ', read/nt'
                
                if not normalized_visu[i]:
                    text = text + ' (raw)' 
                
                windowLayout.setFillLayout(blockLayout = iBlockLayout, text = text)
                
                if i < (nb_sample_visu - 1):
                    
                    windowLayout.addMargin()
                
            windowLayout.setYRange(blockLayouts = list(range(blockLayoutMem, iBlockLayout + 1)), yRange = yRange)
            
            samples_left = ['' if i in index_samples else samples_left[i] for i in range(0,len(samples_left))]
            
            if annotation.isAnnotToPlot and (samples_left.count('') == len(samples_left)): 
                
                # margin
                windowLayout.addMargin()
                
                iBlockLayout = iBlockLayout + 1
                
                annotation.setTraceAndShapes(blockLayout = iBlockLayout, collapse_transcripts = COLLAPSE_TRANSCRIPTS)
                
                # data
                coverageData.getAnnotData(annot = annotation, blockLayout = iBlockLayout)   
                
                # layout
                windowLayout.setAnnotLayout(blockLayout = iBlockLayout, minY = min(annotation.trace['y']))
        
        if visu == 'heatmap':
            
            iBlockLayout = iBlockLayout + 1
            
            scale_visu_ = scale_visu[0]
            
            lib_type_visu_ = lib_type_visu[0]
            
            if lib_type_visu_ == "stranded":
                
                strand = 'F'
                
            else:
                
                strand = 'both'
            
            # data
            coverageData.getHeatmapTrace(sampleNames = sampleNames_visu, scale = scale_visu_, strand = strand, normalized = normalized_visu, description_data = description_data, blockLayout = iBlockLayout)
            
            # layout
            windowLayout.setHeatmapLayout(blockLayout = iBlockLayout, nSample = nb_sample_visu, strand = 'strand +' if strand == 'F' else '', showXTicks = False if strand == 'F' else True)
            
            if annotation.isAnnotToPlot:
                
                # margin
                windowLayout.addMargin()
                
                iBlockLayout = iBlockLayout + 1
                
                annotation.setTraceAndShapes(blockLayout = iBlockLayout, collapse_transcripts = COLLAPSE_TRANSCRIPTS)
                
                # data
                coverageData.getAnnotData(annot = annotation, blockLayout = iBlockLayout)   
                
                # layout
                windowLayout.setAnnotLayout(blockLayout = iBlockLayout, minY = min(annotation.trace['y']))
                
                # margin
                windowLayout.addMargin()
                
            # if heatmap visu is stranded 
            
            if lib_type_visu_ == "stranded":
                
                if annotation.isAnnotToPlot == False:
                    
                    # margin
                    windowLayout.addMargin()
                
                iBlockLayout = iBlockLayout + 1
                
                # data
                coverageData.getHeatmapTrace(sampleNames = sampleNames_visu, scale = scale_visu_, strand = 'R', normalized = normalized_visu, description_data = description_data, blockLayout = iBlockLayout)
                
                # layout
                windowLayout.setHeatmapLayout(blockLayout = iBlockLayout, nSample = nb_sample_visu, strand = 'strand -')
            
            # heatmap legend
            
            # margin
            windowLayout.addMargin(75)
            
            iBlockLayout = iBlockLayout + 1
            
            # data
            coverageData.getHeatmapLegend(blockLayout = iBlockLayout)
            
            # layout
            windowLayout.setHeatmapLegendLayout(blockLayout = iBlockLayout, scale = scale_visu_)
            
# set y domains
windowLayout.calcYdomain(nBlockLayout = iBlockLayout)

windowLayout.setGrid(nRow = iBlockLayout)

windowLayout.addShapes(annotation.shapes)

windowLayout.setOutMargin(l = 100, r = 100, b = 25, t = 25)

res = [coverageData.data, windowLayout.layout, windowLayout.window_height]

print(json.dumps(res, separators=(',',':')))

