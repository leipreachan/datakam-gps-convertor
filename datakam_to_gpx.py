#!/usr/bin/python
from datetime import datetime
import gpxpy
import gpxpy.gpx
import sys

def convert_to_gpx(log_file):
    gpx_file = log_file + '.gpx'
    with open(log_file) as f:
        content = f.read().splitlines()

    for i, var in enumerate(content):
        content[i] = var.split('\t')

    gpx = gpxpy.gpx.GPX()

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # name.text = "datakam track " + filename

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

for i, v in sys.argv:
    if i>1:
        convert_to_gpx(v)