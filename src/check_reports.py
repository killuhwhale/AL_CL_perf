import json
import os
from utils.utils import users_home_dir

'''
Checks reports and sums the metrics
prints out ; separated data to paste to sheets

URL;total;error message;
https://client.dhayxeqnylmaparu.net/;0;The page did not paint any content. Please ensure you keep the browser window in the foreground during the load and try again. (NO_FCP)l;
https://animesuge.to;0;;
https://asuracomic.net/8203063091;;

'''

# Folder Where reports are
FOLDER = f"{users_home_dir()}/Downloads/al_perf_reports"






def check():
    filenames = os.listdir(FOLDER)
    rows = []

    for fn in filenames:
        filename = f"{FOLDER}/{fn}"

        with open(filename, 'r', encoding='utf-8') as f:
            report = json.load(f)
            print("Opened: ", fn)

            # Check for error report:
            requestedUrl = report['requestedUrl']
            metric_obj = report['audits']['metrics']

            if 'details' in   metric_obj:
                metrics = metric_obj['details']['items'][0] if report else {}
                total = sum([metrics[k] for k in metrics ])
                err = ""
            else:
                err = metric_obj['errorMessage']
                total = 0

            row = f"{requestedUrl};{total};{err}"
            rows.append(row)

    for r in rows:
        print(r)



def check_alt():
    '''
    Tmp version to work with poorly formatted error files, I have fixed them but I dont want to reun so I will hack thischeck
    '''

    filenames = os.listdir(FOLDER)
    rows = []

    for fn in filenames:
        filename = f"{FOLDER}/{fn}"

        with open(filename, 'r', encoding='utf-8') as f:
            report = json.load(f)
            # print("Opened: ", fn)


            if not 'requestedUrl' in report:
                print(": ", fn)

            requestedUrl = fn if not 'requestedUrl' in report else report['requestedUrl']

            metric_obj = report['metrics']['audits']['metrics'] if not 'audits' in report  else  report['audits']['metrics']

            if 'details' in   metric_obj:
                metrics = metric_obj['details']['items'][0] if report else {}
                total = sum([metrics[k] for k in metrics ])
                err = ""
            else:
                err = metric_obj['errorMessage']
                total = 0

            row = f"{requestedUrl};{total};{err}"
            rows.append(row)

    for r in rows:
        print(r)




if __name__ == "__main__":
    check()