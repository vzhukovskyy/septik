import sys, os, datetime, time, math, calendar
import numpy
import plotly
import plotly.graph_objs as go
from log_parser import extract_pillars_from_logs

line_styles = { 
    'mem by second': dict(color = ('#D62728')), 
    'cpu by second': dict(color = ('#1F77B4')),
    'cpu by minute': dict(color = ('#FF7F0E')),
    'cpu by hour': dict(color = ('#258D6B'))
}

def get_line_style(id):
    return line_styles[id]

def parse_date(date):
    return datetime.datetime.strptime(date, '"%Y-%m-%d %H:%M:%S"')

def read(filename):
    dates = []
    seconds = []
    cpus = []
    mems = []
    with open(filename, 'r') as f:
        try:
            f.readline() # skip titles
            second = 0
            while True:
                line = f.readline()
                date, cpu, mem = line.split(',')
                try:
                    date = parse_date(date)
                except:
                    print 'error'
                dates.append(date)
                seconds.append(second)
                second += 1
                cpus.append(float(cpu))
                mems.append(float(mem))
        except:
            pass
    return dates, seconds, cpus, mems

def aggregate(aggregation_seconds, dates, values):
    if aggregation_seconds == 1:
        return dates, values

    agg_dates = []
    agg_values = []
    for agg_i in range(0, len(dates)/aggregation_seconds):
        sum = 0
        for i in range(0, aggregation_seconds):
            sum += values[agg_i*aggregation_seconds+i]
        avg = sum / aggregation_seconds
        middle_date_in_range = agg_i*aggregation_seconds+aggregation_seconds/2
        #print last_date_in_range_index,'of',len(dates)

        agg_dates.append(middle_date_in_range)
        agg_values.append(avg)
    return agg_dates, agg_values

def build_chart_data(filename):
    dates, seconds, cpus, mems = read(filename)
    seconds_for_minutes, cpu_by_minutes = aggregate(60, seconds, cpus)
    seconds_for_hours, cpu_by_hours = aggregate(3600, seconds, cpus)

    chart_data = [('cpu by second', seconds, cpus),
                  ('mem by second', seconds, mems),
                  ('cpu by minute', seconds_for_minutes, cpu_by_minutes),
                  ('cpu by hour', seconds_for_hours, cpu_by_hours)]
    return chart_data

def build_title(filename, chart_data):
    seconds = chart_data[0][1]
    cpus = chart_data[0][2]
    mems = chart_data[1][2]

    # time can change on the box during run so rely on number of seconds
    duration = datetime.timedelta(seconds=len(seconds))
    cpus_numpy = numpy.array(cpus)
    cpu_average = round(cpus_numpy.mean(), 2)
    mems_numpy = numpy.array(mems)
    mem_average = round(mems_numpy.mean(), 2)

    title = filename+': CPU avg: '+str(cpu_average)+'%, RAM avg: '+str(mem_average)+'%, duration: '+str(duration)
    return title

def build_traces(chart_data):
    traces = []
    for element in chart_data:
        trace = go.Scatter(
            name = element[0],
            x = element[1],
            y = element[2],
            line = get_line_style(element[0])
        )
        traces.append(trace)
    return traces

def map_pillars(filename, pillars):
    dates, seconds, cpus, mems = read(filename)
    mapped_pillars = []

    index = 1
    for pillar in pillars:
        pillar_date = pillar[0]
        #print 'Pillar date',pillar_date
        while index < len(dates):
            prev_date = dates[index-1]
            date = dates[index]
            #print 'Prev date',prev_date,'date',date
            
            if prev_date <= pillar_date and pillar_date < date:
                print 'Pillar date',pillar_date,'is between',prev_date,'and',date,'=',index
                break
            index += 1
        
        pillar = (seconds[index], pillar[1], pillar[2])
        mapped_pillars.append(pillar)

    return mapped_pillars

def get_average_hourly_cpu(chart_data, second_start, second_end):
    hourly_cpu = chart_data[3][2]
    seconds_for_hourly_cpu = chart_data[3][1]

    for i in range(0, len(seconds_for_hourly_cpu)):
        hour = seconds_for_hourly_cpu[i]
        if hour >= second_start:
            return hourly_cpu[i]
    return hourly_cpu[-1]


