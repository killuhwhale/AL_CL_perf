import collections
import json
import os
from typing import List


'''
    Contains 2 tools:
        1. Comapre Lighthouse reports.
        2. Analyze Lighthouse reports to check site loaded.
'''

''' Creates Sheet to compare Lighthouse reports.'''
def compare(al_folder, chrome_folder):
    header = 'OS;URL;Error;Score (AL/CR);firstContentfulPaint;largestContentfulPaint;interactive;speedIndex;totalBlockingTime;maxPotentialFID;cumulativeLayoutShift;cumulativeLayoutShiftMainFrame;timeToFirstByte'
    # results = [header]
    print(header)
    da, db = get_aligned_files(al_folder, chrome_folder)
    for url in da:
        al_filename = da[url]
        chrome_filename = db[url]

        al_report = get_json_report(al_folder, al_filename)
        chrome_report = get_json_report(chrome_folder, chrome_filename)
        # print("Comparing:")
        # print(al_filename, " AND ", al_report)

        al_res, cr_res, combined = compare_reports(al_report, chrome_report)

        al_result = f'''AL;{url};{al_res}'''
        cr_result = f'''CR;{url};{cr_res}'''
        combined_result = f'''CO;{url};{combined}'''

        print(al_result)
        print(cr_result)
        print()
        # print(combined_result)

''' Creates Sheet to analyze Lighthouse reports for Loaded or not.'''
def check_loaded(folder):
    '''
        Checks a lighthouse report to see if the site loaded successfully or not.
    '''
    filenames = os.listdir(folder)
    rows = []

    for fn in filenames:
        filename = f"{folder}/{fn}"
        if not filename.endswith(".json"): continue
        check_failed_row = check_failed_report(filename)
        rows.append(check_failed_row)

    if len(rows) > 0:
        for r in rows:
            print(r)

'''  Helpers  '''
def failed_run_warnings(runWarnings):
    status_codes = ["400", "401", "403", "404", "500" ]
    failed = False
    for warning in runWarnings:
        for code in status_codes:
            if code in warning:
                failed = True
    return failed

def compare_reports(r1, r2):
    chromeos_score, al_os_score = 0, 0
    data = collections.defaultdict(List)
    for key in r1['metrics'].keys() & r2['metrics'].keys():
        data[key] = [r1['metrics'][key], r2['metrics'][key]]

    al_err = r1['error'] if r1['error'] else ""
    cr_err = r2['error'] if r2['error'] else ""

    target_keys =  [
        "firstContentfulPaint",
        "largestContentfulPaint",
        "interactive",
        "speedIndex",
        "totalBlockingTime",
        "maxPotentialFID",
        "cumulativeLayoutShift",
        "cumulativeLayoutShiftMainFrame",
        # "lcpLoadStart",
        # "lcpLoadEnd",
        "timeToFirstByte",
    ]

    al_metrics_res = ''
    cr_metrics_res = ''
    combined_metrics = ''

    # For each key in data show data in comma separated
    for key in target_keys:
        values = data[key]
        if values[0] < values[1]:
             chromeos_score += 1
             cr_metrics_res += f'''{values[1]};'''
             al_metrics_res += f'''{-values[0]};''' ## lost this round, make negative....

        else:
             al_os_score += 1
             al_metrics_res += f'''{values[0]};'''
             cr_metrics_res += f'''{-values[1]};''' ## lost this round, make negative....

        combined_metrics += f'{values[0]}/{values[1]};'

    al_res = f"{al_err};{al_os_score};{al_metrics_res}"
    cr_res = f"{cr_err};{chromeos_score};{cr_metrics_res}"

    combined = f"{al_err}/{cr_err};{al_os_score}/{chromeos_score};{combined_metrics}"

    return  al_res, cr_res, combined

def getURL(filename):
    ''' Extract URL

        accounts.google.com-20241003T142246.json
        accounts.google.com-20241003T142246_chromeos.json
    '''
    # Extract url from filename
    name_parts = filename.split("-")
    return "".join(name_parts[:-1])

def get_aligned_files(al_dir, chrome_dir):
    '''
    given two directories of similar files, group by url
    accounts.google.com-20241003T142246.json
    accounts.google.com-20241003T142246_chromeos.json
    '''
    al_filenames = os.listdir(al_dir)
    chrome_filenames = os.listdir(chrome_dir)
    da = {getURL(fn):fn for fn in al_filenames if fn.endswith('.json')}
    db = {getURL(fn):fn for fn in chrome_filenames if fn.endswith('.json')}
    return da, db

