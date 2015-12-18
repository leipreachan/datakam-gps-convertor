#!/usr/bin/python
from datetime import datetime
import os.path
import gpxpy
import gpxpy.gpx
import sys


def convert_to_gpx(log_file):
    print log_file + ' converting ...'
    gpx_file = log_file + '.gpx'
    if os.path.isfile(gpx_file):
        print gpx_file + ' file exist, skip converting'
        return

    with open(log_file) as f:
        content = f.read().splitlines()

    for i, var in enumerate(content):
        content[i] = var.split('\t')

    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for i, v in enumerate(content):
        if len(v) > 1:
            lat = v[1][1:]
            lon = v[2][1:]
            elev = v[3]
            t = datetime.strptime(v[0], "%Y-%m-%d %H:%M:%S")
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=elev, time=t))

    result = gpx.to_xml()

    result_file = open(gpx_file, 'w')
    result_file.write(result)
    result_file.close()
    print log_file + ' - done'

for i, v in enumerate(sys.argv):
    if i > 0:
        convert_to_gpx(v)
