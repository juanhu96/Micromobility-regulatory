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

    # filtered_data = pd.read_csv('~/Desktop/Passport Project/Data/filtered_data.csv')
    # print("Filtered dataset imported.", filtered_data.shape)

    # NOTE: for constructing matrix, we focus on the trips that happen within these areas

    # trimmed_data = filtered_data[(filtered_data['start_UTM_x'] >= x_min) & (filtered_data['start_UTM_x'] <= x_max) &\
    #      (filtered_data['start_UTM_y'] >= y_min) & (filtered_data['start_UTM_y'] <= y_max) &\
    #          (filtered_data['end_UTM_x'] >= x_min) & (filtered_data['end_UTM_x'] <= x_max) &\
    #              (filtered_data['end_UTM_y'] >= y_min) & (filtered_data['end_UTM_y'] <= y_max)]
    # trimmed_data.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'trimmed_data.csv',\
    #     encoding='utf-8', index=False, header = True)
    # print("Trimmed data obtained: ", trimmed_data.shape, "Start assigning cell number and time bucket...")
    
    # trimmed_data = pd.read_csv('~/Desktop/Passport Project/Data/trimmed_data.csv')
    # cell_zone_matrix = create_cell_matrix(trimmed_data, x_min, x_max, y_min, y_max, grid_size)
    # np.save('cell_zone_matrix.npy', cell_zone_matrix)
    # trimmed_cell_bucket_data = assign_feature(trimmed_data, cell_zone_matrix)
    # trimmed_cell_bucket_data.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'trimmed_cell_bucket_data.csv',\
    #     encoding='utf-8', index=False, header = True)
    # print("Trimmed data with cell and bucket information saved as trimmed_cell_bucket_data.csv")

    # trimmed_cell_bucket_data = pd.read_csv('~/Desktop/Passport Project/Data/trimmed_cell_bucket_data.csv')
    # cell_zone_matrix = np.load('cell_zone_matrix.npy')
    # print(trimmed_cell_bucket_data['end_inventory_day'].min() + 1, trimmed_cell_bucket_data['end_inventory_day'].max() + 1)
    # trip_od_matrix(trimmed_cell_bucket_data[trimmed_cell_bucket_data['event'] == 'trip'])
    # rebalance_od_matrix(trimmed_cell_bucket_data[trimmed_cell_bucket_data['event'] == 'rebalance'])
    # inventory_table(trimmed_cell_bucket_data)

    # within_between_demand(trimmed_cell_bucket_data, level = 'cell')
    # within_between_demand_cell = pd.read_csv('~/Desktop/Passport Project/Data/within_between_demand(cell_level).csv')
    # compute_demand_cell_aggregated(within_between_demand_cell)
    



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

    data['start_bucket'] = data.apply(get_start_bucket, axis=1)
    data['end_bucket'] = data.apply(get_end_bucket, axis=1)
    data['start_cell'] = data.apply(get_start_cell_number, axis=1)
    data['start_cell_zone'] = data.apply(get_start_cell_zone, axis=1, args = (cell_zone_matrix, ))
    data['end_cell'] = data.apply(get_end_cell_number, axis=1)
    data['end_cell_zone'] = data.apply(get_end_cell_zone, axis=1, args = (cell_zone_matrix, ))
    return data