def check_failed_report(filename):
    '''
        Checks a lighthouse report to see if the site loaded successfully or not.
    '''
    row = ""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            report = json.load(f)
            print("Opened: ", filename)

            # Check for error report:
            requestedUrl = report['requestedUrl']
            runWarnings = failed_run_warnings(report['runWarnings'])
            metric_obj = report['audits']['metrics']

            # print("Run warning? ", runWarnings)

            if 'details' in  metric_obj and not runWarnings:
                metrics = metric_obj['details']['items'][0] if report else {}
                total = sum([metrics[k] for k in metrics ])
                err = ""
            else:
                err =  metric_obj['errorMessage'] if 'errorMessage' in  metric_obj else ', '.join(report['runWarnings'])
                total = 0

            row = f"{requestedUrl};{total};{err}"

    except Exception as err:
        print(f"Error w/ {filename=} ", err)

    return row

def get_empty_details():
    return {
            'items': [
                {
                    "firstContentfulPaint": 0,
                    "largestContentfulPaint": 0,
                    "interactive": 0,
                    "speedIndex": 0,
                    "totalBlockingTime": 0,
                    "maxPotentialFID": 0,
                    "cumulativeLayoutShift": 0,
                    "cumulativeLayoutShiftMainFrame": 0,
                    "lcpLoadStart": 0,
                    "lcpLoadEnd": 0,
                    "timeToFirstByte": 0,
                    "observedTimeOrigin": 0,
                    "observedTimeOriginTs": 0,
                    "observedNavigationStart": 0,
                    "observedNavigationStartTs": 0,
                    "observedFirstPaint": 0,
                    "observedFirstPaintTs": 0,
                    "observedFirstContentfulPaint": 0,
                    "observedFirstContentfulPaintTs": 0,
                    "observedFirstContentfulPaintAllFrames": 0,
                    "observedFirstContentfulPaintAllFramesTs": 0,
                    "observedLargestContentfulPaint": 0,
                    "observedLargestContentfulPaintTs": 0,
                    "observedLargestContentfulPaintAllFrames": 0,
                    "observedLargestContentfulPaintAllFramesTs": 0,
                    "observedTraceEnd": 0,
                    "observedTraceEndTs": 0,
                    "observedLoad": 0,
                    "observedLoadTs": 0,
                    "observedDomContentLoaded": 0,
                    "observedDomContentLoadedTs": 0,
                    "observedCumulativeLayoutShift": 0,
                    "observedCumulativeLayoutShiftMainFrame": 0,
                    "observedFirstVisualChange": 0,
                    "observedFirstVisualChangeTs": 0,
                    "observedLastVisualChange": 0,
                    "observedLastVisualChangeTs": 0,
                    "observedSpeedIndex": 0,
                    "observedSpeedIndexTs": 0
                }
            ]
        }

def get_json_report(folder, filename):
    if not filename.endswith(".json"): return {}
    json_report = {}
    try:
        with open(f"{folder}/{filename}", 'r', encoding='utf-8') as f:
            report = json.load(f)
            # Check for error report:

            requestedUrl = report['requestedUrl']
            runWarnings = failed_run_warnings(report['runWarnings'])
            metric_obj = report['audits']['metrics']

            # print("Run warning? ", runWarnings)

            if 'details' in  metric_obj and not runWarnings:
                metrics = metric_obj['details']['items'][0] if report else {}
                err = ""
            else:
                runWarnings =  metric_obj['errorMessage'] if 'errorMessage' in  metric_obj else ', '.join(report['runWarnings'])
                metric_obj['details'] = get_empty_details()
                metrics = metric_obj['details']['items'][0]


            json_report['filename'] = requestedUrl
            json_report['metrics'] = metrics
            json_report['error'] = runWarnings

            return json_report

    except Exception as err:
        print(f"Error w/ {filename=} ", err)

    return json_report


if __name__ == "__main__":
    AL_FOLDER = f"{os.path.expanduser('~')}/Downloads/al_perf_reports_brya_v12"
    CR_FOLDER = f"{os.path.expanduser('~')}/Downloads/al_perf_reports_brya_v12"

    # check_loaded(AL_FOLDER)
    compare(AL_FOLDER, CR_FOLDER)