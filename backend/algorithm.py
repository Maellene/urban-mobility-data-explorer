def custom_sort_zones_by_trips(zone_trip_counts):
    """
    Custom insertion sort algorithm to rank zones by trip count.
    No use of built-in sort, sorted(), or any sorting library.

     Pseudo-code:
        FOR i FROM 1 TO length(data):
            current = data[i]
            j = i - 1
            WHILE j >= 0 AND data[j].trip_count < current.trip_count:
                data[j+1] = data[j]
                j = j - 1
            data[j+1] = current
        RETURN data
    
    Input: list of dictionaries with zone_name and trip_count
    Output: sorted list from highest to lowest trip count
    """
    data = zone_trip_counts[:]

    for i in range(1, len(data)):
        current = data[i]
        j = i - 1
        while j >= 0 and data[j]['trip_count'] < current['trip_count']:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = current

    return data


def custom_group_by_hour(trips):
    """
    Custom hash map implementation to group trips by hour.
    No use of Counter, groupby, or value_counts.
    
      Pseudo-code:
        hour_map = empty dictionary
        FOR each trip in trips:
            hour = extract hour from trip.pickup_datetime
            IF hour not in hour_map:
                hour_map[hour] = 0
            hour_map[hour] = hour_map[hour] + 1
        RETURN hour_map sorted by hour

    Input: list of trip dictionaries with pickup_datetime
    Output: dictionary of hour trip count
    """
    hour_map = {}

    for trip in trips:
        hour = int(trip['pickup_datetime'][11:13])
        if hour not in hour_map:
            hour_map[hour] = 0
        hour_map[hour] += 1

    return hour_map