def trip_od_matrix(trip_data):

    """
    OD in and OD out for each time bucket
    OD in gives infomation on where the scooter are from
    OD out gives information on where the scooter goes to
    E.g. (bucket 1, cell 1) --> (bucket 2, cell 2)
    OD_out_bucket1[1][2]++
    OD_in_bucket2[2][1]++
    Because during bucket 1, the scooter is not at cell 2 yet
    out[i][j]: trip from i to j
    in[i][j]: trip to i from j
    """

    rows = 18
    cols = 18
    cells = rows * cols
    dummy_cell = cells
    # trip out
    for day in range(1,92):
        df_day = trip_data[trip_data['Start_Day'] == day]
        for bucket in range(0, 5):
            df_same_bucket = df_day[(df_day['start_bucket'] == bucket) & (df_day['end_bucket'] == bucket)]
            df_start_bucket = df_day[(df_day['start_bucket'] == bucket) & (df_day['end_bucket'] != bucket)]
            df_end_bucket = df_day[(df_day['start_bucket'] != bucket) & (df_day['end_bucket'] == bucket)]
            # NOTE: dummy cell for cross bucket event
            od_matrix = [[0 for i in range(cells+1)] for j in range(cells+1)]

            # within the bucket
            for start_cell in df_same_bucket['start_cell'].unique():
                df_start_cell_same_bucket = df_same_bucket[df_same_bucket['start_cell'] == start_cell]
                for end_cell in df_start_cell_same_bucket['end_cell'].unique():
                    od_matrix[start_cell][end_cell] = len(df_start_cell_same_bucket[df_start_cell_same_bucket['end_cell'] == end_cell])
            
            # start from the bucket
            for start_cell in df_start_bucket['start_cell'].unique():
                od_matrix[start_cell][dummy_cell] = len(df_start_bucket[df_start_bucket['start_cell'] == start_cell])

            # end at the bucket
            for end_cell in df_end_bucket['end_cell'].unique():
                od_matrix[dummy_cell][end_cell] = len(df_end_bucket[df_end_bucket['end_cell'] == end_cell])

            np.save(r'/Users/ArcticPirates/Desktop/Passport Project/OD_matrix/trip/np_array/' +\
                'trip_matrix_' + 'day' + str(day) + '_' + 'bucket' + str(bucket) + '.npy', np.array(od_matrix))

            np.savetxt(r'/Users/ArcticPirates/Desktop/Passport Project/OD_matrix/trip/csv/' +\
                'trip_matrix_' + 'day' + str(day) + '_' + 'bucket' + str(bucket) + '.csv', od_matrix, fmt="%d", delimiter=",")
            
    print("trip matrix finished")

    # trip out
    # for day in range(1,3):
    #     df_day = trip_data[trip_data['Start_Day'] == day]
    #     for bucket in range(1, 4):
    #         df_bucket = df_day[df_day['start_bucket'] == bucket]
    #         od_matrix = [[0 for i in range(cells)] for j in range(cells)]
    #         for start_cell in df_bucket['start_cell'].unique():
    #             df_start_cell = df_bucket[df_bucket['start_cell'] == start_cell]
    #             for end_cell in df_start_cell['end_cell'].unique():
    #                 od_matrix[start_cell][end_cell] = len(df_start_cell[df_start_cell['end_cell'] == end_cell])
    #         np.save(r'/Users/ArcticPirates/Desktop/Passport Project/OD_matrix/trip_out/' +\
    #             'trip_out_matrix_' + 'day' + str(day) + '_' + 'bucket' + str(bucket) + '.npy', np.array(od_matrix))
    #         np.savetxt(r'/Users/ArcticPirates/Desktop/Passport Project/OD_matrix/trip_out/' +\
    #             'trip_out_matrix_' + 'day' + str(day) + '_' + 'bucket' + str(bucket) + '.csv', od_matrix, fmt="%d", delimiter=",")
    # print("trip out matrix finished")
    
    # trip in
    # for day in range(1,3):
    #     df_day = trip_data[trip_data['End_Day'] == day]
    #     for bucket in range(1, 4):
    #         df_bucket = df_day[df_day['end_bucket'] == bucket]
    #         od_matrix = [[0 for i in range(cells)] for j in range(cells)]
    #         for end_cell in df_bucket['end_cell'].unique():
    #             df_end_cell = df_bucket[df_bucket['end_cell'] == end_cell]
    #             for start_cell in df_end_cell['start_cell'].unique():
    #                 od_matrix[end_cell][start_cell] = len(df_end_cell[df_end_cell['start_cell'] == start_cell])
    #         np.save(r'/Users/ArcticPirates/Desktop/Passport Project/OD_matrix/trip_in/' +\
    #             'trip_in_matrix_' + 'day' + str(day) + '_' + 'bucket' + str(bucket) + '.npy', np.array(od_matrix))
    #         np.savetxt(r'/Users/ArcticPirates/Desktop/Passport Project/OD_matrix/trip_in/'+\
    #             'trip_in_matrix_' + 'day' + str(day) + '_' + 'bucket' + str(bucket) + '.csv', od_matrix, fmt="%d", delimiter=",")
    # print("trip in matrix finished")


