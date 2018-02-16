#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
#
#python ./src/donor.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt

echo "--[Case 1: Given Test Case]--"
python ./src/donor.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt

#echo "--[Case 2: Invalid and Valid Records]--"
#python ./src/donor.py ./input/invalid.txt ./input/percentile.txt ./output/repeat_donors_invalid.txt

#echo "--[Case 3: Invalid Records Only]--"
#python ./src/donor.py ./input/invalid_only.txt ./input/percentile.txt ./output/repeat_donors_invalid_only.txt

#echo "--[Case 4: itcont_2018_20171113_20180131.txt]--"
#python ./src/donor.py ./input/itcont_2018_20171113_20180131.txt ./input/percentile.txt ./output/itcont_2018_20171113_20180131_output.txt

#echo "--[Case 5: indiv18.txt (All data from 2018 (Feb.))]--"
#python ./src/donor.py ./input/indiv18.txt ./input/percentile.txt ./output/indiv18_output.txt