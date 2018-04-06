# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 15:57:20 2018

@author: kswillic
"""

import numpy as np

def load_potentials(input_potentials):
    coordinate_file = '\potential.coord'
    potential_file = '\potential.dat'
    general_file = '\potential.fld'
    
    periods = ['\P1_V_C_', '\P2_V_L1_', '\P3_V_R1_', '\P4_V_C_']
    potentials = input_potentials
    
    for period in periods:
        if period != '\P1_V_C_':
            potentials.reverse()
        for potential in potentials:
            file_path = r'C:\Users\kswillic\Documents\nextnano\Output\3' + period + \
                        potential + 'E-1\output'
            
            with open(file_path + general_file) as fr:
                total = fr.readlines() 
                num_x = int(total[3][7:])
                num_y = int(total[4][7:])
                num_z = int(total[5][7:])
                    
            dims = []                   
            with open(file_path + coordinate_file) as fr:
                for dim in fr.readlines():
                    dim = dim.strip()
                    dims.append(float(dim))
            
            dim_x = dims[0 : num_x]
            dim_y = dims[num_x : num_x + num_y]
            dim_z = dims[num_x + num_y :]
        
            lines = []
            with open(file_path + potential_file) as fr:
                for line in fr.readlines():
                    line = line.strip()
                    lines.append(float(line))            
                            
            potential_array = np.array(lines).reshape((num_z, num_y, num_x),order = 'C')
    
            y_idx = (np.abs(np.array(dim_y)-0.0)).argmin()
            
            xz_slice_potential = potential_array[:,y_idx,:]
            
            potential_axis_array = np.zeros((num_z+1, num_x+1))
            potential_axis_array[0,1:] = np.array(dim_x)
            potential_axis_array[1:,0] = np.array(dim_z)
            potential_axis_array[1:,1:] = xz_slice_potential
                    
            file_name = period[1:4] + str(potentials.index(potential)) + '.csv'
                    
            np.savetxt(file_name, potential_axis_array, delimiter = '\t')
    