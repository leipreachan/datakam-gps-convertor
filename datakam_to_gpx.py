#!/usr/bin/python
from datetime import datetime
import os
import gpxpy
import gpxpy.gpx
import sys


def convert_to_gpx(log_file, force=False):
    tz_offset = 3 * 60 * 60
    print log_file + ' converting ...'
    gpx_file = log_file + '.gpx'
    if force == False and os.path.isfile(gpx_file):
        print gpx_file + ' file exist, skip converting'
        return

    with open(log_file) as f:
        content = f.read().splitlines()

    for i, var in enumerate(content):
        content[i] = var.split('\t')

    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    fileName = os.path.basename(log_file)
    gpx_track.name = fileName
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for i, v in enumerate(content):
        if len(v) > 1:
            lat = v[1][1:]
            lon = v[2][1:]
            elevation = v[3]
            date_time = datetime.strptime(v[0], "%Y-%m-%d %H:%M:%S")
            # date_time.tz
            current_speed = v[4]
            magnetic_variation = v[5]
            point = gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=elevation, time=date_time, speed=current_speed)
            point.magnetic_variation = magnetic_variation
            gpx_segment.points.append(point)

    result = gpx.to_xml()

    result_file = open(gpx_file, 'w')
    result_file.write(result)
    result_file.close()
    print log_file + ' - done'


force = False
for i, v in enumerate(sys.argv):
    if i > 0:
        if i == 1 and v == '-f':
            force = True
        else:
            convert_to_gpx(v, force=force)
