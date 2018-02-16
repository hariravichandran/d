## Import all the packages
import sys, csv, datetime, argparse
import pandas as pd
import numpy as np

from decimal import *

print sys.argv

infile = sys.argv[1]
pfile = sys.argv[2]
outfile = sys.argv[3]

loglevel = 0

valid_records = 0
rows_written = 0

## Create Dictionaries

#Input
year_count = {} #Year
drop_count = {} #invalid_column

repeat_donor = {} #Zip5 + Name
donor_year = {} #Zip5 + Name + Year

invalid_column_count = {}

#Output
repeat_donations = {} #Committee + Zip + Year
repeat_donations_total_amt = {} #Committee + Zip + Year
repeat_donations_total_nbr = {} #Committee + Zip + Year

now = datetime.datetime.now()
start_time = now
print('Begin Time: %s' % (start_time))
this_calendar_year = now.year

year_of_interest = this_calendar_year

with open(pfile, 'rb') as percentile_file:
	first_line = percentile_file.readline()

	percentile_wanted = int(first_line)


print('percentile: %d' % (percentile_wanted) )

#Names from Data Dictionary (FEC) - https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml
column_names = ['CMTE_ID', 'AMNDT_ID', 'RPT_TP', 'TRANSACTION_PGI', 'IMAGE_NUM', \
				'TRANSACTION_TP', 'ENTITY_TP', 'NAME', 'CITY', 'STATE', 'ZIP_CODE', \
				'EMPLOYER', 'OCCUPATION', 'TRANSACTION_DT', 'TRANSACTION_AMT', \
				'OTHER_ID', 'TRAN_ID', 'FILE_NUM', 'MEMO_CD', 'MEMO_TEXT', 'SUB_ID']

''' Desired Columns
CMTE_ID: identifies the flier, which for our purposes is the recipient of this contribution
NAME: name of the donor
ZIP_CODE: zip code of the contributor (we only want the first five digits/characters)
TRANSACTION_DT: date of the transaction
TRANSACTION_AMT: amount of the transaction
OTHER_ID: a field that denotes whether contribution came from a person or an entity
'''

with open(outfile, 'wb') as output_file:
	writer = csv.writer(output_file, delimiter = '|')

	with open(infile, 'rb') as input_file:
		reader = csv.DictReader(input_file, delimiter = '|', fieldnames = column_names)

		try:
			for row in reader:
				cmte = row['CMTE_ID']
				name = row['NAME']
				zip_code9 = row['ZIP_CODE']
				t_date = row['TRANSACTION_DT']
				t_amount = row['TRANSACTION_AMT']
				other_id = row['OTHER_ID']

				zip_code5 = zip_code9[0:5]

				#Find Invalid Date
				try:
					transformed_date = datetime.datetime.strptime(t_date, '%m%d%Y') #MMDDYY format, from data dictionary
					good_date = True
				except ValueError:
					good_date = False

				#Drop Invalid Records
				invalid_column = ''
				invalid_reason = ''
				drop = False
				if len(other_id) > 0:
					drop, invalid_column, invalid_reason = True, 'other_id', 'Other ID is populated'
				elif len(cmte) == 0:
					drop, invalid_column, invalid_reason = True, 'committee', 'Committee is empty'
				elif len(zip_code5) < 5:
					drop, invalid_column, invalid_reason = True, 'zip_code5', 'Zip Code must have 5 digits'
				elif len(t_amount) == 0:
					drop, invalid_column, invalid_reason = True, 't_amount', 'Transaction Amount is blank'
				elif len(name) == 0:
					drop, invalid_column, invalid_reason = True, 'name', 'Name is empty'
				elif not(',' in name):
					drop, invalid_column, invalid_reason = True, 'name', 'Last Name, First Name'
				elif good_date == False:
					drop, invalid_column, invalid_reason = True, 't_date', 'Transaction Date is empty/malformed'
				else:
					drop, invalid_column, invalid_reason = False, '', ''
				
				if invalid_column_count.has_key(invalid_column): #Create a dictionary
					invalid_column_count[invalid_column] += 1
				else:
					invalid_column_count[invalid_column] = 1

				if drop == False:
					amount = Decimal(t_amount)
					unique_donor = zip_code5 + ' ' + name
					year = t_date[4:8]
					valid_records += 1

					if year_count.has_key(year):
						year_count[year] += 1
					else:
						year_count[year] = 1

					if not donor_year.has_key(unique_donor): #Donor has not contributed before
						donor_year[unique_donor] = [year] 
					else: #Donor has contributed before
						other_years = donor_year[unique_donor]
						if year in other_years: 
							#Assumption: If a donor makes a donation again makes a donation again the same year, is not a repeat donor
							if loglevel > 1: print('Same Year Contribution -- Unique Donor: %s , Years Donated: %s' % (unique_donor, other_years))
						else:
							#Donated in a different year other than the year of interest; add to list of years
							repeat_donor[unique_donor] = True
							donor_year[unique_donor].append(year)
							other_years = donor_year[unique_donor]
							if loglevel > 1: print('Different Year -- Unique Donor: %s , Years Donated: %s' % (unique_donor, other_years))
						
							cmte_zip_year = cmte + ' ' + zip_code5 + ' ' + year

							if loglevel > 1: print('Year: %s, Year of Interest: %s' % (year, year_of_interest))

							if int(year) == int(year_of_interest):
								if loglevel > 1: print('Matched! - Year: %s, Year of Interest: %s' % (year, year_of_interest)) #Years matched
								if repeat_donations.has_key(cmte_zip_year):
									repeat_donations[cmte_zip_year].append(amount) #list of values
									repeat_donations_total_amt[cmte_zip_year] += amount #total amount
									repeat_donations_total_nbr[cmte_zip_year] += 1 #Number of donations
								else:
									repeat_donations[cmte_zip_year] = [amount] #list of values - 1 value
									repeat_donations_total_amt[cmte_zip_year] = amount #total amount
									repeat_donations_total_nbr[cmte_zip_year] = 1 #Number of donations

								#Calculate Percentile
								percentile_amount = np.percentile(np.array(repeat_donations[cmte_zip_year]), \
									percentile_wanted, interpolation = 'nearest')

								percentile_amount_rounded = Decimal(percentile_amount).quantize(Decimal('1.'))

								total_amount = repeat_donations_total_amt[cmte_zip_year]
								total_count = repeat_donations_total_nbr[cmte_zip_year]

								writer.writerow([cmte, zip_code5, year, percentile_amount_rounded, total_amount, total_count])
								rows_written += 1

		except csv.Error as err:
			print('Filename: %s , Line Number: %d, Error: %s' % (infile, reader.line_num, err))
			#sys.exit('Filename: %s , Line Number: %d, Error: %s' % (infile, reader.line_num, err))
		else:
			print('Filename: %s , Lines Processed: %d' % (infile, reader.line_num))

if loglevel > 1:
	rd = pd.DataFrame(repeat_donor.items(), columns = ['Repeat Donor', 'Status'])
	print(rd)

	dy = pd.DataFrame(donor_year.items(), columns = ['Unique Donor', 'Years'])
	print(dy)

ic = pd.DataFrame(invalid_column_count.items(), columns = ['Invalid Column', 'Count'])
print(ic)

yc = pd.DataFrame(year_count.items(), columns = ['Year', 'Count'])
print(yc)

print('Number of Valid Records: %i' % valid_records)
print('Number of Rows Written: %i' % rows_written)

end_time = datetime.datetime.now()
print('End Time: %s' % (end_time))

elapsed_time = end_time - start_time
print('Elapsed Time: %s' % (elapsed_time))
