# Preprocess the dataset
import os
import utm
import pandas as pd

def main():
    # Set up working directory
    os.chdir("/Users/ArcticPirates/Desktop/Passport Project/Code")
    
    # Import dataset as csv
    scooter_data = pd.read_csv('~/Desktop/Passport Project/Charlotte_Pilot_3PreMonths_SafeData_Sorted.csv')
    print("Original dataset size:", scooter_data.shape)
    
    # Drop the uncategorized zone
    scooter_data = scooter_data[scooter_data['zone_number'] != -1]
    print("Uncategorized zone dropped:", scooter_data.shape)

    # Drop 0 latitude, 0 longitude data
    scooter_data = scooter_data[scooter_data['latitude'] != 0]
    scooter_data = scooter_data[scooter_data['longitude'] != 0]
    print("Wrong lat/long data dropped:", scooter_data.shape)
    
    # Transfer the (latitude, longitude) to UTM data format
    scooter_data[['UTM_x', 'UTM_y']] = scooter_data.apply(lambda row: pd.Series(utm.from_latlon(row['latitude'], row['longitude'])[:2]), axis = 1)
    scooter_data.to_csv('scooter_data.csv', encoding='utf-8', index=False)
    print("CSV file saved as scooter_data.csv")

if __name__ == "__main__":
    main()