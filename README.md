npm i -g appium
appium driver install uiautomator2@3.7.9
Appium-Python-Client==2.6.0
selenium==4.6.0


## Process to get performance comparisons AL_OS:
1. Run python3 src/main.py -i 192.168.1.112:5555
2. Collect Reports from Downloads
 Done Here


## Process to get ChromeOS Reports
1. Run Tast test to get Results
    - Need to save file as _chromeos when pulling from device via tast or ssh

2. Collect Reports From Downloads

# TODO()
## Tast Script
1. Open Chrome and inspector to Lighthouse panel
2. Loop
    1. Nav to URL
    2. Press Generate report
        - Check for errors
        - save error report to file by url.json

## Pull Files from DUT to Host device: bash script
1. ssh connect to device
2. Pull files from downloads, should be empty except for current runs files
    - scp  local


## Extract Data

1. Move all reports to some directory
2. Pass that directory to extracts script
3. Extractscript will take all reports from the directy and get filenames
4. It will split them and into 2 list:
    - ChromeOS reports   [when pulled from DUT, _chromeOS is appended to filename]
    - AL_OS reports
5. Create 2 dicts: chromeos_filenames, al_os_filenames
    - For each chromeos report:
        1. find url in filename
            - filename pattern == URL-date.json
            - url may contain dashes, split filename by - and take everthing before the last dash
                - (find index of last dash and get substring.)

        2. add url to chromeOS dict
            - { url: file name }


    ** Repeat for AL_OS reports filenames


6. Now we can get intersection of each dict to get common key/ URLs
    - for key in intersection of maps:
        chrome_file = chromeos_filenames[key]
        al_os_file = al_os_filenames[key]
        res = compare(chrome_file, al_os_file) # returns chromeos_score, al_os_score
        rows.append(key, res[0], res[1])



- We already have ability to compare two reports but we only want to compare the below 9 keys




1. Place reports in folder
2. run extract script
3. For each comparison
    - Take these 11 metrics and give each platform a score to see who won
    - If ChromeOS has better scores of 6/11 then AL_OS would have 5/11
    - we report in overview tsv file=>
                     Url; ChromeOS; AL OS;
                    https://youtube.com; 6;5;
                    https://facebook.com; 3;8;
                    https://google.com; 9;2;

    - We can then just save these metrics over the file instead of keeping all the data.
        1. "firstContentfulPaint": ChromeOS 3,  AL_OS 1
        2. "largestContentfulPaint": ChromeOS 3,  AL_OS 1
        3. "interactive": ChromeOS 3,  AL_OS 1
        4. "speedIndex": ChromeOS 3,  AL_OS 1
        5. "totalBlockingTime": ChromeOS 3,  AL_OS 1
        6. "maxPotentialFID": ChromeOS 3,  AL_OS 1

        7. "cumulativeLayoutShift": ChromeOS 3,  AL_OS 5
        8. "cumulativeLayoutShiftMainFrame": ChromeOS 3,  AL_OS 5
        9. "lcpLoadStart": ChromeOS 3,  AL_OS 5                                # Might Take these out of the overview
        10. "lcpLoadEnd": ChromeOS 3,  AL_OS 5                                 # Might Take these out of the overview
        11. "timeToFirstByte": ChromeOS 3,  AL_OS 5

3. TSV created per site?