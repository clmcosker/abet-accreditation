# script to loop through data and determine if abet

# Caitlin McOsker

import csv
import pandas as pd

# Type of data (ENGR or IT)
dept = input('Data Name: ')

# CSV name strings
# raw data
rawcsv = input('CSV to count: ')
# cleaned data file
datacsv = 'data_{}.csv'.format(dept)
# counter file
countcsv = 'counter_{}.csv'.format(dept)

# open csv with master data
data = pd.read_csv(rawcsv, encoding='utf8', header=0)

# clean any remaining duplicates
# remove duplicates postings from different cities, same url, or same description
data = data.drop_duplicates(['company','position']).drop_duplicates('url').drop_duplicates('description')
# remove emplty rows
data = data.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
# write to csv
data.to_csv(path_or_buf = datacsv, index=False)


# csv to hold variable counts
writer = csv.writer(open(countcsv, "w", newline=''))
# headers
writer.writerow(['abet', 'accredited', 'accreditation'])

# loop through lines
temp = []
var0_counter = 0
var1_counter = 0
var2_counter = 0
with open(datacsv, encoding='utf-8') as cleandata:
	# header
	headerrow = next(cleandata)
	# reader
	reader = csv.reader(cleandata, delimiter=",", skipinitialspace=True)
	for row in reader:
		descriptions = row[5]
		#convert line (string) to list of strings
		words = descriptions.split()
		#print(words)
		var0 = 0 # abet
		var1 = 0 # accredited
		var2 = 0 # accreditation
		
		# loop through each word
		for word in words:
			if word == 'abet':
				var0 = 1
				var0_counter += 1
				continue
			elif word == 'accredited':
				var1 = 1
				var1_counter += 1
				continue
			elif word == 'accreditation':
				var2 = 1
				var2_counter += 1
				continue
			else:
				continue
		writer.writerow([var0, var1, var2])

print('Word Counters:\nabet: {}\naccredited: {}\naccreditation: {}'.format(var0_counter,var1_counter,var2_counter))	
