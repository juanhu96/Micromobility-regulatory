"""
Created on Jan, 2020
@author: Jingyuan Hu
"""

import os
import pandas as pd
import datetime as dt
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math
import utils

x_min = 510927
x_max = 518127
y_min = 3893570
y_max = 3900770
grid_size = 400

def main():
    os.chdir("/Users/ArcticPirates/Desktop/Passport Project/Code")
    filtered_data = pd.read_csv('~/Desktop/Passport Project/Data/filtered_data.csv')
    print("Filtered dataset imported.", filtered_data.shape)

    # NOTE: for constructing matrix, we focus on the trips that happen within these areas
    trimmed_data = filtered_data[(filtered_data['start_UTM_x'] >= x_min) & (filtered_data['start_UTM_x'] <= x_max) &\
         (filtered_data['start_UTM_y'] >= y_min) & (filtered_data['start_UTM_y'] <= y_max) &\
             (filtered_data['end_UTM_x'] >= x_min) & (filtered_data['end_UTM_x'] <= x_max) &\
                 (filtered_data['end_UTM_y'] >= y_min) & (filtered_data['end_UTM_y'] <= y_max)]
    trimmed_data.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'trimmed_data.csv', encoding='utf-8', index=False, header = True)
    print("Trimmed data obtained and saved.", trimmed_data.shape)
    # cell_zone_matrix = create_cell_matrix(trimmed_data, x_min, x_max, y_min, y_max, grid_size)
    # assign_feature(trimmed_data, cell_zone_matrix)


def create_cell_matrix(data, x_min, x_max, y_min, y_max, grid_size):
    
    """
    Get the zone each cell belongs to, return a 18*18 matrix that stores the information
    Assume the grid are square, and the range is divisible by the grid size
    x: [510927, 518127]
    y: [3893570, 3900770]
    cols = rows = 18
    324 cells, each cell is a 400*400 grid
    i, j = 0, 1, ..., 17
    """
    
    cols = int((x_max - x_min) / grid_size)
    rows = int((y_max - y_min) / grid_size)
    cell_zone_matrix = [[0 for i in range(rows)] for j in range(cols)]
    for i in range(rows):
        for j in range(cols):
            cell_y_min = y_min + i * grid_size
            cell_x_min = x_min + j * grid_size
            df_cell = data[(data['start_UTM_x'] >= cell_x_min) & \
                (data['start_UTM_x'] < (cell_x_min + grid_size)) & \
                    (data['start_UTM_y'] >= cell_y_min) & \
                        (data['start_UTM_y'] < (cell_y_min + grid_size))]
            if len(df_cell) == 0:
                cell_zone_matrix[i][j] = 0
            else:
                cell_zone_matrix[i][j] = df_cell['start_zone'].mode()[0]

    cell_zone_matrix = np.array(cell_zone_matrix)
    print("cell_zone_matrix created.")
    return cell_zone_matrix


def assign_feature(data, cell_zone_matrix):
    """
    Add extra columns/features which indicates:
    1. which time bucket the event is in
    2. which cell the event is in
    """

    data['start_cell'], data['end_cell'] = data.apply(get_cell_number, axis=1)
    pass

def get_cell_number(row):
    i_start = int((row['start_UTM_y'] - y_min) / grid_size)
    j_start = int((row['start_UTM_x'] - x_min) / grid_size)
    start_cell_number = i_start * 18 + j_start
    i_end = int((row['end_UTM_y'] - y_min) / grid_size)
    j_end = int((row['end_UTM_x'] - x_min) / grid_size)
    end_cell_number = i_end * 18 + j_end
    return start_cell_number, end_cell_number

def get_bucket(row):
    pass


if __name__ == "__main__":
    main()