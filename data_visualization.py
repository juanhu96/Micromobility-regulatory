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
import construct_matrix
from random import randint

def main():
    os.chdir("/Users/ArcticPirates/Desktop/Passport Project/Code")

    filtered_data = pd.read_csv('~/Desktop/Passport Project/Data/filtered_data.csv')
    trip_rebalance_total_over_days = pd.read_csv('~/Desktop/Passport Project/Data/trip_rebalance_total_over_days.csv')
    trip_rebalance_by_zone_over_days = pd.read_csv('~/Desktop/Passport Project/Data/trip_rebalance_by_zone_over_days.csv')
    inventory_by_hour = pd.read_csv('~/Desktop/Passport Project/Data/inventory_by_hour.csv')
    within_between_demand_zone = pd.read_csv('~/Desktop/Passport Project/Data/within_between_demand(zone_level).csv')
    within_between_demand_cell = pd.read_csv('~/Desktop/Passport Project/Data/within_between_demand(cell_level).csv')
    demand_cell_aggregated = pd.read_csv('~/Desktop/Passport Project/Data/demand_cell_aggregated.csv')
    trimmed_cell_bucket_data = pd.read_csv('~/Desktop/Passport Project/Data/trimmed_cell_bucket_data.csv')

    print("Dataset imported. Start plotting the data...")
    duration_dist_histogram(trimmed_cell_bucket_data)
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
    UTM_x_min = trip_data['start_UTM_x'].min() + 26000
    UTM_x_max = trip_data['start_UTM_x'].max() - 22000
    UTM_y_min = trip_data['start_UTM_y'].min() + 23000
    UTM_y_max = trip_data['start_UTM_y'].max() - 33000
        
    if plot_type == 'hours':
        fig, ax = plt.subplots(figsize=(20, 20))
        for i in range(24):
        # for i in range(1):
            df = event_data[(event_data['start_time'] >= dt.time(i,00,00)) & (event_data['start_time'] <= dt.time(i,59,59))]
            # df = event_data
            df = append_dummy(df, data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max)
            sns.scatterplot(x = "start_UTM_x", y = "start_UTM_y", data = df, hue = 'start_zone', style = 'Mobility_Provider', size = 100, legend = 'full')
            plt.axis([UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max], 'equal')
            plt.xticks(np.arange(UTM_x_min, UTM_x_max, 400), rotation = 90)
            plt.yticks(np.arange(UTM_y_min, UTM_y_max, 400))
            plt.grid(linestyle = '-')
            plt.title(event + ' between hour ' + str(i) + ' and hour ' + str(i+1), fontdict = {'fontsize' : 40})
            plt.savefig(f'../Figs/scatterplots/2d_scatterplot/{event}_in_hour_{i}_trimmed.png')
            # plt.title(event + ' aggregated over 24 hours and 90 days', fontdict = {'fontsize' : 40})
            # plt.savefig(f'../Figs/scatterplots/2d_scatterplot/{event}_trimmed.png')
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
                plt.savefig(f'../Figs/scatterplots/2d_scatterplot/trip_between_8_10_over_days/{event}_between_{8+j}_{10+j}_day_{i}.png')
                plt.cla()

    else:
        pass


