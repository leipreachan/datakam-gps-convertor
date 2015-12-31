#!/usr/bin/python
from datetime import datetime
import os
import sys

import pytz
import gpxpy
import gpxpy.gpx


def get_date_time(datakam_date):
    """

    :rtype : datetime
    """
    default_timezone = 'Europe/Moscow'

    unaware = datetime.strptime(datakam_date, '%Y-%m-%d %H:%M:%S')
    result = pytz.timezone(default_timezone).localize(unaware)
    return result


def convert_to_gpx(log_file, force=False):
    print log_file + ' converting ...'
    gpx_file = log_file + '.gpx'
    if force is False and os.path.isfile(gpx_file):
        print gpx_file + ' file exist, skip converting'
        return

    with open(log_file) as f:
        content = f.read().splitlines()

    for i, var in enumerate(content):
        content[i] = var.split('\t')

    gpx = gpxpy.gpx.GPX()

    gpx_track_file_name = os.path.basename(log_file)
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_track.name = gpx_track_file_name
    gpx.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    last_point_date_time = get_date_time('1970-01-01 00:00:00')

    for i, v in enumerate(content):
        if len(v) < 5:
            continue

        point_date_time = get_date_time(v[0])
        delta = point_date_time - last_point_date_time
        if i != 0 and delta.seconds > 60 * 10:
            gpx_segment = gpxpy.gpx.GPXTrackSegment()
            gpx_track.segments.append(gpx_segment)

        last_point_date_time = point_date_time

        lat = v[1][1:]
        lon = v[2][1:]
        elevation = v[3]

        current_speed = v[4]
        magnetic_variation = v[5]
        point = gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=elevation, time=point_date_time, speed=current_speed)
        point.magnetic_variation = magnetic_variation
        gpx_segment.points.append(point)

    result = gpx.to_xml()

    result_file = open(gpx_file, 'w')
    result_file.write(result)
    result_file.close()
    print log_file + ' - done'


for i, v in enumerate(sys.argv):
    if i > 0:
        convert_to_gpx(v)