def rebalance_od_matrix(rebalance_data):
    rows = 18
    cols = 18
    cells = rows * cols
    dummy_cell = cells
    # trip out
    for day in range(1,92):
        df_day = rebalance_data[rebalance_data['Start_Day'] == day]
        for bucket in range(0, 5):
            df_same_bucket = df_day[(df_day['start_bucket'] == bucket) & (df_day['end_bucket'] == bucket)]
            df_start_bucket = df_day[(df_day['start_bucket'] == bucket) & (df_day['end_bucket'] != bucket)]
            df_end_bucket = df_day[(df_day['start_bucket'] != bucket) & (df_day['end_bucket'] == bucket)]
            # NOTE: dummy cell for cross bucket event
            od_matrix = [[0 for i in range(cells+1)] for j in range(cells+1)]

            # within the bucket
            for start_cell in df_same_bucket['start_cell'].unique():
                df_start_cell_same_bucket = df_same_bucket[df_same_bucket['start_cell'] == start_cell]
                for end_cell in df_start_cell_same_bucket['end_cell'].unique():
                    od_matrix[start_cell][end_cell] = len(df_start_cell_same_bucket[df_start_cell_same_bucket['end_cell'] == end_cell])
            
            # start from the bucket
            for start_cell in df_start_bucket['start_cell'].unique():
                od_matrix[start_cell][dummy_cell] = len(df_start_bucket[df_start_bucket['start_cell'] == start_cell])

            # end at the bucket
            for end_cell in df_end_bucket['end_cell'].unique():
                od_matrix[dummy_cell][end_cell] = len(df_end_bucket[df_end_bucket['end_cell'] == end_cell])

            np.save(r'/Users/ArcticPirates/Desktop/Passport Project/OD_matrix/rebalance/np_array/' +\
                'rebalance_matrix_' + 'day' + str(day) + '_' + 'bucket' + str(bucket) + '.npy', np.array(od_matrix))
            
            np.savetxt(r'/Users/ArcticPirates/Desktop/Passport Project/OD_matrix/rebalance/csv/' +\
                'rebalance_matrix_' + 'day' + str(day) + '_' + 'bucket' + str(bucket) + '.csv', od_matrix, fmt="%d", delimiter=",")

    print("rebalance matrix finished")


def inventory_table(data):

    """
    Compute the inventory at the start of each bucket in each grid based on the base inventory level
    May over count the inventory if a scooter showed up in multiple cells
    But this would still be a good approximation since our base inventory level was computed at 6
    At when there haven't been much trips and other events yet
    NOTE: all service_start_implicit starts at 5:59:59 and ends at 6:00:00

    90 days * 5 bucket * 324 cells
    """

    rows = 18
    cols = 18
    cells = rows * cols

    inventory_day_bucket_list = []
    # inventory day from 1 to 91
    # inventory day at 0: 0-6am of the first day, ignore this part
    for day in range(data['end_inventory_day'].min() + 1, data['end_inventory_day'].max() + 1):
        df_day = data[data['end_inventory_day'] == day]
        day_type = df_day['end_inventory_day_type'].values[0]
        for cell in range(cells):
            df_cell = df_day[(df_day['start_cell'] == cell) | (df_day['end_cell'] == cell)]
            df_cell_base = df_cell[(df_cell['event'] == 'service_start_implicit') | \
                    (((df_cell['event'] == 'trip') | (df_cell['event'] == 'low_battery')) & \
                        (df_cell['start_time_hour'] <= 6) & (df_cell['end_time_hour'] >= 6))]
            # inventory level at 6 (bucket 0)
            total_inventory = len(df_cell_base['Scooter_ID'].unique())
            inventory_day_bucket_list.append({"Inventory_day": day, "Day_type": day_type, "Bucket": 0, "Cell": cell, "Inventory": total_inventory})

            for bucket in range(1, 5): 
                # to compute the inventory at the start of the ith bucket, we want the rebalance event in (i-1)th bucket
                # max{inventory, 0} to avoid negative entries, since approximation
                inventory_added = len(df_cell[(df_cell['event'] == 'rebalance') & (df_cell['end_bucket'] == (bucket - 1))])
                inventory_removed = len(df_cell[(df_cell['event'] == 'rebalance') & (df_cell['start_bucket'] == (bucket - 1))])
                total_inventory = total_inventory + inventory_added - inventory_removed
                inventory_day_bucket_list.append({"Inventory_day": day, "Day_type": day_type, "Bucket": bucket, "Cell": cell, "Inventory": max(total_inventory, 0)})
    
    inventory_day_bucket = pd.DataFrame(inventory_day_bucket_list)
    inventory_day_bucket.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'inventory_day_bucket.csv', encoding='utf-8', index=False, header = True, \
        columns = ["Inventory_day", "Day_type", "Bucket", "Cell", "Inventory"])
    print("Inventory_day_bucket data saved.")


