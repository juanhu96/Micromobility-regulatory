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

def main():
    os.chdir("/Users/ArcticPirates/Desktop/Passport Project/Code")
    converted_data = pd.read_csv('~/Desktop/Passport Project/Data/converted_data.csv')
    print("Dataset imported. Original dataset size:", converted_data.shape)

    # converted_data['start_time_hour'] = pd.to_datetime(converted_data['start_time'], format = '%H:%M:%S').dt.hour
    converted_data['start_time'] = pd.to_datetime(converted_data['start_time'], format = '%H:%M:%S').dt.time
    converted_data['end_time'] = pd.to_datetime(converted_data['end_time'], format = '%H:%M:%S').dt.time
    
    # filtered_data = filter_data(converted_data, 'trip')
    # filtered_data = filter_data(converted_data, 'rebalance')
    # print("Data filtered, the size is now:", filtered_data.shape)
    print("Start plotting the data...")
    # event_boxplot(filtered_data)
    # grid_scatterplot(filtered_data, event = 'trip', plot_type = 'hours')
    grid_scatterplot(filtered_data, event = 'trip', plot_type = 'days')
    # grid_scatterplot(filtered_data, event = 'rebalance', plot_type = 'hours')
    # grid_histogram(filtered_data, event = 'trip', plot_type = 'trip')
    # grid_histogram(filtered_data, event = 'rebalance', plot_type = 'trip')
    print("Finished plotting the data.")


def grid_scatterplot(data, event, plot_type, unique = False, rotate = False):

    """
    Scatterplot of scooters over time/days with grids

    UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max: the boundary of the plot
    event: 'trip' or 'rebalance'
    plot_type: 'hours' or 'days'
    unique: 'True' or 'False', whether to count unique scooters or all trips
    rotate: 'True' or 'False', whether to rotate the coordinates for plot, set to 'False' as default
    """

    event_data = data[data['event'] == event]
    trip_data = data[data['event'] == 'trip']
    UTM_x_min = trip_data['start_UTM_x'].min() + 24000
    UTM_x_max = trip_data['start_UTM_x'].max() - 22000
    UTM_y_min = trip_data['start_UTM_y'].min() + 23000
    UTM_y_max = trip_data['start_UTM_y'].max() - 33000

    # TODO: subject to changes
    if rotate == True:
        event_data['start_UTM_x'], event_data['start_UTM_y'] = utils.rotate((0,0), (event_data['start_UTM_x'], event_data['start_UTM_y']), angle = math.radians(5))
        
    if plot_type == 'hours':
        fig, ax = plt.subplots(figsize=(20, 20))
        for i in range(24):
            df = event_data[(event_data['start_time'] >= dt.time(i,00,00)) & (event_data['start_time'] <= dt.time(i,59,59))]
            # TODO: if unique == True:
            df = append_dummy(df, data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max)
            plt.rcParams['savefig.dpi'] = 200
            plt.rcParams['figure.dpi'] = 200
            sns.scatterplot(x = "start_UTM_x", y = "start_UTM_y", data = df, hue = 'start_zone', style = 'Mobility_Provider', size = 100, legend = 'full')
            plt.axis([UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max], 'equal')
            plt.xticks(np.arange(UTM_x_min, UTM_x_max, 200), rotation = 90)
            plt.yticks(np.arange(UTM_y_min, UTM_y_max, 200))
            plt.grid(linestyle = '-')
            plt.title(event + ' between hour ' + str(i) + ' and hour ' + str(i+1), fontdict = {'fontsize' : 40})
            plt.savefig(f'../Figs/{event}_in_hour_{i}_trimmed.png', dpi = 200)
            plt.cla()
    
    elif plot_type == 'days':
        fig, ax = plt.subplots(figsize=(20, 20))
        for i in range(1, 31): # days
            df = event_data[event_data['Start_Day'] == i]
            for j in range(1): # hours
                dff = df[(df['start_time'] >= dt.time(8+j,00,00)) & (df['start_time'] <= dt.time(10+j,59,59))]
                dff = append_dummy(dff, data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max)
                # plt.rcParams['savefig.dpi'] = 200
                # plt.rcParams['figure.dpi'] = 200
                sns.scatterplot(x = "start_UTM_x", y = "start_UTM_y", data = dff, hue = 'start_zone', style = 'Mobility_Provider', \
                    size = 100, legend = 'full')
                plt.axis([UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max], 'equal')
                plt.xticks(np.arange(UTM_x_min, UTM_x_max, 200), rotation = 90)
                plt.yticks(np.arange(UTM_y_min, UTM_y_max, 200))
                plt.grid(linestyle = '-')
                plt.title(event + ' between hour ' + str(8+j) + ' and hour ' + str(10+j) + ' at day ' + str(i), fontdict = {'fontsize' : 40})
                # plt.savefig(f'../Figs/trip_plots_over_days/{event}_between_{9+j}_{10+j}_day_{i}.png', dpi = 200)
                plt.savefig(f'../Figs/trip_between_8_10_over_days/{event}_between_{8+j}_{10+j}_day_{i}.png')
                plt.cla()

    else:
        pass


