s  = '''Dec 22, 2023
Gross
$3,563.61
Take Home
$2,605.07
Hours
88
Dec 8, 2023
Gross
$3,563.61
Take Home
$2,605.06
Hours
88
Nov 24, 2023
Gross
$3,563.61
Take Home
$2,605.05
Hours
88
Nov 9, 2023
Gross
$4,211.29
Take Home
$2,988.63
Hours
104
Oct 25, 2023
Gross
$3,725.53
Take Home
$2,700.98
Hours
92
Oct 10, 2023
Gross
$2,915.93
Take Home
$2,220.41
Hours
72
Sep 25, 2023
Gross
$3,887.45
Take Home
$2,796.86
Hours
96
Sep 8, 2023
Gross
$3,887.45
Take Home
$2,796.84
Hours
96
Aug 25, 2023
Gross
$3,563.61
Take Home
$2,605.07
Hours
88
Aug 10, 2023
Gross
$3,563.61
Take Home
$2,605.06
Hours
88
Jul 25, 2023
Gross
$4,049.37
Take Home
$2,892.74
Hours
80
Jul 10, 2023
Gross
$3,563.61
Take Home
$2,605.06
Hours
88
Jun 23, 2023
Gross
$3,563.61
Take Home
$2,605.08
Hours
88
Jun 9, 2023
Gross
$3,887.45
Take Home
$2,796.83
Hours
96
May 25, 2023
Gross
$3,563.61
Take Home
$2,605.08
Hours
88
May 10, 2023
Gross
$3,239.77
Take Home
$2,413.30
Hours
80
Apr 25, 2023
Gross
$8,063.45
Take Home
$5,269.88
Hours
100
Apr 10, 2023
Gross
$3,641.48
Take Home
$2,651.31
Hours
96
Mar 24, 2023
Gross
$3,338.12
Take Home
$2,471.69
Hours
88
Mar 10, 2023
Gross
$2,731.40
Take Home
$2,108.64
Hours
72
Feb 24, 2023
Gross
$3,338.12
Take Home
$2,471.67
Hours
88
Feb 10, 2023
Gross
$4,399.88
Take Home
$3,100.45
Hours
116
Jan 25, 2023
Gross
$3,034.76
Take Home
$2,292.03
Hours
80
Jan 10, 2023
Gross
$4,551.56
Take Home
$3,190.40
Hours
120'''


items = s.split("\n")
N = len(items)



for i in range(0,N,7):
    group = items[i: i + 7]
    print(f"Date: {group[0]}, Gross: {group[2]}, Net: {group[4]}, Hours: {group[6]}")