def within_between_demand(data, level = 'zone'):
    """
    Compute the within/between demand at the given level for each time bucket
    NOTE:
    Since we're considering demand, we consider the start zones/cells
    level: zone, cell
    """

    within_between_demand_list = []

    if level == 'zone':
        for day in data['Start_Day'].unique():
            df_day = data[data['Start_Day'] == day]
            day_type = df_day['Day_type'].values[0]
            for zone in df_day['start_zone'].unique():
                df_zone = df_day[df_day['start_zone'] == zone]
                for bucket in range(1, 4): # we don't care about bucket 0, 4
                    df_bucket = df_zone[df_zone['start_bucket'] == bucket]

                    within_zone_within_bucket = len(df_bucket[(df_bucket['end_zone'] == zone) & (df_bucket['end_bucket'] == bucket)])
                    between_zone_within_bucket = len(df_bucket[(df_bucket['end_zone'] != zone) & (df_bucket['end_bucket'] == bucket)])
                    within_zone_between_bucket = len(df_bucket[(df_bucket['end_zone'] == zone) & (df_bucket['end_bucket'] != bucket)])
                    between_zone_between_bucket = len(df_bucket[(df_bucket['end_zone'] != zone) & (df_bucket['end_bucket'] != bucket)])

                    within_between_demand_list.append({"Day": day, "Day_type": day_type, "Time_bucket": bucket, "Zone": zone, \
                        "within_zone_within_bucket": within_zone_within_bucket, "between_zone_within_bucket": between_zone_within_bucket, \
                            "within_zone_between_bucket": within_zone_between_bucket, "between_zone_between_bucket": between_zone_between_bucket})

        within_between_demand = pd.DataFrame(within_between_demand_list)
        within_between_demand.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'within_between_demand.csv', encoding='utf-8', index=False, header = True, \
            columns = ["Day", "Day_type", "Time_bucket", "Zone", "within_zone_within_bucket", "between_zone_within_bucket", "within_zone_between_bucket", "between_zone_between_bucket"])
        print("within_between_demand data for zone level saved.")

    elif level == 'cell':
        for day in data['Start_Day'].unique():
            df_day = data[data['Start_Day'] == day]
            day_type = df_day['Day_type'].values[0]
            for cell in df_day['start_cell'].unique():
                df_cell = df_day[df_day['start_cell'] == cell]
                zone = df_cell['start_cell_zone'].values[0]
                for bucket in range(1, 4): # we don't care about bucket 0, 4
                    df_bucket = df_cell[df_cell['start_bucket'] == bucket]

                    within_cell_within_bucket = len(df_bucket[(df_bucket['end_cell'] == cell) & (df_bucket['end_bucket'] == bucket)])
                    between_cell_within_bucket = len(df_bucket[(df_bucket['end_cell'] != cell) & (df_bucket['end_bucket'] == bucket)])
                    within_cell_between_bucket = len(df_bucket[(df_bucket['end_cell'] == cell) & (df_bucket['end_bucket'] != bucket)])
                    between_cell_between_bucket = len(df_bucket[(df_bucket['end_cell'] != cell) & (df_bucket['end_bucket'] != bucket)])

                    within_between_demand_list.append({"Day": day, "Day_type": day_type, "Time_bucket": bucket, "Cell": cell, "Zone": zone, \
                        "within_cell_within_bucket": within_cell_within_bucket, "between_cell_within_bucket": between_cell_within_bucket, \
                            "within_cell_between_bucket": within_cell_between_bucket, "between_cell_between_bucket": between_cell_between_bucket})

        within_between_demand = pd.DataFrame(within_between_demand_list)
        within_between_demand.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'within_between_demand(cell_level).csv', encoding='utf-8', index=False, header = True, \
            columns = ["Day", "Day_type", "Time_bucket", "Cell", "Zone", "within_cell_within_bucket", "between_cell_within_bucket", "within_cell_between_bucket", "between_cell_between_bucket"])
        print("within_between_demand data for cell level saved.")


