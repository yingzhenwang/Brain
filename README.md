# Brain 5

## Repository Summary
In this repository, we have folders which split up tasks. In the Classifier folder, we have all classifier for training data. The Training Data folder holds wave files collected by our team using the SpikerBox and includes various wave lenghts and also error wave files. The Chrome folder holds the code for operating the Chrome Website using our classifier and is the script we ran in our final presentation, live.py is for controlling video play/pause and fastforward, present.py is for controlling our presentation. 

## Reproducible Code for Output Graphs
In "notebook.ipynb", this holds all the code for our graphs in the final report and also contains the final classifier for training data. It also includes our configuration of the classifier training. 

## Requirements
Please refer to the "requirements.txt" file to see packages needed to run code. In addition to this, we ran our scripts on M1 Macbooks. In order to run it you must modify line 21 of Chrome/live.py to make sure you have the correct directory of the chromedriver for your browser. And line 19 change c_port to the port your SpikerBox is connected to. 

After this intial setup you could use "Python3 Chrome/live.py" to execute the script, you will see a new browser window open and once the website is loaded the message "website loaded" will be printed to the output which signal the site is ready. Depends on the machine user might need to manually click on the video once to initiate SpikerBox control, afterwards user could twist or turn their arm to toggle play/pause, or tension their arm to fast forward five seconds.

To modify which video to play, replace video link in line 22 of Chrome/live.py.


## Group Members
This repository was managed by both Data Science students Martin Huang (500494994) and Harry Wang (490556311). The training data and classifier for the training data was primarily managed by Martin Huang. The Chrome script and final live classifier was primarily managed by Harry Wang. Data collection was primarily managed by both Physics Students Yuxuan Cheng (490062904) and Jamie Nicholas (490424858)