def grid_histogram(data, event, plot_type, unique = False, rotate = False):

    """
    2D histogram of counts of trips/scooter with grids
    
    event: 'trip' or 'rebalance'
    plot_type: 'hours' or 'days'
    TODO: unique: 'True' or 'False', whether to count unique scooters or all trips
    rotate: 'True' or 'False', whether to rotate the coordinates for plot, set to 'False' as default
    """

    event_data = data[data['event'] == event]
    trip_data = data[data['event'] == 'trip']
    UTM_x_min = trip_data['start_UTM_x'].min() + 24000
    UTM_x_max = trip_data['start_UTM_x'].max() - 22000
    UTM_y_min = trip_data['start_UTM_y'].min() + 23000
    UTM_y_max = trip_data['start_UTM_y'].max() - 33000

    fig, ax = plt.subplots(figsize = (40, 40))
    for i in range(24):
        df = event_data[(event_data['start_time'] >= dt.time(i,00,00)) & (event_data['start_time'] <= dt.time(i,59,59))]
        x_edges = np.arange(UTM_x_min, UTM_x_max, 200)
        y_edges = np.arange(UTM_y_min, UTM_y_max, 200)
        H, x_edges, y_edges = np.histogram2d(x = df['start_UTM_x'].tolist(), \
            y = df['start_UTM_y'].tolist(), bins = (x_edges, y_edges))
        H = H.T 

        """
        NOTE:
        H is a ndarray of shape(nx, ny), we transpose it to let 
        each row list bins with common y range
        TODO: count the unique scooters in each grids (how to compute this without manually for loop)

        Another way is to use pcolormesh to display actual edges
        X, Y = np.meshgrid(x_edges, y_edges)
        ax.pcolormesh(X,Y,H, cmap='RdBu')
        """

        plt.rcParams['savefig.dpi'] = 200
        plt.rcParams['figure.dpi'] = 200
        plt.axis([UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max], 'equal')
        plt.xticks(np.arange(UTM_x_min, UTM_x_max, 200), rotation = 90)
        plt.yticks(np.arange(UTM_y_min, UTM_y_max, 200))
        plt.grid(linestyle = '-')
        plt.imshow(H, interpolation = 'nearest', origin = 'low', extent = [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]])
        for (a, b), z in np.ndenumerate(H):
            ax.text(x_edges[b] + 100, y_edges[a] + 100, z, ha = 'center', va = 'center', fontsize = 12)
        # cbar = plt.colorbar()
        # cbar.ax.set_ylabel('Counts')
        plt.title(event + ' count histogram between ' + str(i) + ' and ' + str(i+1), fontdict = {'fontsize' : 40})
        plt.savefig(f'../Figs/{event}_count_histogram_hour_{i}.png', dpi = 200)
        plt.cla()