def compute_demand_cell_aggregated(data):

    """
    Compute the aggregated demand between/within time bucket
    from the within_between_demand(cell_level).csv
    """

    demand_cell_aggregated_list = []

    for day in data['Day'].unique():
        df_day = data[data['Day'] == day]
        day_type = df_day['Day_type'].values[0]
        for bucket in range(1, 4):
            df_bucket = df_day[df_day['Time_bucket'] == bucket]
            within_cell_within_bucket = df_bucket['within_cell_within_bucket'].sum()
            between_cell_within_bucket = df_bucket['between_cell_within_bucket'].sum()
            within_cell_between_bucket = df_bucket['within_cell_between_bucket'].sum()
            between_cell_between_bucket = df_bucket['between_cell_between_bucket'].sum()
            demand_cell_aggregated_list.append({"Day": day, "Day_type": day_type, "Time_bucket": bucket, \
                        "within_cell_within_bucket": within_cell_within_bucket, "between_cell_within_bucket": between_cell_within_bucket, \
                            "within_cell_between_bucket": within_cell_between_bucket, "between_cell_between_bucket": between_cell_between_bucket})
    
    demand_cell_aggregated = pd.DataFrame(demand_cell_aggregated_list)
    demand_cell_aggregated.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'demand_cell_aggregated.csv', encoding='utf-8', index=False, header = True, \
            columns = ["Day", "Day_type", "Time_bucket", "within_cell_within_bucket", "between_cell_within_bucket", "within_cell_between_bucket", "between_cell_between_bucket"])


def compute_scooter_company(data):

    """
    Compute the number of scooters each company deployed over 90 days
    """

    scooter_company_list = []
    for day in data['Start_Day'].unique():
        df_day = data[data['Start_Day'] == day]
        for company in df_day['Mobility_Provider'].unique():
            scooter_company_list.append({"Day": day, "Mobility_Provider": company, "Count": len(df_day[df_day['Mobility_Provider'] == company]['Scooter_ID'].unique())})
    scooter_company = pd.DataFrame(scooter_company_list)
    # scooter_company.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'scooter_company.csv', encoding='utf-8', index=False, header = True, \
    #     columns = ["Day", "Mobility_Provider", "Count"])
    return scooter_company



def get_start_cell_number(row):
    i_start = int((row['start_UTM_y'] - y_min) / grid_size)
    j_start = int((row['start_UTM_x'] - x_min) / grid_size)
    return i_start * 18 + j_start

   
def get_start_cell_zone(row, cell_zone_matrix):
    i_start = int((row['start_UTM_y'] - y_min) / grid_size)
    j_start = int((row['start_UTM_x'] - x_min) / grid_size)
    return cell_zone_matrix[i_start][j_start]


def get_end_cell_number(row):
    i_end = int((row['end_UTM_y'] - y_min) / grid_size)
    j_end = int((row['end_UTM_x'] - x_min) / grid_size)
    return i_end * 18 + j_end


def get_end_cell_zone(row, cell_zone_matrix):
    i_end = int((row['end_UTM_y'] - y_min) / grid_size)
    j_end = int((row['end_UTM_x'] - x_min) / grid_size)
    return cell_zone_matrix[i_end][j_end]


def get_start_bucket(row):

    """
    Bucket: 0, 1, 2, 3, 4
    0: 4:00:00 - 8:59:59
    1: 9:00:00 - 13:59:59
    2: 14:00:00 - 18:59:59
    3: 19:00:00 - 23:59:59
    4: 0:00:00 - 3:59:59
    """

    start_time_hour = row['start_time_hour']
    if start_time_hour >= 9 and start_time_hour < 14:
        start_bucket = 1
    elif start_time_hour >= 14 and start_time_hour < 19:
        start_bucket = 2
    elif start_time_hour >= 19 and start_time_hour < 24:
        start_bucket = 3
    elif start_time_hour >= 4 and start_time_hour < 9:
        start_bucket = 0
    else: # 0<= hour < 4
        start_bucket = 4

    return start_bucket


def get_end_bucket(row):

    """
    Bucket: 0, 1, 2, 3, 4
    0: 4:00:00 - 8:59:59
    1: 9:00:00 - 13:59:59
    2: 14:00:00 - 18:59:59
    3: 19:00:00 - 23:59:59
    4: 0:00:00 - 3:59:59
    """

    end_time_hour = row['end_time_hour']
    if end_time_hour >= 9 and end_time_hour < 14:
        end_bucket = 1
    elif end_time_hour >= 14 and end_time_hour < 19:
        end_bucket = 2
    elif end_time_hour >= 19 and end_time_hour < 24:
        end_bucket = 3
    elif end_time_hour >= 4 and end_time_hour < 9:
        end_bucket = 0
    else: # 0<= hour < 4
        end_bucket = 4
    
    return end_bucket


if __name__ == "__main__":
    main()