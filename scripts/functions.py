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
import tabix
import urllib.parse

###############
#  functions  #   
############### 

# for annotation processing

class Annotation:
    
    def __init__(self, annotFile, chrWindow, startWindow, stopWindow, types_allowed, show_transcript_name):
        
        self.annotFile = annotFile
        self.indexed = annotFile.endswith(".gz")
        
        self.chrWindow = chrWindow
        self.startWindow = int(startWindow)
        self.stopWindow = int(stopWindow)
        self.spanWindow = self.stopWindow - self.startWindow
        
        self.parking = [np.array([0] * self.spanWindow)]
        
        self.annot = {}
        self.attributes = ["gene_id","gene_name","gene_type","transcript_id","transcript_name","transcript_type"]
        self.types_allowed = set(types_allowed)
        self.isAnnotToPlot = False
        self.show_transcript_name = show_transcript_name
        
        self.shapes = []
        self.trace = {
            'x':[],
            'y':[],
            'text':[],
            'mode':'text',
            'hovertext' : [],
            'hoverinfo' : 'text',
            'textfont': {
                'size': 10
            },
            'showlegend': False
        }
        
        self.blockLayout = 0
        self.layout = {}
    
    ### readAnnotFile : read gtf file for a given window, store info in annot and build annot_index 
    # only take gene, transcript, exon & CDS lines

    # internal function used in readAnnotFile
    def __readGtfAttributes(self, attributes_line):
        
        attributes = {}
        res = []
        
        for field in attributes_line.split(";"):
            field = field.strip().split(" ")
            if self.attributes.count(field[0]) > 0:
                attributes[field[0]] = field[1].strip("\"")
        
        for attr in self.attributes:
            if attr in attributes:
                res.append(attributes[attr])
            else:
                res.append("")
        
        return(res)
    
    # internal function used in readAnnotFile to build annot_index
    # build annot_index, dict with info about partent-child relationship between annotation features
    def __setAnnotLine(self, line):
        
        chr, source, type, start, end, score, strand, frame, attr_line = line
        start = int(start)
        end = int(end)
        
        gene_id, gene_name, gene_type, transcript_id, transcript_name, transcript_type = self.__readGtfAttributes(attr_line)
        
        if type == "gene" and gene_type in self.types_allowed:
            if not gene_id in self.annot:
                self.annot[gene_id] = {
                    "chr" : chr,
                    "start" : start,
                    "end" : end,
                    "strand" : strand,
                    "gene_id" : gene_id,
                    "gene_name" : gene_name,
                    "gene_type" : gene_type,
                    "transcripts" : {}
                }
            else:
                self.annot[gene_id]["chr"] = chr
                self.annot[gene_id]["start"] = start
                self.annot[gene_id]["end"] = end
                self.annot[gene_id]["strand"] = strand
        
        if type == "transcript" and gene_type in self.types_allowed:
            if not gene_id in self.annot:
                self.annot[gene_id] = {
                    "gene_id" : gene_id,
                    "gene_name" : gene_name,
                    "gene_type" : gene_type,
                    "transcripts" : {}
                }
            if not transcript_id in self.annot[gene_id]["transcripts"]:
                self.annot[gene_id]["transcripts"][transcript_id] = {
                    "chr" : chr,
                    "start" : start,
                    "end" : end,
                    "strand" : strand,
                    "transcript_id" : transcript_id,
                    "transcript_name" : transcript_name,
                    "transcript_type" : transcript_type,
                    "exon" : [],
                    "CDS" : []
                }
            else:
                self.annot[gene_id]["transcripts"][transcript_id]["chr"] = chr
                self.annot[gene_id]["transcripts"][transcript_id]["start"] = start
                self.annot[gene_id]["transcripts"][transcript_id]["end"] = end
                self.annot[gene_id]["transcripts"][transcript_id]["strand"] = strand
        
        if (type == "exon" or type == "CDS") and gene_type in self.types_allowed:
            if not gene_id in self.annot:
                self.annot[gene_id] = {
                    "gene_id" : gene_id,
                    "gene_name" : gene_name,
                    "gene_type" : gene_type,
                    "transcripts" : {}
                }
            if not transcript_id in self.annot[gene_id]["transcripts"]:
                self.annot[gene_id]["transcripts"][transcript_id] = {
                    "chr" : chr,
                    "start" : start,
                    "end" : end,
                    "strand" : strand,
                    "transcript_id" : transcript_id,
                    "transcript_name" : transcript_name,
                    "transcript_type" : transcript_type,
                    "exon" : [],
                    "CDS" : []
                }
            self.annot[gene_id]["transcripts"][transcript_id][type].append([start, end])
    
    # readAnnotFile
    def readAnnotFile(self):
        
        i = 0
        
        if os.path.exists(self.annotFile):
            if self.indexed:
                tb = tabix.open(self.annotFile)
                try:
                    records = tb.query(self.chrWindow, self.startWindow, self.stopWindow)
                except:
                    records=[]
            else:
                records = open(self.annotFile)
            
            for record in records:
                if not self.indexed:
                    if record[0] == "#":
                        continue
                    record = record[0:len(record)-1].split("\t")
                
                if (record[0] == self.chrWindow) and (int(record[3]) < self.stopWindow) and (int(record[4]) > self.startWindow) and (int(record[3]) < int(record[4])):
                    
                    self.__setAnnotLine(record)
        
        if len(self.annot) > 0:
            self.isAnnotToPlot = True
    
    ### set trace and shapes : add data to trace and shapes
     
    # internal function used in addShape : add rectangle to shapes
    def __getRectangle(self, start, stop, yPos):
        
        line_height = 0.01
        
        return({
            'type': 'rect',
            'x0': start,
            'y0': yPos - line_height,
            'x1': stop,
            'y1': yPos + line_height,
            'line': {
                'color': 'DodgerBlue'
            },
            'fillcolor': 'DodgerBlue'
        })
    
    # internal function used in addShape : add arrow to shapes    
    def __getArrow(self, start, stop, yPos, strand):
        
        line_height = 0.001
        
        head_height = 0.03
        
        head_length = self.spanWindow * 0.01
        
        if strand == "+":
        
            if head_length < (stop-start):
            
                path = (
                    ' M ' + str(start) + ',' + str(yPos - line_height) + 
                    ' L ' + str(start) + ',' + str(yPos + line_height) +
                    ' L ' + str(stop - head_length) + ',' + str(yPos + line_height) +
                    ' L ' + str(stop - head_length) + ',' + str(yPos + head_height) +
                    ' L ' + str(stop) + ',' + str(yPos) +
                    ' L ' + str(stop - head_length) + ',' + str(yPos - head_height) +
                    ' L ' + str(stop - head_length) + ',' + str(yPos - line_height) + 
                    ' Z '
                    )
                    
            else:
            
                path = (
                    ' M ' + str(start) + ',' + str(yPos - line_height) + 
                    ' L ' + str(start) + ',' + str(yPos + line_height) +
                    ' L ' + str(stop) + ',' + str(yPos) +
                    ' Z '
                    )
        
        else:
        
            if head_length < (stop-start):
                
                path = (
                    ' M ' + str(stop) + ',' + str(yPos - line_height) + 
                    ' L ' + str(stop) + ',' + str(yPos + line_height) +
                    ' L ' + str(start + head_length) + ',' + str(yPos + line_height) +
                    ' L ' + str(start + head_length) + ',' + str(yPos + head_height) +
                    ' L ' + str(start) + ',' + str(yPos) +
                    ' L ' + str(start + head_length) + ',' + str(yPos - head_height) +
                    ' L ' + str(start + head_length) + ',' + str(yPos - line_height) + 
                    ' Z '
                    )
            
            else:
                
                path = (
                    ' M ' + str(stop) + ',' + str(yPos - line_height) + 
                    ' L ' + str(stop) + ',' + str(yPos + line_height) +
                    ' L ' + str(start) + ',' + str(yPos) +
                    ' Z '
                    )
                    
        return({
            'type': 'path',
            'path': path,
            'fillcolor': "Black",
            'line': {
                'color': "Black"
                }
            })
    
    # internal function used in addShape : add box to shapes
    def __getBox(self, start, stop, yPos, strand, size):
        
        head_length = self.spanWindow * 0.01
        
        if size == "small":
            
            s = 0.1
            
            fill = "Grey"
            
        else:
            
            fill = "DodgerBlue"
            
            s = 0.25
        
        if strand == "+":
            
            if head_length < (stop-start):
                
                path = (
                    ' M ' + str(start) + ',' + str(yPos - s) + 
                    ' L ' + str(start) + ',' + str(yPos + s) +
                    ' L ' + str(stop - head_length) + ',' + str(yPos + s) +
                    ' L ' + str(stop) + ',' + str(yPos) +
                    ' L ' + str(stop - head_length) + ',' + str(yPos - s) + 
                    ' Z '
                    )
                
            else:
                
                path = (
                    ' M ' + str(start) + ',' + str(yPos - s) + 
                    ' L ' + str(start) + ',' + str(yPos + s) +
                    ' L ' + str(stop) + ',' + str(yPos) +
                    ' Z '
                    )
        
        else:
            
            if head_length < (stop-start):
                
                path = (
                    ' M ' + str(stop) + ',' + str(yPos - s) + 
                    ' L ' + str(stop) + ',' + str(yPos + s) +
                    ' L ' + str(start + head_length) + ',' + str(yPos + s) +
                    ' L ' + str(start) + ',' + str(yPos) +
                    ' L ' + str(start + head_length) + ',' + str(yPos - s) + 
                    ' Z '
                    )
            
            else:
                
                path = (
                    ' M ' + str(stop) + ',' + str(yPos - s) + 
                    ' L ' + str(stop) + ',' + str(yPos + s) +
                    ' L ' + str(start) + ',' + str(yPos) +
                    ' Z '
                    )
        
        return({
            'type': 'path',
            'path': path,
            'fillcolor': fill,
            'line': {
                'color': 'Black',
                'width': 0.7
                }
            })
    
    # internal function used in addData : add shape
    def __addShape(self, shape, start, stop, yPos, strand = None, size = None):
        
        if strand == ".":
            
            Shape = self.__getRectangle(start = start, stop = stop, yPos = yPos)
        
        else:
            
            if shape == "Rectangle":
                
                Shape = self.__getRectangle(start = start, stop = stop, yPos = yPos)
            
            if shape == "Arrow":
                
                Shape = self.__getArrow(start = start, stop = stop, yPos = yPos, strand = strand)
            
            if shape == "Box":
                
                Shape = self.__getBox(start = start, stop = stop, yPos = yPos, strand = strand, size = size)
        
        Shape['xref'] = 'x' + str(self.blockLayout)
        
        Shape['yref'] = 'y' + str(self.blockLayout)
        
        self.shapes.append(Shape)
    
    # internal function used in addData : calculate y position for a given gene
    def __calcYposGene(self, startGene, stopGene):
        
        startGene = startGene - round((self.stopWindow - self.startWindow) * 0.01)
        
        stopGene = stopGene + round((self.stopWindow - self.startWindow) * 0.01)
        
        if startGene < self.startWindow:
            
            start_ = 1
            
        else:
            
            start_ = startGene - self.startWindow + 1
        
        if stopGene > self.stopWindow:
            
            stop_ = self.spanWindow - 1
            
        else:
            
            stop_ = stopGene - self.startWindow + 1
        
        yPos = -1
        
        j = 0
        
        while yPos == -1:
            
            maxYposGeneSpan = np.max(self.parking[j][start_:stop_]) 
            
            if maxYposGeneSpan == 0:
                
                yPos = j + 1
                
            else:
                
                j = j + 1
                
                if j == len(self.parking):
                    
                    self.parking.append(np.array([0] * self.spanWindow))
                    
                    yPos = j + 1
        
        self.parking[j][start_:stop_] = [1]*len(self.parking[j][start_:stop_])
        
        return(-yPos)
    
    # internal function used in setData : add data to trace and shapes for a given gene
    def __addDataGene(self, startGene, stopGene, yPos, geneID, geneType, strand, shape, size = None):
        
        if geneID != "":
            
            stopGeneWindow = stopGene
            
            if stopGene > self.stopWindow:
                
                stopGeneWindow = self.stopWindow
            
            startGeneWindow = startGene
            
            if startGene < self.startWindow:
                
                startGeneWindow = self.startWindow
            
            self.trace['x'].append(startGeneWindow + (stopGeneWindow - startGeneWindow)/2)
            
            yText = 0.4
            
            self.trace['y'].append(yPos + yText)
            
            self.trace['text'].append(geneID)
            
            self.trace['hovertext'].append(geneType)
            
        self.__addShape(shape = shape, start = startGene, stop = stopGene, yPos = yPos, strand = strand, size = size)
    
    # internal function used in setTraceAndShapes : get name of gene/transcript
    def __getName(self, index_line, transcriptName):
        
        if transcriptName:
            
            name = self.__getGeneInfo(index_line = index_line, which_info = "transcript_name")
            
            if name == '':
                
                name = self.__getGeneInfo(index_line = index_line, which_info = "ID")
        
        else:
            
            name = self.__getGeneInfo(index_line = index_line, which_info = "gene_name")
            
            if name == '':
                
                name = self.__getGeneInfo(index_line = index_line, which_info = "gene")
                
                if name == '':
                    
                    name = self.__getGeneInfo(index_line = index_line, which_info = "ID")
                    
        return(urllib.parse.unquote(name))
    
    def __setBlockLayout(self, blockLayout):
        
        self.blockLayout = blockLayout
        
        self.trace['xaxis'] = 'x' + str(blockLayout)
        
        self.trace['yaxis'] = 'y' + str(blockLayout)
    
    ### set trace and shapes data for all genes in annotation
    def setTraceAndShapes(self, blockLayout, collapse_transcripts):
        
        self.__setBlockLayout(blockLayout)
        
        for gene_id in self.annot.keys():
            
            if collapse_transcripts:
                
                start = self.annot[gene_id]["start"]
                end = self.annot[gene_id]["end"]
                strand = self.annot[gene_id]["strand"]
                gene_type = self.annot[gene_id]["gene_type"]
                gene_name = self.annot[gene_id]["gene_name"]
                
                yPosGene = self.__calcYposGene(startGene = start, stopGene = end)
                
                self.__addDataGene(startGene = start, stopGene = end, yPos = yPosGene, geneID = gene_name, geneType = gene_type, strand = strand, shape = "Arrow", size = "small")
                
                for transcript_id in self.annot[gene_id]["transcripts"]:
                    for i_exon in range(0, len(self.annot[gene_id]["transcripts"][transcript_id]["exon"])):
                        start_, end_ = self.annot[gene_id]["transcripts"][transcript_id]["exon"][i_exon]
                        self.__addDataGene(startGene = start_, stopGene = end_, yPos = yPosGene, geneID = '', geneType = gene_type, strand = strand, shape = "Box", size = "small")
                
                for transcript in self.annot[gene_id]["transcripts"]:
                    for i_cds in range(0, len(self.annot[gene_id]["transcripts"][transcript_id]["CDS"])):
                        start_, end_ = self.annot[gene_id]["transcripts"][transcript_id]["CDS"][i_cds]
                        self.__addDataGene(startGene = start_, stopGene = end_, yPos = yPosGene, geneID = '', geneType = gene_type, strand = strand, shape = "Box", size = "big")
            else:
                
                for transcript in self.annot[gene_id]["transcripts"]:
                    
                    start = self.annot[gene_id]["transcripts"][transcript_id]["start"]
                    end = self.annot[gene_id]["transcripts"][transcript_id]["end"]
                    strand = self.annot[gene_id]["transcripts"][transcript_id]["strand"]
                    gene_type = self.annot[gene_id]["transcripts"][transcript_id]["transcript_type"]
                    gene_name = self.annot[gene_id]["transcripts"][transcript_id]["transcript_name"]
                    
                    yPosGene = self.__calcYposGene(startGene = start, stopGene = end)
                    
                    self.__addDataGene(startGene = start, stopGene = end, yPos = yPosGene, geneID = gene_name, geneType = gene_type, strand = strand, shape = "Arrow", size = "small")
                    
                    for i_exon in range(0, len(self.annot[gene_id]["transcripts"][transcript_id]["exon"])):
                        start_, end_ = self.annot[gene_id]["transcripts"][transcript_id]["exon"][i_exon]
                        self.__addDataGene(startGene = start_, stopGene = end_, yPos = yPosGene, geneID = '', geneType = gene_type, strand = strand, shape = "Box", size = "small")
                    
                    for i_cds in range(0, len(self.annot[gene_id]["transcripts"][transcript_id]["CDS"])):
                        start_, end_ = self.annot[gene_id]["transcripts"][transcript_id]["CDS"][i_cds]
                        self.__addDataGene(startGene = start_, stopGene = end_, yPos = yPosGene, geneID = '', geneType = gene_type, strand = strand, shape = "Box", size = "big")

