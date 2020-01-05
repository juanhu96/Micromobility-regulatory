import os
import pandas as pd
import datetime as dt
from datetime import datetime, date
import matplotlib.pyplot as plt
import utils

def main():
    # Set up working directory
    os.chdir("/Users/ArcticPirates/Desktop/Passport Project/Code")

    # Import dataset as csv
    scooter_data = pd.read_csv('~/Desktop/Passport Project/Code/scooter_data.csv')
    print("Original dataset imported, size:", scooter_data.shape)

    # Data preprocessing (for starting/ending time)
    scooter_data['start_time'] = pd.to_datetime(scooter_data['start_time'], format = '%H:%M:%S').dt.time
    scooter_data['end_time'] = pd.to_datetime(scooter_data['end_time'], format = '%H:%M:%S').dt.time
    # scooter_data = scooter_data[(scooter_data['start_time'] >= dt.time(6,00,00)) & (scooter_data['start_time'] <= dt.time(21,00,00))]
    # scooter_data = scooter_data[(scooter_data['end_time'] >= dt.time(6,00,00)) & (scooter_data['end_time'] <= dt.time(21,00,00))]
    # print("Non-operating hours events dropped:", scooter_data.shape)

    # convert into trips and maintenance/rebalance events
    event_data = convert_data(scooter_data)
    # filtered_data = filter_data(event_data)

    
def convert_data(scooter_data):
    print("Start converting the data...")
    event_data_list = []
    for index, row in scooter_data.iterrows():
        """
        - consider the normal events only for now
        - ignore the first event
        - look for the same scooter
        """
        if (row['event_type_reason'] == 'trip_end' or row['event_type_reason'] == 'low_battery' or \
            row['event_type_reason'] == 'service_start' or row['event_type_reason'] == 'rebalance_drop_off' or \
                row['event_type_reason'] == 'maintenance_drop_off') and \
            index > 0 and row['Scooter_ID'] == scooter_data.iloc[[index - 1]]['Scooter_ID'].values[0]:

            if row['event_type_reason'] == 'trip_end':
                event_type = 'trip'
            elif row['event_type_reason'] == 'low_battery':
                event_type = 'low_battery'
            else:
                event_type = 'rebalance/maintenance'

            previous_event = scooter_data.iloc[[index - 1]]
            # NOTE: for zone/provider we convert to string to make it categorical
            event_start_day = previous_event['End_Day'].values[0]
            event_start_time = previous_event['end_time'].values[0]
            event_start_zone = str(previous_event['zone_number'].values[0])
            event_start_UTM_x = previous_event['UTM_x'].values[0]
            event_start_UTM_y = previous_event['UTM_y'].values[0]
            event_start_lat = previous_event['latitude'].values[0]
            event_start_long = previous_event['longitude'].values[0]

            event_end_day = row['Start_Day']
            event_end_time = row['start_time']
            event_end_zone = str(row['zone_number'])
            event_end_UTM_x = row['UTM_x']
            event_end_UTM_y = row['UTM_y']
            event_end_lat = row['latitude']
            event_end_long = row['longitude']
            
            # NOTE: this works even if the start and end time are not on the same day
            # event_end_time = dt.time(0,10,00)
            # event_start_time = dt.time(23,50,00)
            event_duration = round((datetime.combine(date.min, event_end_time) - \
                 datetime.combine(date.min, event_start_time)).seconds/60, 2)
            # distance rounded as integers
            line_dist = utils.distance_cartesian(event_start_UTM_x, event_start_UTM_y, event_end_UTM_x, event_end_UTM_y)
            provider = str(row['Mobility_Provider'])
            scooter_id = row['Scooter_ID']

            # same format as park data
            # NOTE: later on we will add the route distance
            event = {"start_time": event_start_time, "end_time": event_end_time, \
                "Start_Day": event_start_day, "End_Day": event_end_day, \
                    "start_zone": event_start_zone, "end_zone": event_end_zone, \
                        "start_UTM_x": event_start_UTM_x, "start_UTM_y": event_start_UTM_y, \
                            "end_UTM_x": event_end_UTM_x, "end_UTM_y": event_end_UTM_y, \
                                "start_lat": event_start_lat, "start_long": event_start_long, \
                                    "end_lat": event_end_lat, "end_long": event_end_long, \
                                        "line_dist": line_dist, \
                                        "duration": event_duration, "Mobility_Provider": provider, \
                                            "Scooter_ID": scooter_id, "event": event_type}
            event_data_list.append(event)
        
    print("All events converted.")
    # NOTE: This is way faster than appending to a data frame row by row directly
    event_data = pd.DataFrame(event_data_list)
    event_data.to_csv('converted_data.csv', encoding='utf-8', index=False, header = True, \
        columns = ["start_time", "end_time", "Start_Day", "End_Day", "start_zone", "end_zone", \
        "start_UTM_x", "start_UTM_y", "end_UTM_x", "end_UTM_y", "start_lat", "start_long", "end_lat", \
            "end_long", "line_dist", "duration", "Mobility_Provider", "Scooter_ID", "event"])
    print("File saved as converted_data.csv")
    return event_data


def filter_data(event_data):
    """
    For trip/low battery/rebalance events:
    - drop trips w/ duration < 1min or > ?hr
    - drop the ones w/ straight line distance < ?m
    """
    # event_data = event_data[(event_data['duration'] < 1 and event_data['duration'] > 1 and event_data['event'] == 'trip')]
    pass

if __name__ == "__main__":
    main()