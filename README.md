# RCPremChecker


WINDOWS ONLY



Usage:
Place all images into the 'in' folder or place csv file for auto-download and processing of images.
All images will be sorted into 'Accept' or 'Decline' folders located in 'out' depending on premium status.


Starting arguments:
(-v = Verbose, -m = Manual verification using 'a' to accept and 'd' to decline, -h or /? = Display help)


How to run. Open Powershell and type:

python3 index.py      (Normal   Mode)
python3 index.py -v   (Verbose  Mode)
python3 index.py -m   (Manual   Mode)
