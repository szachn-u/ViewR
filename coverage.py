# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 22:07:07 2019

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

###########
# classes #
###########

class Layout:

    def readGff(self, file, info = ["Name","Parent","gene","Alias","orf_classification","Ontology_term","Note","GO"]):
        tmp = np.genfromtxt(f, dtype = 'str', delimiter = "\t")
        coord = tmp[:,0:8]
        notes = tmp[:, 8]

        notes_ = ['']*len(notes)
        annot = ['']*(len(notes)+1)
        annot[0] = ["Chr", "Source", "Type", "Start", "Stop", "Score", "Strand", "Frame", "ID"] + info

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
        self.annot = annot
