# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from sensors import sensors

def index(request):
    time,cputemp,temperature,pressure,humidity,distance_flow_sensor,distance_level_sensor = sensors.get_sensor_data()
    s = "<table>"+\
	"<tr><td>Time</td><td>"+time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-5]+"</td></tr>"+\
	"<tr><td>CPU temperature,C</td><td>"+str(cputemp)+"</td></tr>"+\
	"<tr><td>Temperature,C</td><td>"+str(temperature)+"</td></tr>"+\
	"<tr><td>Pressure,hPa</td><td>"+str(pressure)+"</td></tr>"+\
	"<tr><td>Humidity</td><td>"+str(humidity)+"</td></tr>"+\
	"<tr><td>Distance flow</td><td>{0:5.2f}".format(distance_flow_sensor)+"</td></tr>"+\
	"<tr><td>Distance level</td><td>{0:6.2f}".format(distance_level_sensor)+"</td></tr>"+\
	"</table>"
    return HttpResponse(s)

