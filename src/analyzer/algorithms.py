from src.utils.timeutil import timeutil


def calculate_average(data):
    if len(data) == 0:
        return data

    sums = _assign(data[0])
    for i in range(1, len(data)):
        _sum(sums, data[i])
    return _average(sums, len(data))


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


def _average(sums, count):
    average = [None]*len(sums)
    for i in range(0, len(sums)):
        if i == 0:
            # keep time
            average[0] = sums[0]
        else:
            average[i] = sums[i] / count
    return average


