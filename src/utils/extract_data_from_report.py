'''
    Given a path to a report, load the json file and find following info:

    report = json.load("file_path")

    metrics = report['metrics']['details']['items'][0]


    Report = {
        "metrics": {
            "id": "metrics",
            "title": "Metrics",
            "description": "Collects all available metrics.",
            "score": 1,
            "scoreDisplayMode": "informative",
            "numericValue": 8781,
            "numericUnit": "millisecond",
            "details": {
                "type": "debugdata",
                "items": [
                {
                    "firstContentfulPaint": 3127,
                    "largestContentfulPaint": 4824,
                    "interactive": 8781,
                    "speedIndex": 7298,
                    "totalBlockingTime": 3623,
                    "maxPotentialFID": 1474,
                    "cumulativeLayoutShift": 0.00010012040845049745,
                    "cumulativeLayoutShiftMainFrame": 0.00010012040845049745,
                    "lcpLoadStart": 2872,
                    "lcpLoadEnd": 2910,
                    "timeToFirstByte": 207,
                    "observedTimeOrigin": 0,
                    "observedTimeOriginTs": 63229657676,
                    "observedNavigationStart": 0,
                    "observedNavigationStartTs": 63229657676,
                    "observedFirstPaint": 3443,
                    "observedFirstPaintTs": 63233100676,
                    "observedFirstContentfulPaint": 3443,
                    "observedFirstContentfulPaintTs": 63233100676,
                    "observedFirstContentfulPaintAllFrames": 3443,
                    "observedFirstContentfulPaintAllFramesTs": 63233100676,
                    "observedLargestContentfulPaint": 8707,
                    "observedLargestContentfulPaintTs": 63238365099,
                    "observedLargestContentfulPaintAllFrames": 8707,
                    "observedLargestContentfulPaintAllFramesTs": 63238365099,
                    "observedTraceEnd": 16232,
                    "observedTraceEndTs": 63245890099,
                    "observedLoad": 3626,
                    "observedLoadTs": 63233283308,
                    "observedDomContentLoaded": 286,
                    "observedDomContentLoadedTs": 63229943650,
                    "observedCumulativeLayoutShift": 0.00010012040845049745,
                    "observedCumulativeLayoutShiftMainFrame": 0.00010012040845049745,
                    "observedFirstVisualChange": 3377,
                    "observedFirstVisualChangeTs": 63233034676,
                    "observedLastVisualChange": 12656,
                    "observedLastVisualChangeTs": 63242313676,
                    "observedSpeedIndex": 8160,
                    "observedSpeedIndexTs": 63237817348
                },
                {
                    "lcpInvalidated": false
                }
                ]
            }
            },

    }

    # r1 chromeos, r2 AL OS
    def compare_reports(r1, r2):
        data = defaultdict(List)
        for key in intersect(r1, r2):
            data[key] = [r1[key], r2[key]]

        # For each key in data show data in comma separated
        for key in data:
            values = data[key]                           100             70
            print(key, values[0], value[1], f"{ 'dec' if values[0] > values[1] else 'inc'}", -(values[0] - values[1]) )



'''


import collections
import json
from typing import List


fp1 = "/home/killuh/Downloads/www.youtube.com-20240924T230012.json"
fp2 = "/home/killuh/Downloads/www.facebook.com-20240924T225052.json"

def get_report(fp):
    r = None
    with open(fp, 'r', encoding='utf-8') as f:
        r = json.load(f)
        print(r.keys())

    return r['audits']['metrics']['details']['items'][0] if r else {}



chromeOS_report = get_report(fp1)
AL_OS_report = get_report(fp2)


# r1 chromeos, r2 AL OS
def compare_reports(r1, r2):
    data = collections.defaultdict(List)
    for key in r1.keys() & r2.keys():
        data[key] = [r1[key], r2[key]]

    # For each key in data show data in comma separated
    for key in data:
        values = data[key]
        if key[:-2] == "Ts":
            print(key, ";", values[0], ";", values[1])
        else:
            print(key, ";", values[0], ";", values[1],  ";", f"{ 'dec' if values[0] > values[1] else 'inc'}", ";", -(values[0] - values[1]) )




compare_reports(chromeOS_report, AL_OS_report)