def extract_pillar_areas(chart_data, pillars):
    #print 'pillars',pillars
    #print 'chart_data',chart_data

    seconds = []
    cpu_by_second = []
    cpu_by_hour = []
    cpu_increase_labels = []

    pillar_start_second = None
    pillar_end_second = None
    for pillar in pillars:
        pillar_type = pillar[2]
        if pillar_type == 'Start':
            pillar_start_second = pillar[0]
            print 'Start',pillar_start_second
        elif pillar_type == 'End':
            pillar_end_second = pillar[0]
            print 'End',pillar_end_second
            assert not pillar_start_second is None
            cpu_diff_area_total = 0
            for second in range(pillar_start_second, pillar_end_second+1):
                value_second = chart_data[0][1][second]
                assert second == value_second
                value_cpu = chart_data[0][2][second]
                average_hourly_cpu = get_average_hourly_cpu(chart_data, pillar_start_second, pillar_end_second)
                cpu_diff_area_total += (value_cpu-average_hourly_cpu)

                seconds.append('s'+str(value_second))
                cpu_by_second.append(value_cpu)
                cpu_by_hour.append(average_hourly_cpu)

            seconds.append('s'+str(pillar_end_second+1))
            cpu_by_second.append(None)
            cpu_by_hour.append(None)

            seconds_in_area = pillar_end_second-pillar_start_second+1
            cpu_increase = int(round(cpu_diff_area_total))
            label_position = pillar_start_second+int(seconds_in_area/2)
            cpu_increase_labels.append((label_position, '+'+str(cpu_increase)+'%*s'))
            
            pillar_start_second = None
            pillar_end_second = None

    #print seconds
    return [('cpu by second', seconds, cpu_by_second),
            ('cpu by hour', seconds, cpu_by_hour)], cpu_increase_labels

#vertical lines
def build_chart_shapes(pillars):
    shapes = []
    for pillar in pillars:
        tag = pillar[1]
        if tag == 'CAP':
            color = 'rgb(255, 255, 0)'
        else:
            color = 'rgb(255, 0, 255)'
        shapes.append({
            'type': 'line',
            'x0': pillar[0],
            'y0': -10,
            'x1': pillar[0],
            'y1': 100,
            'line': {
                'color': color,
                'width': 1,
            },
        })
    return shapes

def build_chart_annotations(pillars):
    annotations = []
    for pillar in pillars:
        tag = pillar[1]
        annotations.append({
            'x': pillar[0],
            'y': 100,
            'xref': 'x',
            'yref': 'y',
            'text': tag,
            # 'showarrow': True,
            # 'arrowhead': 7,
            # 'ax': 0,
            # 'ay': -40
        })
    return annotations

def build_chart_labels(labels):
    annotations = []
    for label in labels:
        position = label[0]
        tag = label[1]

        annotations.append({
            'x': position,
            'y': 40,
            'xref': 'x',
            'yref': 'y',
            'text': tag,
            # 'showarrow': True,
            # 'arrowhead': 7,
            # 'ax': 0,
            # 'ay': -40
        })
    return annotations

def build_double_chart(title1, traces1, pillars1, title2, traces2):
    fig = plotly.tools.make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(title1, title2))
    for trace in traces1:
        fig.append_trace(trace, 1, 1)
    for trace in traces2:
        fig.append_trace(trace, 2, 1)
    shapes = build_chart_shapes(pillars1)
    annotations = build_chart_annotations(pillars1)

    fig['layout']['xaxis1'].update(title='# of seconds since start')
    fig['layout']['yaxis1'].update(title='usage, percents', range=[-10, 120])
    fig['layout']['yaxis2'].update(title='usage, percents', range=[0, 100])
    fig['layout']['shapes'].extend(shapes)
    fig['layout']['annotations'].extend(annotations)

    plotly.offline.plot(fig, filename='usage.html')

def build_pillar_areas_chart(traces, pillars, labels):
    bag_pillars = [p for p in pillars if p[2] != 'Pillar']
    stringified_bag_pillars = [('s'+str(p[0]),p[1],p[2]) for p in bag_pillars]
    print stringified_bag_pillars

    shapes = build_chart_shapes(stringified_bag_pillars)
    annotations = build_chart_annotations(stringified_bag_pillars)

    stringified_labels = [('s'+str(l[0]),l[1]) for l in labels]
    labels = build_chart_labels(stringified_labels)

    layout = go.Layout(
        shapes = shapes,
        annotations = annotations+labels,
        # xaxis=dict(
        #     autotick=False,
        #     showticklabels=True
        # )
    )
    fig = go.Figure(data=traces, layout=layout)
    plotly.offline.plot(fig, filename='pillar_areas.html')

def main():
    if len(sys.argv) != 3:
        print 'Usage: ',sys.argv[0],'folder1 folder2'
        print 'Folder is expected to contain csv and logs'
        return

    folder1 = sys.argv[1]
    folder2 = sys.argv[2]

    filename1 = os.path.join(folder1, 'pulse.csv')
    filename2 = os.path.join(folder2, 'pulse.csv')

    chart_data1 = build_chart_data(filename1)
    chart_data2 = build_chart_data(filename2)

    pillars1 = extract_pillars_from_logs(folder1)
    pillars1 = map_pillars(filename1, pillars1)

    title1 = build_title(filename1, chart_data1)
    traces1 = build_traces(chart_data1)
    title2 = build_title(filename2, chart_data2)
    traces2 = build_traces(chart_data2)
    build_double_chart(title1, traces1, pillars1, title2, traces2)

    time.sleep(1)

    chart_data_pillar_areas, cpu_increase_labels = extract_pillar_areas(chart_data1, pillars1)
    traces_pillar_areas = build_traces(chart_data_pillar_areas)
    build_pillar_areas_chart(traces_pillar_areas, pillars1, cpu_increase_labels)

main()
