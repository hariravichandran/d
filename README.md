# Table of Contents
1. [Introduction](README.md#introduction)
2. [Program Approach](README.md#program-approach)
3. [Input files](README.md#input-files)
4. [Output file](README.md#output-file)
5. [Percentile Computation](README.md#percentile-computation)
6. [Example](README.md#example)
7. [Unit Tests](README.md#unit-tests)
8. [Scalabilty Test](README.md#scalability-test)

# Introduction
Python is selected as a programming language, and it uses the standard libraries such as datetime, pandas, and numpy. The python program donor.py calculates the percentile, total amount, and total count of repeat contributions from donors to recipients. The donors are uniquely identified by a combination of zip code, first name, and last name. Repeat Donations are identified by the zip code, committee ID, and year.
# Program Approach
This program uses data dictionaries to do its computations efficiently for large data sets. For the entire set, it took two minutes and 42 seconds to process the entire data set of 7 million records (2017 - 2018 FEC dataset) on a 2016 13" Macbook Pro. It calculates three values: total dollars received, total number of contributions received, and donation amount in a given percentile.

## Input files
The Federal Election Commission provides data files from 2000 onwards and is [well-maintained](http://classic.fec.gov/finance/disclosure/ftpdet.shtml).

The program has been tested on individual contributions using the data files found at the FEC's website.  The test data files conform to the data dictionary [as described by the FEC](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).

The program uses the following fields from the FEC datasets:

* `CMTE_ID`: identifies the flier, which for our purposes is the recipient of this contribution
* `NAME`: name of the donor
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity 

## Output file
For the  output file that the program creates, `repeat_donors.txt`, the fields on each line should be separated by a `|`

## Percentile computation
The percentile computation was done by using a numpy module using the nearest-rank method.

# Example
Using the input files (`percentile.txt` and `itcont.txt`), the program creates the expected output. 

The program outputs the following `repeat_donors.txt` from the test cases in `itcont.txt`:

    C00384516|02895|2018|333|333|1
    C00384516|02895|2018|333|717|2

## Unit Tests
The program handles invalid data. This functionality has been tested with a special test file which includes all identified invalid test cases. The program successfully passed the tests. The program also passed the test case provided in `run_tests.sh`.

No additional folders were generated under the Test Suites folder. Rather, all the input files were kept in the original `input` file folder at the top level.

##### Example Test Log
```
$ sh run_tests.sh 
--[Case 1: Given Test Case]--
['./src/donor.py', './input/itcont.txt', './input/percentile.txt', './output/repeat_donors.txt']
Begin Time: 2018-02-15 19:46:37.239282
percentile: 30
Filename: ./input/itcont.txt , Lines Processed: 7

  Invalid Column  Count
0                     6
1       other_id      1

   Year  Count
0  2017      4
1  2018      2

Number of Valid Records: 6
Number of Rows Written: 2
End Time: 2018-02-15 19:46:37.266297
Elapsed Time: 0:00:00.027015

-e [PASS]: test_1 repeat_donors.txt
[Thu Feb 15 19:46:37 PST 2018] 1 of 1 tests passed
```

##### Invalid Test Log - Invalid and Valid Records
```
$ sh run.sh 
--[Case 2: Invalid and Valid Records]--
['./src/donor.py', './input/invalid.txt', './input/percentile.txt', './output/repeat_donors_invalid.txt']
Begin Time: 2018-02-15 19:49:11.079622
percentile: 30
Filename: ./input/invalid.txt , Lines Processed: 16

  Invalid Column  Count
0                     6
1       other_id      2
2           name      2
3         t_date      2
4      committee      2
5      zip_code5      1
6       t_amount      1

   Year  Count
0  2017      4
1  2018      2

Number of Valid Records: 6
Number of Rows Written: 2
End Time: 2018-02-15 19:49:11.109881
Elapsed Time: 0:00:00.030259
```
##### Invalid Test Log - Invalid Records Only
```
--[Case 3: Invalid Records Only]--
$ sh run.sh 
['./src/donor.py', './input/invalid_only.txt', './input/percentile.txt', './output/repeat_donors_invalid_only.txt']
Begin Time: 2018-02-15 19:49:13.147723
percentile: 30
Filename: ./input/invalid_only.txt , Lines Processed: 8

  Invalid Column  Count
0       other_id      1
1           name      2
2         t_date      2
3      committee      1
4      zip_code5      1
5       t_amount      1

Empty DataFrame
Columns: [Year, Count]
Index: []

Number of Valid Records: 0
Number of Rows Written: 0
End Time: 2018-02-15 19:49:13.164537
Elapsed Time: 0:00:00.016814
```


# Scalability Test
The program was run on the full data set that contains over 7 million entries, and it took 2 minutes and 42 seconds to complete on a 2016 13" Macbook Pro. The output is shown below:

##### Example run log
```
$ sh run.sh
--[Case 5: indiv18.txt (All data from 2018 (Feb.))]--
['./src/donor.py', './input/indiv18.txt', './input/percentile.txt', './output/indiv18_output.txt']
Begin Time: 2018-02-15 18:15:23.967300
percentile: 30
Filename: ./input/indiv18.txt , Lines Processed: 7031510

  Invalid Column    Count
0                 3918681
1      zip_code5     7493
2           name     6633
3       other_id  3098271
4         t_date      432

   Year    Count
0  2007        1
1  2015       38
2  2012        3
3  2017  3917557
4  2016      935
5  2018      147

Number of Valid Records: 3918681
End Time: 2018-02-15 18:18:05.499170
Elapsed Time: 0:02:41.531870
```

Based on this test, the program handles roughly 43,400 records per second. Given this scalability, the program will be able to handle all the FEC data sets. The program will easily handle streaming/real-time inputs.
