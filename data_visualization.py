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
    # Set up working directory
    os.chdir("/Users/ArcticPirates/Desktop/Passport Project/Code")

    # Import dataset as csv
    # scooter_data = pd.read_csv('~/Desktop/Passport Project/Code/scooter_data.csv')
    # n_original, p_original = scooter_data.shape
    # print("Original dataset size:", scooter_data.shape)

    # scooter_data = scooter_data.head(10000)
    # print("Taking the first 10000 rows", scooter_data.shape)

    # scooter_data['start_time'] = pd.to_datetime(scooter_data['start_time'], format = '%H:%M:%S').dt.time
    # scooter_data['end_time'] = pd.to_datetime(scooter_data['end_time'], format = '%H:%M:%S').dt.time

    # UTM_x_min = scooter_data['UTM_x'].min() - 1000
    # UTM_x_max = scooter_data['UTM_x'].max() + 1000
    # UTM_y_min = scooter_data['UTM_y'].min() - 5000
    # UTM_y_max = scooter_data['UTM_y'].max() + 5000

    # plot(scooter_data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max)

    # Note: the parking data needs further cleaning, perform on trip data first
    converted_data = pd.read_csv('~/Desktop/Passport Project/Code/converted_data.csv')
    print("Dataset imported. Original dataset size:", converted_data.shape)
    trip_data = converted_data[converted_data['event'] == 'trip']
    trip_data['start_time'] = pd.to_datetime(trip_data['start_time'], format = '%H:%M:%S').dt.time
    trip_data['end_time'] = pd.to_datetime(trip_data['end_time'], format = '%H:%M:%S').dt.time
    
    # where the trip started
    # UTM_x_min = trip_data['start_UTM_x'].min() - 500
    # UTM_x_max = trip_data['start_UTM_x'].max() + 500
    # UTM_y_min = trip_data['start_UTM_y'].min() - 1000
    # UTM_y_max = trip_data['start_UTM_y'].max() + 1000

    UTM_x_min = trip_data['start_UTM_x'].min() + 24000
    UTM_x_max = trip_data['start_UTM_x'].max() - 22000
    UTM_y_min = trip_data['start_UTM_y'].min() + 23000
    UTM_y_max = trip_data['start_UTM_y'].max() - 33000
    print("Start plotting the data...")
    plot_over_hours(trip_data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max)
    #plot_over_days(trip_data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max)
    print("Finished plotting the data.")


"""
Plot the distribution of scooters over time
Ignore the outliers since there’s only one or two of them and 
they are really far away from the city so it may be due to some
measurement error, we want to focus at the trips in downtown.
"""
def plot_over_hours(data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max):
    # parking data in the ith hour
    for i in range(3):
        df = data[(data['start_time'] >= dt.time(i,00,00)) & (data['start_time'] <= dt.time(i,59,59))]
        df = append_dummy(df, data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max)
        # df['start_UTM_x'], df['start_UTM_y'] = utils.rotate((0,0), (df['start_UTM_x'], df['start_UTM_y']), angle = math.radians(5))
        # print(df.start_zone.unique())
        fig, ax = plt.subplots(figsize=(20, 20))
        sns.scatterplot(x = "start_UTM_x", y = "start_UTM_y", data = df, hue = 'start_zone', style = 'Mobility_Provider', size = 100, legend = 'full')
        plt.axis([UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max], 'equal')
        plt.xticks(np.arange(UTM_x_min, UTM_x_max, 200), rotation = 90)
        plt.yticks(np.arange(UTM_y_min, UTM_y_max, 200))
        plt.grid(linestyle='-')
        plt.title('Trip start between ' + str(i) + ' and ' + str(i+1) + ' by areas')
        plt.savefig(f'Figs/trip_start_in_hour_{i}_trimmed.png')

# Plot the distribution of scooters over days within a certain time period
# This is just for clarifying the weekdays and weekends
def plot_over_days(data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max):
    for i in range(1, 11):
        # first 10 days
        df = data[data['Start_Day'] == i]
        for j in range(1):
            dff = df[(df['start_time'] >= dt.time(16+j,00,00)) & (df['start_time'] <= dt.time(16+j,59,59))]
            # by provider and zone
            fig, ax = plt.subplots(figsize=(20, 20))
            sns.scatterplot(x = "start_UTM_x", y = "start_UTM_y", data = df, hue = 'start_zone', style = 'Mobility_Provider', \
                size = 100, legend = 'brief')
            plt.axis([UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max], 'equal')
            plt.xticks(np.arange(UTM_x_min, UTM_x_max, 200), rotation = 90)
            plt.yticks(np.arange(UTM_y_min, UTM_y_max, 200))
            plt.grid(linestyle='-')
            plt.title('Trip start between ' + str(16+j) + ' and ' + str(17+j) + ' at day ' + str(i))
            plt.savefig(f'Figs/trip_start_hour_{j}_day_{i}.png')

# Add 3 x 4 dummy data points to correct the legend (tentative solution)
def append_dummy(selected_data, whole_data, UTM_x_min, UTM_x_max, UTM_y_min, UTM_y_max):
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
    selected_data = selected_data.append(dummy_list, ignore_index=True)
    return selected_data

if __name__ == "__main__":
    main()