from src.utils.timeutil import timeutil

def average_hours(data):
    hour_averages = []

    if len(data) == 0:
        return hour_averages

    sum, count, hour = _start_hour(data[0])

    for i in range(1, len(data)):
        record = data[i]
        time = timeutil.parse_db_time(record[0])

        if hour == time.hour:
            _sum(sum, record)
            count += 1
        else:
            average = _averages(sum, count)
            hour_averages.append(average)

            sum, count, hour = _start_hour(record)

    return hour_averages


def _start_hour(record):
    sum = _assign(record)
    hour = sum[0].hour
    count = 1
    return sum, count, hour


def _assign(values):
    time = timeutil.parse_db_time(values[0])
    time.replace(minute=0, second=0, microsecond=0)

    result = list(values)
    result[0] = time
    return result


def _sum(sums, list):
    for i in range(0, len(list)):
        if i == 0:
            pass # skip time
        else:
            sums[i] += list[i]


def _averages(sums, count):
    average = [None]*len(sums)
    for i in range(0, len(sums)):
        if i == 0:
            average[0] = sums[0]
        else:
            average[i] = sums[i] / count
    return average


