from src.utils.timeutil import timeutil


def calculate_average(data):
    if len(data) == 0:
        return data

    averages = _assign(data[0])
    for d in data:
        _sum(averages, d)
    return _averages(averages, len(data))


def _start_hour(record):
    sum = _assign(record)
    hour = sum[0].hour
    count = 1
    return sum, count, hour


def _assign(values):
    time = timeutil.parse_db_time(values[0])
    time = time.replace(minute=30, second=0, microsecond=0)

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


