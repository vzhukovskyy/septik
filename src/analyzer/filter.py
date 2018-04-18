class DataFilter:
    def __init__(self):
        self.K = {
            'cpu_temperature': 0.4,
            'outside_temperature': 0.01,
            'pressure': 0.01,
            'humidity': 0.01,
            'flow': 0.3,
            'level': 0.01
        }

    def reverse_filter_series(self, unfiltered_data_dict, starting_kalman):
        filtered_data_dict = {}
        final_kalman = {}

        for sensor in unfiltered_data_dict.iterkeys():
            if sensor == 'time':
                filtered_data_dict[sensor] = unfiltered_data_dict[sensor]
                continue

            unfiltered_data = unfiltered_data_dict[sensor]
            filtered_data = [None]*len(unfiltered_data)

            K = self.K[sensor]
            if starting_kalman:
                kalman = starting_kalman[sensor]
            else:
                kalman = unfiltered_data[0]

            for i in range(len(unfiltered_data)-1,-1,-1):
                kalman = K * unfiltered_data[i] + (1 - K) * kalman
                filtered_data[i] = kalman

            final_kalman[sensor] = kalman
            filtered_data_dict[sensor] = filtered_data

        return filtered_data_dict, final_kalman

    def filter_value(self, unfiltered_data_dict, starting_kalman_dict):
        filtered_data_dict = {}

        for sensor in unfiltered_data_dict.iterkeys():
            unfiltered_data = unfiltered_data_dict[sensor]
            if sensor == 'time':
                filtered_data_dict[sensor] = unfiltered_data
                continue

            K = self.K[sensor]
            if starting_kalman_dict:
                kalman = starting_kalman_dict[sensor]
            else:
                kalman = unfiltered_data

            kalman = K * unfiltered_data + (1 - K) * kalman

            filtered_data_dict[sensor] = kalman

        return filtered_data_dict


data_filter = DataFilter()