class descriptionData:
    
    def __init__(self, descriptionDataFile):
        
        self.description_data = {}
        
        field = ['file_F', 'file_R', 'replicate_name', 'cond_name', 'norm_coeff']
        
        for field_ in field:
        
            self.description_data[field_] = np.array([])
        
        description_data_file = open(descriptionDataFile)
        
        i = 0
        
        for line in description_data_file:
            
            line = line[0:len(line)-1].split("\t")
            
            if i == 0:
                
                header = line
                
            else:
                
                for i_col in range(0, len(line)):
                    
                    col = header[i_col]
                    
                    if col in self.description_data:
                        
                        self.description_data[col] = np.append(self.description_data[col], line[i_col])
            
            i = i + 1
        
        description_data_file.close()
    
    
    def getSampleInfo(self, sampleName, info):
        
        sampleIndex = np.where(np.array(self.description_data['replicate_name']) == sampleName)[0]
        
        if len(sampleIndex) == 0:
            
            sampleIndex = np.where(np.array(self.description_data['cond_name']) == sampleName)[0]
        
        if info == 'index':
            
            res = sampleIndex
        
        elif info == 'file_F' or info == 'file_R':
            
            res = np.array([self.description_data[info][i] for i in sampleIndex])
            
        else:
            
            res = self.description_data[info][sampleIndex]
            
        
        return(res.tolist())


