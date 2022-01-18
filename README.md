# RCPremChecker


WINDOWS ONLY



Usage:
Place all images into the 'in' folder or place csv file for auto-download and processing of images.
All images will be sorted into 'Accept' or 'Decline' folders located in 'out' depending on premium status.



Starting arguments:
(-v = Verbose, -m = Manual verification using 'a' to accept and 'd' to decline, -h or /? = Display help)



How to run. Open Powershell and type:

"python3 index.py"     (Normal   Mode)

"python3 index.py -v"  (Verbose  Mode)

"python3 index.py -m"  (Manual   Mode)



INFO:

folder "img" holds test images.

folder "componets" holds required components, with install for python.

file "depleted.csv" is a test file for auto-download and verification.


Demo:

Manual mode:

https://user-images.githubusercontent.com/65334355/149931035-7d7ade46-d659-4c67-89fc-9b192ae2793a.mp4


Auto Mode:

https://user-images.githubusercontent.com/65334355/149931337-16b51910-2502-4378-bfd6-d9b22f384ccf.mp4
