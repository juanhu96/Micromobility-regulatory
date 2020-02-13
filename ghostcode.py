"""
This stores a list of command/code I used for calling the functions and making the plots
"""

def data_visualization():
    # scooter_unique_boxplot(filtered_data)
    # grid_scatterplot(filtered_data, event = 'trip', plot_type = 'hours')
    # grid_scatterplot(filtered_data, event = 'trip', plot_type = 'days')
    # grid_scatterplot(filtered_data, event = 'rebalance', plot_type = 'hours')

    # for event_type in filtered_data['event'].unique():
    #     grid_histogram(filtered_data, event = event_type)

    # event_data = filtered_data[filtered_data['event'] == 'trip']
    # avg_data = count_avg(event_data)

    # for event in trip_rebalance_total_over_days['event'].unique():
    #     for day_type in trip_rebalance_total_over_days['Day_type'].unique():
    #         trip_rebalance_boxplot_over_hours(trip_rebalance_total_over_days, event, day_type)
    #         trip_rebalance_lineplot_over_days(trip_rebalance_total_over_days, event, day_type)

    # for day_type in inventory_by_hour['Day_type'].unique():
    #     inventory_boxplot_over_hours(inventory_by_hour, day_type)


    # inventory_lineplot_over_days(inventory_by_hour, True)

    # df_list = []
    # for day in range(1, 92):
    #     for company in range(1, 4):
    #         dff = filtered_data[(filtered_data['Start_Day'] == day) & (filtered_data['Mobility_Provider'] == company)]
    #         scooter_count = len(dff['Scooter_ID'].unique())
    #         trip_count = len(dff[dff['event'] == 'trip'])
    #         rebalance_count = len(dff[dff['event'] == 'rebalance'])
    #         df_list.append({"Day": day, "Day_type": dff['Day_type'].values[0], "Company": company, "scooter_count": scooter_count,\
    #             "trip_count": trip_count, "rebalance_count": rebalance_count})
    # df = pd.DataFrame(df_list)
    # df.to_csv(r'/Users/ArcticPirates/Desktop/Passport Project/Data/'+'event_count_by_day.csv', encoding='utf-8', index=False, header = True, \
    #     columns = ["Day", "Day_type", "Company", "scooter_count", "trip_count", "rebalance_count"])
    # print("csv file saved") 
    
    # fig, ax = plt.subplots(figsize=(20, 20))
    # sns.lineplot(x = 'Day', y = 'trip_count', data = df)
    # plt.title('Trip count over 90 days', fontdict = {'fontsize' : 30})
    # plt.savefig(f'../Figs/lineplot/trip_count_over_90days.png')
    # plt.cla()

    # sns.lineplot(x = 'Day', y = 'trip_count', data = df)
    # plt.title('Rebalance count over 90 days', fontdict = {'fontsize' : 30})
    # plt.savefig(f'../Figs/lineplot/rebalance_count_over_90days.png')
    # plt.cla()

    # sns.lineplot(x = 'Day', y = 'trip_count', data = df)
    # plt.title('Service count over 90 days', fontdict = {'fontsize' : 30})
    # plt.savefig(f'../Figs/lineplot/service_count_over_90days.png')
    # plt.cla()

    # demand_scatterplot_over_days(within_between_demand_zone)
    # demand_scatterplot_over_days(demand_cell_aggregated, level = 'cell_aggregate')

    # scooter_lineplot_by_company(filtered_data)

    # duration_dist_histogram(trimmed_cell_bucket_data)


def construct_matrix():
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