class coverageData:
    
    def __init__(self, chrWindow, startWindow, stopWindow):
        
        self.chrWindow = chrWindow
        
        self.startWindow = startWindow
        
        self.stopWindow = stopWindow
        
        self.binSize = 2
        
        # compress x coordinates if window > 10000 bp
        if (stopWindow - startWindow) >= 10000:
            
            self.binSize = max(self.binSize, round((stopWindow - startWindow) / 10000)*2)
        
        self.xAxis = []
        
        if (stopWindow - startWindow) < 10000:
            
            self.xAxis = list(range(startWindow, (stopWindow + 1)))
        
        else:
            
            center = startWindow + round(self.binSize/2)
            
            while center < stopWindow:
                
                self.xAxis.append(center)
                
                center = center + round(self.binSize/2)
        
        self.colorScale = None
        
        self.maxSignal = 0
        
        self.data = []
    
    
    # internal function used in getSignal if window > 10000 bp
    def __compressSignal(self, signal):
        
        res = []
        
        if len(signal) < self.binSize:
            
            res = signal
        
        else:
            
            center = round(self.binSize/2)
            
            while center < len(signal):
                
                bottom = center - round(self.binSize/2)
                
                top = center + round(self.binSize/2)
                
                if top > (len(signal) - 1):
                    
                    top = len(signal) - 1
                
                res.append(np.mean(signal[bottom:top]))
                
                center = center + round(self.binSize/2)
        
        return(res)
    
    
    def __getSignalFromBigWig(self, sampleName, strand, scale, normalized, description_data, reverseNegative = True, getMax = False):
        
        repNames = description_data.getSampleInfo(sampleName = sampleName, info = 'replicate_name')
        
        n_samples = len(repNames)
        
        signal = np.array([0]*(self.stopWindow - self.startWindow))    
        
        for repName in repNames:
            
            if normalized:
                
                coeff = float(description_data.getSampleInfo(sampleName = repName, info = 'norm_coeff')[0])
            
            else:
                
                coeff = float(1)
            
            if strand == 'both':
                
                for file_str in ['file_F', 'file_R']:
                    
                    file = description_data.getSampleInfo(sampleName = repName, info = file_str)[0]
                    
                    if os.path.exists(file) == False:
                        
                        print("file " + file + " was not found")
                    
                    else:
                        
                        bw = pyBigWig.open(file)
                        
                        try:
                            signal = signal + np.nan_to_num(np.array(bw.values(self.chrWindow, self.startWindow, self.stopWindow)))*coeff
                        except:
                            pass
                        
                        bw.close()
            
            else:
                
                if strand == 'F':            
                    
                    file = description_data.getSampleInfo(sampleName = repName, info = 'file_F')[0] 
                
                else:
                    
                    file = description_data.getSampleInfo(sampleName = repName, info = 'file_R')[0]
                
                if os.path.exists(file) == False:
                        
                    print("file " + file + " was not found")
                
                else:
                    
                    bw = pyBigWig.open(file)
                    
                    try:
                        signal = signal + np.nan_to_num(np.array(bw.values(self.chrWindow, self.startWindow, self.stopWindow)))*coeff
                    except:
                        pass
                    
                    bw.close()
        
        signal = signal/n_samples
        
        if scale == 'log2':
            
            signal = np.log2(signal+1)
        
        if reverseNegative:    
            
            if strand == 'R':
                
                signal = -signal
        
        signal = signal.tolist()
        
        if self.binSize > 1:
            
            signal = self.__compressSignal(signal = signal)
            
        if getMax:
            
            self.maxSignal = max([self.maxSignal, max(signal)])
        
        return(signal)    
    
    
    def getLineTraces(self, sampleNames, scale, libraryTypes, normalized, description_data, blockLayout, color = None, lineType = None):
        
        for i_sample in range(0, len(sampleNames)):
            
            if color is not None:
                
                i_color = color[i_sample]
            
            else:
                
                i_color = "#000000"
            
            if lineType is not None:
                
                i_lty = lineType[i_sample]
                
            else:
                
                i_lty = 'solid'
            
            legendName = sampleNames[i_sample]
            
            if normalized[i_sample] == False:
                
                legendName = legendName + ' (raw)' 
            
            if libraryTypes[i_sample] == 'unstranded':
                
                signal = self.__getSignalFromBigWig(sampleName = sampleNames[i_sample], strand = 'both', scale = scale, normalized = normalized[i_sample], description_data = description_data)
                
                self.data.append({
                    'x' : self.xAxis, 
                    'y' : signal,
                    'mode' : 'lines',
                    'name' : legendName,
                    'hoverinfo' : 'skip',
                    'line' : {
                        'color' : i_color,
                        'dash' : i_lty,
                        'width' : 1
                        },
                    'xaxis' : 'x' + str(blockLayout),
                    'yaxis' : 'y' + str(blockLayout),
                    'legendgroup' : 'group' + str(i_sample + 1)
                    })
            
            else:
                
                signal_F = self.__getSignalFromBigWig(sampleName = sampleNames[i_sample], strand = 'F', scale = scale, normalized = normalized[i_sample], description_data = description_data)
                
                self.data.append({
                    'x' : self.xAxis, 
                    'y' : signal_F,
                    'mode' : 'lines',
                    'name' : legendName,
                    'hoverinfo' : 'skip',
                    'line' : {
                        'color' : i_color,
                        'dash' : i_lty,
                        'width' : 1
                        },
                    'xaxis' : 'x' + str(blockLayout),
                    'yaxis' : 'y' + str(blockLayout),
                    'legendgroup' : 'group' + str(i_sample + 1)
                    })
                    
                signal_R = self.__getSignalFromBigWig(sampleName = sampleNames[i_sample], strand = 'R', scale = scale, normalized = normalized[i_sample], description_data = description_data)
                
                self.data.append({
                    'x' : self.xAxis, 
                    'y' : signal_R,
                    'mode' : 'lines',
                    'name' : legendName,
                    'hoverinfo' : 'skip',
                    'line' : {
                        'color' : i_color,
                        'dash' : i_lty,
                        'width' : 1
                        },
                    'xaxis' : 'x' + str(blockLayout),
                    'yaxis' : 'y' + str(blockLayout),
                    'legendgroup' : 'group' + str(i_sample + 1),
                    'showlegend' :False
                    })
    
    
    def getFillTrace(self, sampleName, scale, libraryType, normalized, description_data, blockLayout):
        
        yRange = [0,0]
        
        if libraryType == 'unstranded':
            
            signal = self.__getSignalFromBigWig(sampleName = sampleName, strand = 'both', scale = scale, normalized = normalized, description_data = description_data)
            
            yRange = [0,max(signal)]
            
            self.data.append({
                'x' : self.xAxis, 
                'y' : signal,
                'fillcolor': 'FireBrick',
                'fill': 'tozeroy',
                'hoverinfo' : 'skip',
                'line': {
                    'color':'FireBrick'
                    },
                'xaxis' : 'x' + str(blockLayout),
                'yaxis' : 'y' + str(blockLayout),
                'showlegend' : False
                })
        
        else:
            
            signal_F = self.__getSignalFromBigWig(sampleName = sampleName, strand = 'F', scale = scale, normalized = normalized, description_data = description_data)
            
            yRange[1] = max(signal_F)
            
            self.data.append({
                'x' : self.xAxis, 
                'y' : signal_F,
                'fillcolor': 'FireBrick',
                'fill': 'tozeroy',
                'hoverinfo' : 'skip',
                'line': {
                    'color': 'FireBrick'
                    },
                'xaxis' : 'x' + str(blockLayout),
                'yaxis' : 'y' + str(blockLayout),
                'showlegend' : False
                })
            
            signal_R = self.__getSignalFromBigWig(sampleName = sampleName, strand = 'R', scale = scale, normalized = normalized, description_data = description_data)
            
            yRange[0] = min(signal_R)
            
            self.data.append({
                'x' : self.xAxis, 
                'y' : signal_R,
                'fillcolor': 'CornFlowerBlue',
                'fill': 'tozeroy',
                'hoverinfo' : 'skip',
                'line': {
                    'color': 'CornFlowerBlue'
                    },
                'xaxis' : 'x' + str(blockLayout),
                'yaxis' : 'y' + str(blockLayout),
                'showlegend' : False
                })
        
        return(yRange)
    
    
    def __setColorScale(self, col_min = [1,1,0.667], col_max = [0,0.33,0.33]):
        
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
        
        self.colorScale = colorscale
    
    
    def getHeatmapTrace(self, sampleNames, scale, strand, normalized, description_data, blockLayout):
        
        if self.colorScale is None:
            
            self.__setColorScale()
        
        mat = ['']*len(sampleNames)
        
        y_lab_=['']*len(sampleNames)
        
        for i in range(0,len(sampleNames)):
            
            i_ = (len(sampleNames)-1)-i
            
            y_lab_[i] = sampleNames[i_]
            
            if normalized[i_] == False:
                
                y_lab_[i] = sampleNames[i_] + " (raw)"
            
            mat[i] = self.__getSignalFromBigWig(sampleName = sampleNames[i_], strand = strand, scale = scale, normalized = normalized[i_], description_data = description_data, reverseNegative = False, getMax = True)
        
        scale_title = 'tag/nt'
        
        if scale == 'log2':
            
            scale_title = 'log2 ' + scale_title
        
        self.data.append({
            'z' : mat,
            'x' : self.xAxis,
            'y' : y_lab_,
            'xaxis' : 'x' + str(blockLayout),
            'yaxis' : 'y' + str(blockLayout),
            'type' : 'heatmap',
            'zmin' : 0,
            'zmax' : self.maxSignal,
            'colorscale' : self.colorScale,
            'hoverinfo' : 'skip',
            'colorbar': {
                'title' : {
                    'text' : scale_title
                    }
                },
            'showscale' : False
            })
    
    
    def getHeatmapLegend(self, blockLayout):
        
        if self.maxSignal == 0:
            
            z = [[0,0]]
            
        else:
            
            z = [list(range(0, int(self.maxSignal)))]
        
        self.data.append({
            'z' : z,
            'type' : 'heatmap',
            'zmin' : 0,
            'zmax' : self.maxSignal,
            'colorscale' : self.colorScale,
            'showscale' : False,
            'hoverinfo' : 'skip',
            'xaxis' : 'x' + str(blockLayout),
            'yaxis' : 'y' + str(blockLayout)
            })
    
    
    def getAnnotData(self, annot, blockLayout):
        
        self.data.append(annot.trace)


