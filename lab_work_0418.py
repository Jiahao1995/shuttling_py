# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 10:14:11 2018

@author: lijia
"""

import numpy as np

def load_potentials():
    vrs = ['2.0E-1', '3.0E-1', '4.0E-1', '5.0E-1', '6.0E-1', '7.0E-1', '8.0E-1', \
           '9.0E-1', '1.0E0', '1.1E0', '1.2E0', '1.3E0', '1.4E0', '1.5E0', '1.6E0', \
           '1.7E0', '1.8E0', '1.9E0', '2.0E0']

    vlss = [['0', '0.04', '0.08', '0.12', '0.16', '0.2', '0.24', '0.28', '0.32', '0.36', '0.4'], \
            ['0.1', '0.14', '0.18', '0.22', '0.26', '0.3', '0.34', '0.38', '0.42', '0.46', '0.5'], \
            ['0.2', '0.24', '0.28', '0.32', '0.36', '0.4', '0.44', '0.48', '0.52', '0.56', '0.6'], \
            ['0.3', '0.34', '0.38', '0.42', '0.46', '0.5', '0.54', '0.58', '0.62', '0.66', '0.7'], \
            ['0.4', '0.44', '0.48', '0.52', '0.56', '0.6', '0.64', '0.68', '0.72', '0.76', '0.8'], \
            ['0.5', '0.54', '0.58', '0.62', '0.66', '0.7', '0.74', '0.78', '0.82', '0.86', '0.9'], \
            ['0.6', '0.64', '0.68', '0.72', '0.76', '0.8', '0.84', '0.88', '0.92', '0.96', '1.0'], \
            ['0.7', '0.74', '0.78', '0.82', '0.86', '0.9', '0.94', '0.98', '1.02', '1.06', '1.1'], \
            ['0.8', '0.84', '0.88', '0.92', '0.96', '1.0', '1.04', '1.08', '1.12', '1.16', '1.2'], \
            ['0.9', '0.94', '0.98', '1.02', '1.06', '1.1', '1.14', '1.18', '1.22', '1.26', '1.3'], \
            ['1.0', '1.04', '1.08', '1.12', '1.16', '1.2', '1.24', '1.28', '1.32', '1.36', '1.4'], \
            ['1.1', '1.14', '1.18', '1.22', '1.26', '1.3', '1.34', '1.38', '1.42', '1.46', '1.5'], \
            ['1.2', '1.24', '1.28', '1.32', '1.36', '1.4', '1.44', '1.48', '1.52', '1.56', '1.6'], \
            ['1.3', '1.34', '1.38', '1.42', '1.46', '1.5', '1.54', '1.58', '1.62', '1.66', '1.7'], \
            ['1.4', '1.44', '1.48', '1.52', '1.56', '1.6', '1.64', '1.68', '1.72', '1.76', '1.8'], \
            ['1.5', '1.54', '1.58', '1.62', '1.66', '1.7', '1.74', '1.78', '1.82', '1.86', '1.9'], \
            ['1.6', '1.64', '1.68', '1.72', '1.76', '1.8', '1.84', '1.88', '1.92', '1.96', '2.0'], \
            ['1.7', '1.74', '1.78', '1.82', '1.86', '1.9', '1.94', '1.98', '2.02', '2.06', '2.1'], \
            ['1.8', '1.84', '1.88', '1.92', '1.96', '2.0', '2.04', '2.08', '2.12', '2.16', '2.2']]
    
    gate_widths = ['40', '44', '48', '52', '56', '60']
    gate_separations = ['-10', '-8', '-6', '-4', '-2', '0']
    
    gate_separations1 = ['20', '24', '28', '32', '36' ,'40']
    
    coordinate_file = '\potential.coord'
    potential_file = '\potential.dat'
    general_file = '\potential.fld'    
    
    for gate_width in gate_widths:
        for gate_separation in gate_separations:
            gate_separation_index = gate_separations.index(gate_separation)
            for vr in vrs:
                vr_index = vrs.index(vr)
                for vl in vlss[vr_index]:
                    file_path = r'C:\Users\kswillic\Documents\nextnano\Output\0418' + \
                                '\P_V_R1_' + vr + '_V_L1_' + vl + '_GATE_WIDTH_X_' + \
                                gate_width + '_GATE_SEPARATION_' + gate_separation + '\output'
                                
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
    
                    potential_array = np.array(lines).reshape((num_x, num_y, num_z), order = 'C')
                    
                    y_idx = (np.abs(np.array(dim_y) - 0.0)).argmin()
                    
                    xz_slice_potential = potential_array[:, y_idx, :]
                    
                    potential_axis_array = np.zeros((num_z + 1, num_x+1))
                    potential_axis_array[0, 1:] = np.array(dim_x)
                    potential_axis_array[1:, 0] = np.array(dim_z)
                    potential_axis_array[1:, 1:] = xz_slice_potential
                    
                    file_name = gate_width + '_' + gate_separations1[gate_separation_index] + \
                                '_' + vr + '_' + vl + '.csv'
                                
                    np.savetxt(file_name, potential_axis_array, delimiter = '\t')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    


