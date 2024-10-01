

# bash pullFromDUT.sh ip dutDownloadDir hostDest
# bash pullFromDUT.sh 192.168.1.115 /home/user/fbb67f3975c4b6a4827e02fdd9b9c89c60f6314b/MyFiles/Downloads ~/Downloads/

# scp -r root@192.168.1.115:/home/user/fbb67f3975c4b6a4827e02fdd9b9c89c60f6314b/MyFiles/Downloads/*  ~/Downloads/
scp -r root@$1:$2/*  $3