def grid_histogram(data, event, unique = False, rotate = False):

    """
    2D histogram of counts of trips/scooter with grids (DOES NOT count the unique scooters)
    
    event: 'trip' or 'rebalance'
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
        plt.savefig(f'../Figs/2d_histogram/{event}_count_histogram_hour_{i}.png', dpi = 200)
        plt.cla()


def scooter_unique_boxplot(data, event = 'trip'):

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
    plt.savefig(f'../Figs/boxplots/average_scooter_boxplot/scooter_count_boxplot_total.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Average_duration', palette = 'Set1', data = avg_data)
    plt.title('Average time for each scooter over 24hrs', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/boxplots/average_scooter_boxplot/scooter_avg_duration_boxplot_total.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Average_line_dist', palette = 'Set1', data = avg_data)
    plt.title('Average straight line distance for each scooter over 24hrs', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/boxplots/average_scooter_boxplot/scooter_avg_line_dist_boxplot_total.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Trips', hue = "Zone_number", palette = 'Set1', data = avg_data)
    plt.title('Trips for each scooter over 24hrs (by zone)', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/boxplots/average_scooter_boxplot/scooter_count_boxplot_by_zone.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Average_duration', hue = "Zone_number", palette = 'Set1', data = avg_data)
    plt.title('Average time for each scooter over 24hrs (by zone)', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/boxplots/average_scooter_boxplot/scooter_avg_duration_boxplot_by_zone.png')
    plt.cla()

    sns.boxplot(x = 'Time_period', y = 'Average_line_dist', hue = "Zone_number", palette = 'Set1', data = avg_data)
    plt.title('Average straight line distance for each scooter over 24hrs (by zone)', fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/boxplots/average_scooter_boxplot/scooter_avg_line_dist_boxplot_by_zone.png')
    plt.cla()


def trip_rebalance_boxplot_over_hours(trip_rebalance_data, event, day_type):
    
    """
    Boxplot of the number of trip/rebanacing events over 24 hours 
    (each hour has 90 points, corresponding to 90 days)
    event: trip/take away/put back (we handle inventory separately)
    day_type: weekday/weekend
    within zone/between zone vs. all 4*4 combinations
    """

    df = trip_rebalance_data[(trip_rebalance_data['event'] == event) & (trip_rebalance_data['Day_type'] == day_type)]
    fig, ax = plt.subplots(figsize=(20, 20))
    
    sns.boxplot(x = 'Hour', y = 'count', palette = 'Set1', data = df)
    plt.title('Total '+ event + ' over ' + day_type, fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/boxplots/{event}_boxplot_over_24hours/{event}_total_over_{day_type}.png')
    plt.cla()

    # for start_zone in trip_rebalance_data['start_zone'].unique():
    #     for end_zone in trip_rebalance_data['end_zone'].unique():
    #         dff = df[(df['start_zone'] == start_zone) & (df['end_zone'] == end_zone)]
    #         sns.boxplot(x = 'Hour', y = 'count', palette = 'Set1', data = dff)
    #         plt.title(event + ' from zone ' + str(start_zone) + ' to zone '+ str(end_zone) + ' over ' + day_type, fontdict = {'fontsize' : 30})
    #         plt.savefig(f'../Figs/boxplot/{event}_boxplot_over_24hours/{event}_from_{start_zone}_to_{end_zone}_over_{day_type}.png')
    #         plt.cla()


def trip_rebalance_lineplot_over_days(trip_rebalance_data, event, day_type):
    
    """
    Lineplot of total trip/rebalance events over 90 days 
    (each day is aggregated and has one point)
    event: trip/take away/put back (we handle inventory separately)
    day_type: weekday/weekend
    within zone/between zone vs. all 4*4 combinations
    """

    df = trip_rebalance_data[(trip_rebalance_data['event'] == event) & (trip_rebalance_data['Day_type'] == day_type)]
    fig, ax = plt.subplots(figsize=(20, 20))
    
    # sns.lineplot(x = 'Day', y = 'count', hue = 'Hour', data = df)
    # plt.title(event + ' over 90 days', fontdict = {'fontsize' : 30})
    # plt.savefig(f'../Figs/lineplot/{event}_lineplot_over_days/{event}_total_over_90days.png')
    # plt.cla()

    for hour in range(0, 24):
            df_hour = df[df['Hour'] == hour]
            sns.lineplot(x = 'Day', y = 'count', data = df_hour)
            plt.title(event + ' over ' + day_type + ' at hour ' + str(hour), fontdict = {'fontsize' : 30})
            plt.savefig(f'../Figs/lineplots/{event}_lineplot_over_{day_type}/{event}_total_over_{day_type}_hour{hour}.png')
            plt.cla()

            sns.scatterplot(x = "Day", y = "count", data = df_hour)
            plt.title(event + ' over ' + day_type + ' at hour ' + str(hour), fontdict = {'fontsize' : 30})
            plt.savefig(f'../Figs/scatterplots/{event}_lineplot_over_{day_type}/{event}_total_over_{day_type}_hour{hour}.png')
            plt.cla()


def inventory_boxplot_over_hours(inventory_data, day_type):

    """
    Boxplot for inventory data over 24hours for weekend/weekday separately
    """

    df = inventory_data[inventory_data['Day_type'] == day_type]
    fig, ax = plt.subplots(figsize=(20, 20))
    
    sns.boxplot(x = 'Hour', y = 'Inventory', palette = 'Set1', data = df)
    plt.title('Inventory level over 24 hour on ' + day_type, fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/boxplots/inventory_boxplot_over_24hours/inventory_level_over_{day_type}.png')
    plt.cla()


def duration_dist_histogram(data):
    
    """
    Histogram and boxplot of duration/distance of each trips
    Per zone/time bucket
    """

    df = data[(data['event'] == 'trip') & (data['Day_type'] == 'weekday')]
    fig, ax = plt.subplots(figsize=(20, 20))

    for zone in range(1, 4):
        df_zone = data[data['start_zone'] == zone]
        for bucket in range(1, 4):
            df_bucket = df_zone[df_zone['start_bucket'] == bucket]
            sns.distplot(df_bucket['duration'], bins=30, hist_kws={"range": [0,100]}, kde = False, norm_hist = False)
            plt.title('Histogram of trip duration at zone ' + str(zone) + ' and time bucket ' + str(bucket), fontdict = {'fontsize' : 20})
            plt.savefig(f'../Figs/histogram/duration/duration_histogram_zone{zone}_bucket{bucket}.png')
            plt.cla()
            sns.distplot(df_bucket['line_dist'], bins=30, kde = False, norm_hist = False)
            plt.title('Histogram of trip distance at zone ' + str(zone) + ' and time bucket ' + str(bucket), fontdict = {'fontsize' : 20})
            plt.savefig(f'../Figs/histogram/distance/distance_histogram_zone{zone}_bucket{bucket}.png')
            plt.cla()
    

def inventory_lineplot_over_days(inventory_data, drop = False):

    """
    Lineplot for inventory data over all inventory days for weekend/weekday separately
    """

    # df = inventory_data[inventory_data['Day_type'] == day_type]
    fig, ax = plt.subplots(figsize=(20, 20))

    if drop == False:
        sns.lineplot(x = 'Day', y = 'Inventory', hue = 'Hour', data = inventory_data)
        plt.title('Inventory level over 90 days', fontdict = {'fontsize' : 30})
        plt.savefig(f'../Figs/lineplots/inventory_lineplot_over_days/original/inventory_level_over_90days.png')
        plt.cla()

        for hour in range(0, 24):
            df_hour = inventory_data[inventory_data['Hour'] == hour]
            sns.lineplot(x = 'Day', y = 'Inventory', data = inventory_data)
            plt.title('Inventory level over 90 days at hour ' + str(hour), fontdict = {'fontsize' : 30})
            plt.savefig(f'../Figs/lineplots/inventory_lineplot_over_days/original/inventory_level_over_90days_hour{hour}.png')
            plt.cla()
    else:
        df = inventory_data.drop(inventory_data[(inventory_data['Day'] == 1) | (inventory_data['Day'] == 31) | (inventory_data['Day'] == 62)].index)
        sns.lineplot(x = 'Day', y = 'Inventory', hue = 'Hour', data = df)
        plt.title('Inventory level over 90 days (day 1,31,62 dropped)', fontdict = {'fontsize' : 30})
        plt.savefig(f'../Figs/lineplots/inventory_lineplot_over_days/dropped/inventory_level_over_90days_dropped.png')
        plt.cla()

        for hour in range(0, 24):
            df_hour = df[df['Hour'] == hour]
            sns.lineplot(x = 'Day', y = 'Inventory', data = df_hour)
            plt.title('Inventory level over 90 days at hour ' + str(hour) + ' (day 1,31,62 dropped)', fontdict = {'fontsize' : 30})
            plt.savefig(f'../Figs/lineplots/inventory_lineplot_over_days/dropped/inventory_level_over_90days_hour{hour}_dropped.png')
            plt.cla()


def demand_scatterplot_over_days(demand_data, level = 'zone'):

    """
    Plot the number of trips happen between/within zone + between/within bucket for all these zones and buckets
    """

    df = demand_data[demand_data['Day_type'] == 'weekday']
    fig, ax = plt.subplots(figsize=(20, 20))

    if level == 'zone':
        for zone in df['Zone'].unique():
            for bucket in df['Time_bucket'].unique():
                dff = df[(df['Zone'] == zone) & (df['Time_bucket'] == bucket)]
                ax = dff.plot(kind = 'scatter', x = 'Day', y = 'within_zone_within_bucket', label = 'within_zone_within_bucket', color = 'r')    
                dff.plot(kind = 'scatter', x = 'Day', y = 'between_zone_within_bucket', label = 'between_zone_within_bucket', color = 'g', ax = ax)    
                dff.plot(kind = 'scatter', x = 'Day', y = 'within_zone_between_bucket', label = 'within_zone_between_bucket', color = 'b', ax = ax)
                dff.plot(kind = 'scatter', x = 'Day', y = 'between_zone_between_bucket', label = 'between_zone_between_bucket', color = 'orange', ax = ax)
                plt.title('Demand at zone ' + str(zone) + ' time bucket ' + str(bucket), fontdict = {'fontsize' : 10})
                ax.set_xlabel("Day")
                ax.set_ylabel("Count")
                plt.savefig(f'../Figs/demand(zone_level)/zone_{zone}_bucket_{bucket}.png')
                plt.cla()

    elif level == 'cell': # 324 cells * 3 bucket
        cells = [randint(0, 324) for p in range (10)]
        for cell in cells:
            zone = df[df['Cell'] == cell]['Zone'].values[0]
            for bucket in df['Time_bucket'].unique():
                    dff = df[(df['Cell'] == cell) & (df['Time_bucket'] == bucket)]
                    ax = dff.plot(kind = 'scatter', x = 'Day', y = 'within_cell_within_bucket', label = 'within_cell_within_bucket', color = 'r')    
                    dff.plot(kind = 'scatter', x = 'Day', y = 'between_cell_within_bucket', label = 'between_cell_within_bucket', color = 'g', ax = ax)    
                    dff.plot(kind = 'scatter', x = 'Day', y = 'within_cell_between_bucket', label = 'within_cell_between_bucket', color = 'b', ax = ax)
                    dff.plot(kind = 'scatter', x = 'Day', y = 'between_cell_between_bucket', label = 'between_cell_between_bucket', color = 'orange', ax = ax)
                    plt.title('Demand at cell ' + str(cell) + ' (zone ' + str(zone) + ') time bucket ' + str(bucket), fontdict = {'fontsize' : 10})
                    ax.set_xlabel("Day")
                    ax.set_ylabel("Count")
                    plt.savefig(f'../Figs/demand(cell_level)/cell_{cell}_bucket_{bucket}.png')
                    plt.cla()
    
    # for each bucket compute the aggregated between/within ...
    elif level == 'cell_aggregate':
        for bucket in df['Time_bucket'].unique():
            dff = df[df['Time_bucket'] == bucket]
            ax = dff.plot(kind = 'scatter', x = 'Day', y = 'within_cell_within_bucket', label = 'within_cell_within_bucket', color = 'r')
            dff.plot(kind = 'scatter', x = 'Day', y = 'between_cell_within_bucket', label = 'between_cell_within_bucket', color = 'g', ax = ax)    
            dff.plot(kind = 'scatter', x = 'Day', y = 'within_cell_between_bucket', label = 'within_cell_between_bucket', color = 'b', ax = ax)
            dff.plot(kind = 'scatter', x = 'Day', y = 'between_cell_between_bucket', label = 'between_cell_between_bucket', color = 'orange', ax = ax)
            plt.title('Demand at time bucket ' + str(bucket), fontdict = {'fontsize' : 10})
            ax.set_xlabel("Day")
            ax.set_ylabel("Count")
            plt.savefig(f'../Figs/demand(cell_aggregated)/bucket_{bucket}.png')
            plt.cla()


def scooter_lineplot_by_company(data):

    """
    Plot the amount of scooters each company deployed over 90 days
    """

    scooter_data = construct_matrix.compute_scooter_company(data[data['Day_type'] == 'weekday'])
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.lineplot(x = 'Day', y = 'Count', data = scooter_data, hue = 'Mobility_Provider', legend = 'full')
    plt.title("Scooters deployed over 90 days by company", fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/scooters_deployed_over_weekdays_by_company(lineplot).png')
    plt.cla()
    sns.scatterplot(x = "Day", y = "Count", data = scooter_data, hue = 'Mobility_Provider', legend = 'full')
    plt.title("Scooters deployed over 90 days by company", fontdict = {'fontsize' : 30})
    plt.savefig(f'../Figs/scooters_deployed_over_weekdays_by_company(scatterplot).png')
    plt.cla()


def count_avg(event_data):

    """
    Create a new dataframe that stores the information for each scooter in each period
    Time period, Total trips, Average duration, Average straight line distance, Provider, Zone

    NOTE: 
    This is for the average boxplot, 
    and the trips used here are the total number of trips served in that hour
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