class windowLayout:
    
    def __init__(self, startWindow, stopWindow, line_height = 300, fill_height = 200, heatmap_height = 50, heatmap_legend_height = 50, margin_height = 25, annot_height = 35):
        
        self.layout = {"hovermode" : "closest"}
        
        self.window_height = 0
        
        self.xAxisRange = [startWindow, stopWindow]
        
        self.line_height = line_height
        
        self.fill_height = fill_height
        
        self.heatmap_height = heatmap_height
        
        self.heatmap_legend_height = heatmap_legend_height
        
        self.margin_height = margin_height
        
        self.annot_height = annot_height
    
    def setYdomain(self, blockLayout, blockLayoutHeight):
        
        domain = [self.window_height - blockLayoutHeight, self.window_height]
        
        self.window_height = self.window_height - blockLayoutHeight
        
        return(domain)
    
    
    def addMargin(self, size = None):
        
        if size is None:
            
            size = self.margin_height
        
        self.window_height = self.window_height - size
    
    
    def setLineLayout(self, blockLayout, isLog):
        
        self.layout['xaxis' + str(blockLayout)] = {
            'domain' : [0.1,1],
            'anchor' : 'y' + str(blockLayout),
            'range' : self.xAxisRange,
            'fixedrange' : True
                }
        
        self.layout['yaxis' + str(blockLayout)] = {
            'domain' : self.setYdomain(blockLayout = blockLayout, blockLayoutHeight = self.line_height),
            'anchor' : 'x' + str(blockLayout),
            'title' : 'log2 ' * isLog + 'tag/nt',
            'fixedrange' : True
            }
    
    
    def setFillLayout(self, blockLayout, text):
        
        self.layout['xaxis' + str(blockLayout)] = {
            'domain' : [0.1,1],
            'anchor' : 'y' + str(blockLayout),
            'range' : self.xAxisRange,
            'fixedrange' : True
            }

        self.layout['yaxis' + str(blockLayout)] = {
            'domain' : self.setYdomain(blockLayout = blockLayout, blockLayoutHeight = self.fill_height),
            'anchor' : 'x' + str(blockLayout),
            'title' : {
                'text' : text
                },
            'fixedrange' : True
            }
    
    
    def setHeatmapLayout(self, blockLayout, nSample, strand, showXTicks = True):
        
        self.layout['xaxis' + str(blockLayout)] = {
            'range': self.xAxisRange,
            'domain' : [0.1,1],
            'anchor' : 'y' + str(blockLayout),
            'showticklabels': showXTicks,
            'ticks' : "",
            'fixedrange' : True
            }
        
        self.layout['yaxis' + str(blockLayout)] = {
            'domain' : self.setYdomain(blockLayout = blockLayout, blockLayoutHeight = self.heatmap_height * nSample),
            'anchor' : 'x' + str(blockLayout),
            'ticks' : "",
            'title' : { 
                'text' : strand
                },
            'fixedrange' : True
            }
    
    
    def setHeatmapLegendLayout(self, blockLayout, scale):
        
        self.layout['xaxis' + str(blockLayout)] = {
            'domain' : [0.3,0.8],
            'anchor' : 'y' + str(blockLayout), 
            'ticks' : "",
            'title' : {
                'text' : 'log2 ' * (scale == 'log2') + 'tag/nt',
                'standoff' : 0
                },
            'side' : 'top',
            'fixedrange' : True
            }
            
        self.layout['yaxis' + str(blockLayout)] = {                    
            'domain' : self.setYdomain(blockLayout = blockLayout, blockLayoutHeight = self.heatmap_legend_height),
            'anchor' : 'x' + str(blockLayout),
            'showticklabels': False,
            'ticks' : "",
            'fixedrange' : True
            }
    
    
    def setAnnotLayout(self, blockLayout, minY):
        
        self.layout['xaxis' + str(blockLayout)] = {
            'range': self.xAxisRange,
            'zeroline': False,
            'showgrid': False,
            'domain': [0.1,1],
            'anchor': 'y' + str(blockLayout),
            'showticklabels': False,
            'fixedrange' : True
            }
        
        self.layout['yaxis' + str(blockLayout)] = {
            'range': [minY-0.75, 0],
            'showgrid': False,
            'zeroline': False,
            'showticklabels': False,
            'anchor' : 'x' + str(blockLayout),
            'domain' : self.setYdomain(blockLayout = blockLayout, blockLayoutHeight = self.annot_height*(-minY)),
            'fixedrange' : True
            }
    
    
    def addShapes(self, shapes):
        
        self.layout['shapes'] = shapes
    
    
    def calcYdomain(self, nBlockLayout):
        
        self.window_height = -int(np.ceil(self.window_height))
        
        for iBlockLayout in range(1, (nBlockLayout + 1)):
            
            d = self.layout['yaxis' + str(iBlockLayout)]['domain']
            
            domainFrac = [((d[0] + self.window_height) / self.window_height), ((d[1] + self.window_height) / self.window_height)]
            
            self.layout['yaxis' + str(iBlockLayout)]['domain'] = domainFrac
    
    
    def setGrid(self, nRow):
        
        self.layout['grid'] = {
            'rows' : nRow, 
            'columns' : 1, 
            'pattern' : 'independent'
            }
    
    def setOutMargin(self, l, r, b, t):
        
        self.layout['margin'] = { 'l': l,'r': r,'b': b,'t': t}
    
    
    def setYRange(self, blockLayouts, yRange):
        
        for i in blockLayouts:
            
            self.layout['yaxis' + str(i)]['range'] = yRange