def event_boxplot(data, event = 'trip'):
    """
    Boxplot for the average time/distance of the event group by the time
    NOTE: For first time handling dataset, call count_avg() for data transformation

    event: 'trip' or 'rebalance'
    """
    
    # event_data = data[data['event'] == event]
    # avg_data = count_avg(event_data)
    avg_data = pd.read_csv('~/Desktop/Passport Project/Data/scooter_count_data.csv')

    fig, ax = plt.subplots(figsize=(20, 20))

    sns.boxplot(x = 'Time_period', y = 'Trips', palette = 'Set1', data = avg_data)
    plt.title('Trips for each scooter over 24hrs', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/average_scooter_boxplot/scooter_count_boxplot_total.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Average_duration', palette = 'Set1', data = avg_data)
    plt.title('Average time for each scooter over 24hrs', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/average_scooter_boxplot/scooter_avg_duration_boxplot_total.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Average_line_dist', palette = 'Set1', data = avg_data)
    plt.title('Average straight line distance for each scooter over 24hrs', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/average_scooter_boxplot/scooter_avg_line_dist_boxplot_total.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Trips', hue = "Zone_number", palette = 'Set1', data = avg_data)
    plt.title('Trips for each scooter over 24hrs (by zone)', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/average_scooter_boxplot/scooter_count_boxplot_by_zone.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Average_duration', hue = "Zone_number", palette = 'Set1', data = avg_data)
    plt.title('Average time for each scooter over 24hrs (by zone)', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/average_scooter_boxplot/scooter_avg_duration_boxplot_by_zone.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Average_line_dist', hue = "Zone_number", palette = 'Set1', data = avg_data)
    plt.title('Average straight line distance for each scooter over 24hrs (by zone)', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/average_scooter_boxplot/scooter_avg_line_dist_boxplot_by_zone.png')
    plt.cla()

    



def count_avg(event_data):

    """
    Create a new dataframe that stores the information for each scooter in each period

    Time period, Total trips, Average duration, Average straight line distance, Provider, Zone
    """

    count_data_list = []
    for i in range(24):
        df = event_data[event_data['start_time_hour'] == i]
        # scooters used in that area, for each of them compute how many trips they served
        for scooter in df['Scooter_ID'].unique():
            trips = len(df[df['Scooter_ID'] == scooter])
            provider = df[df['Scooter_ID'] == scooter].iloc[0]['Mobility_Provider']
            zone = df[df['Scooter_ID'] == scooter].iloc[0]['start_zone']
            avg_duration = df[df['Scooter_ID'] == scooter]['duration'].mean()
            avg_line_dist = df[df['Scooter_ID'] == scooter]['line_dist'].mean()
            scooter_event = {"Scooter_ID": scooter, "Time_period": i, "Trips": trips, \
                "Average_duration": avg_duration, "Average_line_dist": avg_line_dist,\
                    "Mobility_Provider": provider, "Zone_number": zone}
            count_data_list.append(scooter_event)
    count_data = pd.DataFrame(count_data_list)
    count_data.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'scooter_count_data.csv', encoding='utf-8', index=False, header = True, \
        columns = ["Scooter_ID", "Time_period", "Trips", "Average_duration", "Average_line_dist", "Mobility_Provider", "Zone_number"])
    print("File saved as scooter_count_data.csv")
    return count_data


def append_dummy(selected_data, whole_data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max):

    """
    Add 3 x 4 dummy data points to correct the legend (tentative solution)
    TODO: add to the boundary instead of the central
    """
    
    dummy_list = []
    x = (UTM_x_min + UTM_x_max) / 2
    y = (UTM_y_min + UTM_y_max) / 2
    for i in whole_data.start_zone.unique():
        for j in whole_data.Mobility_Provider.unique():
            event = {"start_time": 0, "end_time": 0, "Start_Day": 0, "End_Day": 0, \
            "start_zone": i, "end_zone": i, "start_UTM_x": x, "start_UTM_y": y, \
            "end_UTM_x": x, "end_UTM_y": y, "start_lat": 0, "start_long": 0, \
                "end_lat": 0, "end_long": 0, "line_dist": 0, "duration": 0, \
                    "Mobility_Provider": j, "Scooter_ID": 0, "event": "trip"}  
            dummy_list.append(event) 
    selected_data = selected_data.append(dummy_list, ignore_index = True)
    return selected_data


if __name__ == "__main__":
    main()