# count table file
# count table for each sample, with also Chr, Type, Start, Stop, Strand, ID
class countTable:
    
    def __init__(self, description_data, chrom, start, stop, types):
        
        # description_data
        self.description_data = description_data
        
        # count table
        self.countTableHeader = description_data.description_data['replicate_name'].tolist()
        
        self.countTable = []
        
        # annot
        self.annotHeader = ['Chr', 'Type', 'Start', 'Stop', 'Strand', 'ID', 'Name', 'Length']
        
        self.annotTable = []
        
        # 
        self.chrom = chrom
        
        self.start = start
        
        self.stop = stop
        
        self.types = types
    
    
    def readCountTableIdx(self, countFile):
        
        # get file header
        import gzip
        
        lines = gzip.open(countFile, mode='rb')
        
        tmp = lines.readline().decode().rstrip().split("\t")
        
        tmp = [tmp[0].strip("#")] + tmp[1:7] + tmp[8].split(";")
        
        fileHeaderIndex = {}
        
        for i in range(0, len(tmp)):
            
            fileHeaderIndex[tmp[i]] = i
        
        lines.close()
        
        # tabix query
        
        if self.chrom is not None:
            
            tb = tabix.open(countFile)
            
            print("tb.query(" + self.chrom +", "+ str(self.start) + ",  " + str(self.stop), "\n")
            
            lines = tb.query(self.chrom, self.start, self.stop)
            
        
        for line in lines:
            
            if self.chrom is None:
                
                line = line.decode().rstrip().split("\t")
            
            types_ = line[fileHeaderIndex['Type']] if self.types is None else self.types
            
            if line[fileHeaderIndex['Type']] in types_:
                
                line = line[0:7] + line[8].split(";")
                
                # annot
                tmp = []
                
                for col in self.annotHeader:
                    
                    if col == 'Start' or col == 'Stop':
                        
                        tmp.append(int(line[fileHeaderIndex[col]]))
                    
                    else:
                        
                        tmp.append(line[fileHeaderIndex[col]])
                        
                self.annotTable.append(tmp)
                
                # counts
                tmp = []
                
                for col in self.countTableHeader:
                    
                    tmp.append(float(line[fileHeaderIndex[col]]))
                    
                self.countTable.append(tmp)
    
    
    def readCountTable(self,countFile):
        
        # get file header
        lines = open(countFile)
        
        tmp = lines.readline().strip().split("\t")
        
        fileHeaderIndex = {}
        
        for i in range(0, len(tmp)):
            
            fileHeaderIndex[tmp[i]] = i
        
        #read file
        
        for line in lines:
            
            line = line.strip().split("\t")
            
            chrom_ = line[fileHeaderIndex['Chr']] if self.chrom is None else self.chrom
            
            if line[fileHeaderIndex['Chr']] == chrom_ and chrom_ != 'Chr':
                
                start_ = int(line[fileHeaderIndex['Start']]) if self.start is None else self.start
                
                stop_ = int(line[fileHeaderIndex['Stop']]) if self.stop is None else self.stop
                
                if (int(line[fileHeaderIndex['Start']]) < stop_) and (int(line[fileHeaderIndex['Stop']]) > start_):
                    
                    types_ = line[fileHeaderIndex['Type']] if self.types is None else self.types
                        
                    if line[fileHeaderIndex['Type']] in types_:
                        
                        # annot
                        tmp = []
                        
                        for col in self.annotHeader:
                            
                            if col == 'Start' or col == 'Stop':
                                
                                tmp.append(int(line[fileHeaderIndex[col]]))
                                
                            else:
                                
                                tmp.append(line[fileHeaderIndex[col]])
                        
                        self.annotTable.append(tmp)
                        
                        # counts
                        tmp = []
                        
                        for col in self.countTableHeader:
                            
                            tmp.append(float(line[fileHeaderIndex[col]]))
                            
                        self.countTable.append(tmp)
        
        lines.close()

    
    def calcSampleExprs(self, i_line, sample, norm, log, countType):
        
        replicates = self.description_data.getSampleInfo(sample, 'replicate_name')
        
        res = 0.0
        
        for replicate in replicates:
            
            coeff = self.description_data.getSampleInfo(replicate, 'norm_coeff')[0] if norm else 1
            
            res = res + float(self.countTable[i_line][self.countTableHeader.index(replicate)]) * float(coeff)
        
        res = res / len(replicates)
        
        if countType == 'densities':
            
            l = float(self.annotTable[i_line][self.annotHeader.index('Stop')]) - float(self.annotTable[i_line][self.annotHeader.index('Start')]) + 1
            
            res = res/l
            
        if log:
            
            res = np.log2(res) if res > 0 else float('-inf') 
        
        return(res)
    
    
    def calcRatio(self, i_line, sample1, sample2, norm, log):
        
        samples = [sample1, sample2]
        
        vals = []
        
        for i in range(0,len(samples)):
            
            vals.append(self.calcSampleExprs(i_line, samples[i], norm = norm, log = False, countType = 'readcount'))
        
        ratio = np.log2((vals[0] + 1) / (vals[1] + 1)) if log else (vals[0] + 1) / (vals[1] + 1)
        
        return(ratio)
    
    
    def calcSampleKDE(self, npArray, min_, max_):
        
        from scipy.stats.kde import gaussian_kde
        
        kde = gaussian_kde(npArray)
        
        if min_ is None:
            
            min_ = np.trunc(npArray.min())
        
        if max_ is None:
            
            max_ = np.ceil(npArray.max())
        
        x = np.linspace(min_, max_,100)
        
        y = np.array([0]*100, dtype = float)
        
        for i in range(0,len(x)):
            
            y[i]=kde(x[i])[0]
        
        res = {'x' : x, 'y' : y}
        
        return(res)
    
    
    def sortTable(self, table, header, sortBy, deacreasing):
        
        if sortBy in self.annotHeader:
            
            if sortBy == 'Start' or sortBy == 'Stop':
                
                sortedIndex = np.array(table)[:,header.index(sortBy)].astype(int).argsort().tolist()
                
            else:
                
                sortedIndex = np.array(table)[:,header.index(sortBy)].astype(str).argsort().tolist()
            
        else:
            
            sortedIndex = np.array(table)[:,header.index(sortBy)].astype(float).argsort().tolist()
        
        if deacreasing:
            
            sortedIndex.reverse()
        
        sortedTable = []
        
        for index in sortedIndex:
            
            sortedTable.append(table[index])
        
        return(sortedTable)
    

    def getSciNot(self, val):
        
        res = val
        
        try:
            
            float(val)
            
            val_ = abs(val)
            
            if (val_ != float("inf")) and (val_ != 0):
                
                e = np.floor(np.log10(val_))
                
                res = ('-' if val < 0 else '') + str(np.round(val_/np.power(10,e), int(max(e+1, 2)))) + (('e' + str(int(e))) if (e != 0) else '')
            
        except:
            
            pass
        
        return(res)
    
    
    def getExprsTable(self, samples, norm, log, countType, sortBy, deacreasing, printHeader, printAnnot, scientific, json):
        
        exprsTable = []
        
        for i_line in range(0, len(self.countTable)):
            
            tmp = [self.calcSampleExprs(i_line, samples[i_sample], norm[i_sample], log[i_sample], countType) for i_sample in range(0, len(samples))]
            
            if scientific:
                
                tmp = [self.getSciNot(tmp_) for tmp_ in tmp]
            
            if printAnnot:
                
                tmp = self.annotTable[i_line] + tmp
            
            exprsTable.append(tmp)
        
        if sortBy is not None:
            
            exprsTable = self.sortTable(exprsTable, self.annotHeader + samples if printAnnot else samples, sortBy, deacreasing)
        
        if printHeader:
            
            header = [(('log2<br>' if log[i_sample] else '') + samples[i_sample] + '<br>' + countType + ('' if norm[i_sample] else ' (raw)')) for i_sample in range(0, len(samples))]
            
            if printAnnot:
                
                header = self.annotHeader + header
        
        if(json):
            
            toPrint = {0:','.join(map(str, header))} if printHeader else {}
            
            for i in range(0, len(exprsTable)):
                
                toPrint[i+int(printHeader)] = ','.join(map(str, exprsTable[i]))
        
        else:
            
            toPrint = [header] + exprsTable if printHeader else exprsTable
        
        return(toPrint)
    
    
    def getRatioTable(self, samplePairs, norm, log, sortBy, deacreasing, printHeader, printAnnot, scientific, json):
        
        ratioTable = []
        
        ratioTableHeader =  [(('log2<br>' if log[i] else '') + samplePairs[i][0] + (' (raw)' if norm[i] else '') + ' / ' + samplePairs[i][1] + (' (raw)' if norm[i] else '')) for i in range(0,1)]
        
        for i_line in range(0, len(self.countTable)):
            
            tmp = [self.calcRatio(i_line, samplePairs[i_pair][0], samplePairs[i_pair][1], norm[i_pair], log[i_pair]) for i_pair in range(0, len(samplePairs))]
            
            if scientific:
                
                tmp = [self.getSciNot(tmp_) for tmp_ in tmp]
            
            if printAnnot:
                
                tmp = self.annotTable[i_line] + tmp
                
                ratioTableHeader = self.annotHeader + ratioTableHeader
                
            ratioTable.append(tmp)
        
        if sortBy is not None:
            
            ratioTable = self.sortTable(ratioTable, ratioTableHeader, sortBy, deacreasing)
        
        if(json):
            
            toPrint = {0:','.join(map(str, header))} if printHeader else {}
            
            for i in range(0, len(exprsTable)):
                
                toPrint[i+int(printHeader)] = ','.join(map(str, ratioTable[i]))
        
        else:
            
            toPrint = [ratioTableHeader] + ratioTable if printHeader else ratioTable
        
        return(toPrint)
    
    
    def getScatterPlotData(self, sample1, sample2, norm, log, countType):
        
        norm = [norm] * 2
        
        log = [log] * 2
        
        exprsTable = self.getExprsTable(samples = [sample1, sample2], norm = norm, log = log, countType = countType, sortBy = None, deacreasing = None, printHeader = False, printAnnot = False, scientific = False, json = False)
        
        # data
        data = []
        
        npExprsTable = np.array(exprsTable)
        
        npAnnot = np.array(self.annotTable)
        
        is_finite = ((npExprsTable[:,0] != float('-inf')) * (npExprsTable[:,1] != float('-inf')))
        
        npExprsTable = npExprsTable[is_finite,:]
        
        npAnnot = npAnnot[is_finite,:]
        
        xlims = [min(npExprsTable[np.where(npExprsTable[:,0] != float('-inf'))[0],0]), max(npExprsTable[:,0])]
        
        ylims = [min(npExprsTable[np.where(npExprsTable[:,1] != float('-inf'))[0],1]), max(npExprsTable[:,1])]
        
        data.append({
            'x': [(xlims[0]-abs(xlims[0]*0.1)),(xlims[1]+abs(xlims[1]*0.1))], 
            'y': [(ylims[0]-abs(ylims[0]*0.1)),(ylims[1]+abs(ylims[1]*0.1))], 
            'mode' : 'lines',
            'showlegend' : False})
        
        types = self.types
        
        if types is None:
            
            types = np.unique(npAnnot[:,self.annotHeader.index('Type')])
            
        for type_ in types:
            
            index_type = np.where(npAnnot[:,self.annotHeader.index('Type')] == type_)[0]
            
            table_type = npExprsTable[index_type,:]
            
            data.append({
                'x': table_type[:,0].tolist(),
                'y': table_type[:,1].tolist(),
                'mode': 'markers',
                'type': 'scatter',
                'name': type_,
                'text': npAnnot[index_type,self.annotHeader.index('ID')].tolist(),
                'marker': { 'size': 8 },
                'hoverinfo' : "all"
                })
        
        # layout
        layout = {
            'xaxis':{
                'title': { 'text' : (('log2 ' if log[0] else '') + sample1 + ' ' + countType + ('' if norm[0] else ' (raw)')) }
                },
            'yaxis':{
                'title': { 'text' : (('log2 ' if log[1] else '') + sample2 + ' ' + countType + ('' if norm[1] else ' (raw)')) }
                },
            'hovermode' : 'closest',
            'margin': { 
                'l': 50,
                'r': 25,
                'b': 50,
                't': 25
                },
            'showlegend': True
            }
        
        return([data,layout])
    
    
    def getBoxplotData(self, plotType, samples, samplePairs, norm, log, countType, groupBy):
        
        if plotType == 'exprs':
            
            norm = [norm] * len(samples)
            
            log = [log] * len(samples)
            
            sampleNames = samples
            
            ytitle = (('log2 ' if log[0] else '') + countType + ('' if norm[0] else ' (raw)'))
            
            table = self.getExprsTable(samples, norm, log, countType, sortBy = None, deacreasing = None, printHeader = False, printAnnot = False, scientific = False, json = False)
            
        else:
            
            norm = [norm] * len(samplePairs)
        
            log = [log] * len(samplePairs)
            
            sampleNames = [samplePairs[i][0] + '/' + samplePairs[i][1] for i in range(0, len(samplePairs))]
            
            ytitle = (('log2 ' if log[0] else '') + ' ratio' + ('' if norm[0] else ' (raw)'))
            
            table = self.getRatioTable(samplePairs, norm, log, sortBy = None, deacreasing = None, printHeader = False, printAnnot = False, scientific = False, json = False)
        
        # data
        data = []
        
        npTable = np.array(table)
        
        npAnnot = np.array(self.annotTable)
        
        is_finite = np.array([True] * npTable.shape[0])
        
        for i in range(0, npTable.shape[1]):
            
            is_finite = is_finite * npTable[:,i] != float('-inf')
        
        npTable = npTable[is_finite,:]
        
        npAnnot = npAnnot[is_finite,:]
        
        types = self.types
        
        if types is None:
            
            types = np.unique(npAnnot[:,self.annotHeader.index('Type')])
        
        if groupBy == 'Samples':
            
            for type_ in types:
                
                x = y = []
                
                index_type = np.where(npAnnot[:,self.annotHeader.index('Type')] == type_)[0]
                
                for i_sample in range(0, npTable.shape[1]):
                    
                    y = y + npTable[index_type,i_sample].tolist()
                    
                    x = x + ([sampleNames[i_sample]]*len(index_type))
                    
                data.append({
                    'y' : y,
                    'x' : x,
                    'name' : type_,
                    'type' : 'box',
                    })
        
        if groupBy == 'Types':
            
            for i_sample in range(0, npTable.shape[1]):
                
                x = y = []
                
                for type_ in types:
                    
                    index_type = np.where(npAnnot[:,self.annotHeader.index('Type')] == type_)[0]
                    
                    y = y + npTable[index_type,i_sample].tolist()
                    
                    x = x + ([type_]*len(index_type))
                
                data.append({
                    'y' : y,
                    'x' : x,
                    'name' : sampleNames[i_sample],
                    'type' : 'box',
                    })
        
        layout = {
            'yaxis': {
                'title': ytitle
                },
            'boxmode': 'group',
            'margin': { 
                'l': 50,
                'r': 25,
                'b': 50,
                't': 25
                },
            'showlegend': True
            }
        
        return([data,layout])
    
    
    def getDensityPlotData(self, plotType, samples, samplePairs, norm, log, countType):
        
        if plotType == 'exprs':
            
            norm = [norm] * len(samples)
            
            log = [log] * len(samples)
            
            sampleNames = samples
            
            xtitle = (('log2 ' if log else '') + countType + ('' if norm else ' (raw)'))
            
            table = self.getExprsTable(samples = samples, norm = norm, log = log, countType = countType, sortBy = None, deacreasing = None, printHeader = False, printAnnot = False, scientific = False, json = False)
            
        else:
            
            norm = [norm] * len(samplePairs)
            
            log = [log] * len(samplePairs)
            
            sampleNames = [samplePairs[i][0] + '/' + samplePairs[i][1] for i in range(0, len(samplePairs))]
            
            xtitle = (('log2 ' if log[0] else '') + 'ratio' + ('' if norm[0] else ' (raw)'))
            
            table = self.getRatioTable(samplePairs, norm, log, sortBy = None, deacreasing = None, printHeader = False, printAnnot = False, scientific = False, json = False)
        
        # data
        data = []
        
        annotations = []
        
        npTable = np.array(table)
        
        npAnnot = np.array(self.annotTable)
        
        is_finite = np.array([True] * npTable.shape[0])
        
        for i in range(0, npTable.shape[1]):
            
            is_finite = is_finite * (npTable[:,i] != float('-inf'))
        
        npTable = npTable[is_finite,:]
        
        min_ = np.floor(npTable.min())
        
        max_ = np.ceil(npTable.max())
        
        npAnnot = npAnnot[is_finite,:]
        
        types = self.types
        
        if types is None:
            
            types = np.unique(npAnnot[:,self.annotHeader.index('Type')])
        
        lty = [["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"][i % 6] for i in range(0, npTable.shape[1])]
        
        col = get_N_HexCol(len(types))
        
        for i_sample in range(0, npTable.shape[1]):
            
            x = y = []
            
            for i_type in range(0, len(types)):
                
                type_ = types[i_type]
                
                index_type = np.where(npAnnot[:,self.annotHeader.index('Type')] == type_)[0]
                
                kde = self.calcSampleKDE(npTable[index_type,i_sample], min_, max_)
                
                x = kde['x'].tolist()
                
                y = kde['y'].tolist()
                
                mode = 'lines'
                
                if i_sample > 6:
                    
                    mode = 'lines+markers'
                
                data.append({
                    'y' : y,
                    'x' : x,
                    'name' : type_ + ' (' + sampleNames[i_sample] + ')',
                    'type' : 'scatter',
                    'mode' : mode,
                    'line': {
                        'dash': lty[i_sample],
                        'color': col[i_type]
                        },
                    'marker':{
                            'symbol' : (i_sample//6 - 1),
                            'maxdisplayed' : 30
                        }
                    })
        
        layout = {
            'xaxis':{
                'title': { 
                    'text' : xtitle 
                    }
                },
            'yaxis':{
                'title': { 
                    'text' : 'density' 
                    }
                },
            'margin': { 
                'l': 50,
                'r': 25,
                'b': 50,
                't': 25
                },
            'showlegend': True
            }
        
        return([data, layout])


def get_N_HexCol(N):
    
    import colorsys
    
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    
    hex_out = []
    
    for rgb in HSV_tuples:
        
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    
    return(hex_out)

def parseArgs():
    
    import sys
    
    args = sys.argv
    
    dictArgs = {}
    
    nameArg = None
    
    for arg in args:
        
        if arg[0:2] == "--":
            
            split = arg[2:].split("=")
            
            nameArg = str(split[0])
            
            if len(split) > 1:
                
                argVal = split[1]
                
            else:
                
                argVal = True
                
            dictArgs[nameArg] = argVal.strip("\'")
    
    return(dictArgs)
    
    
    
    
