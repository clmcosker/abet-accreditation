# final monster-get-data.py

# Caitlin McOsker

# input is URL (Monster search for 'information technology entry level')
# output cleaned data --> descriptions of jobs

import requests
from bs4 import BeautifulSoup as bs
import re
import csv
import math
import datetime
from nltk import word_tokenize
from nltk.corpus import stopwords

# function to get html from inside tag
def parseURL(html_data, regex):
	instance = str(html_data)
	instance = re.findall(regex, instance)[0]
	return instance

	
def getSoup(inputURL, jobsearch):
	# get first page soup
	originalPage = requests.get(inputURL)
	originalSoup = bs(originalPage.text, 'html.parser')
	# print(originalSoup.prettify())
	URL_list = [inputURL]
	
	jobNum = sum(int(i) for i in re.findall('\d+', originalSoup.find('h2', attrs={'class':'figure'}).text))
	pagNum = math.ceil(jobNum/20)
	
	# get list of urls
	for i in range(pagNum):
		if i == 0:
			continue
		if i == 1:
			continue
		page_url = ''.join([inputURL, '&stpage=1', '&page=', str(i)])
		URL_list.append(page_url)
	
	# open csv file -> description and information
	csvfile = open("output_1118data_{}.csv".format(jobsearch), "w", newline='')
	writer = csv.writer(csvfile)

	j=0
	#summary list to avoid repeats and remove ads
	summary_list = [
	'https://job-openings.monster.com/financial-sales-professional-concord-ca-us-massmutual-great-lakes/fddbdadb-9444-4a62-b73d-cd9cd25763f2,'
	'https://job-openings.monster.com/rn-registered-nurse-telemetry-bridgeton-mo-us-ssm-health-depaul-hospital-–-st-louis/f88d05c6-404c-48a1-86d1-54c2c62c78f2,'
	'https://job-openings.monster.com/dental-lab-technician-greensboro-nc-us-aspen-dental/8640dad2-f4fc-4421-8203-1a95579f4a69,'
	'https://job-openings.monster.com/truck-drivers-experienced-cdl-class-a-drivers-dedicated-route-milton-in-us-c-r-england/fff48bae-d6cb-4b05-ba3a-bcb3c6ca88d3,'
	'https://job-openings.monster.com/part-time-delivery-uber-eats-bothell-wa-us-uber-eats/ffc7ebef-a5f2-49c5-9513-e662c9cbc735,'
	'https://job-openings.monster.com/amazon-shopper-boise-id-us-amazon-workforce-staffing/fe9655df-1db0-4845-962e-7ce5eb76e81f,'
	'https://job-openings.monster.com/radar-test-engineer-principal-or-sr-principal-engineer-systems-test-colorado-springs-co-us-northrop-grumman/fd0765cc-fb69-4a8c-a822-2ea871acac0e,'
	'https://job-openings.monster.com/registered-nurse-ii-rn-med-surg-nights-10-000-sign-on-bonus-referral-bonus-houston-methodist-the-woodlands-hospital-the-woodlands-tx-us-houston-methodist/43a80739-a15d-4774-8cea-e00928649595,'
	'https://job-openings.monster.com/cdl-a-truck-driver-needed-corning-ks-us-hogan-transportation/ffec156a-0e68-4502-9e2e-4cece96602a3,'
	'https://job-openings.monster.com/registered-nurse-progressive-care-unit-full-time-10000-to-15000-sign-on-bonus-3000-relocation-incentive-available-to-daytona-beach-titusville-fl-us-adventhealth-daytona-beach/fe0f322d-e861-46d5-ba2e-04f108307d8f,'
	'https://job-openings.monster.com/pharmacist-landstuhl-rheinland-pfalz-de-sterling-medical/214092253,'
	'https://job-openings.monster.com/certified-surgical-tech-operating-room-ft-days-5k-sign-on-bonus-relocation-available-jacksonville-fl-us-adventhealth-palm-coast/fdd45dc7-88bd-4a8e-be27-e3e2622be885,'
	'https://job-openings.monster.com/certified-nursing-assistant-icu-full-time-nights-sebring-fl-us-adventhealth-sebring-wauchula-lake-placid/fc59de2b-3ec4-40f1-b0b4-c6a2e60129ea,'
	'https://job-openings.monster.com/clinical-team-lead-rn-surgery-idaho-falls-id-us-eastern-idaho-regional-medical-center/fb289c9e-b441-435f-a74a-8eeef30205d6,'
	'https://job-openings.monster.com/nurse-coordinator-full-time-days-bloomington-il-us-chestnut-health-systems/fae7c74e-27bf-483e-a418-3f564e4c3d49,'
	'https://job-openings.monster.com/registered-nurse-pacu-full-time-days-10k-sign-on-bonus-relocation-available-miami-fl-us-adventhealth-new-smyrna-beach/f8fd2cb4-d067-4ec0-b3e8-4677af847031,'
	'https://job-openings.monster.com/registered-nurse-labor-delivery-10-000-sign-on-nights-orlando-fl-us-adventhealth-tampa/f87b2d43-e1ac-4867-bae8-5f5c9c42bee1,'
	'https://job-openings.monster.com/registered-nurse-progressive-care-unit-full-time-nights-15000-sign-on-3000-relocation-available-to-orange-city-fl-cleveland-oh-us-adventhealth-fish-memorial/f82eb30f-f0cb-4e81-ad46-95a897750064,'
	'https://job-openings.monster.com/registered-nurse-critical-care-icu-er-float-pool-prn-killeen-tx-us-adventhealth-central-texas/f7d49a29-c4c3-4b4a-b981-c1089021359e,'
	'https://job-openings.monster.com/nurse-director-clinical-operations-logan-ut-ut-us-cache-valley-hospital/f4e8ae93-bc8c-4af8-b746-206c2825d5a7,'
	'https://job-openings.monster.com/new-grad-rn-behavioral-health-bountiful-ut-us-lakeview-hospital/ee6d30b4-3059-4382-bbe1-5315691d4922,'
	'https://job-openings.monster.com/rn-intermediate-care-unit-ogden-ut-us-ogden-regional-medical-center/e7c4b8c5-e12f-40db-a6e9-7f6f7611446c,'
	'https://job-openings.monster.com/medical-assistant-primary-care-lenexa-shawnee-mission-ks-us-adventhealth-shawnee-mission/e2c14a05-12a3-4d9c-80fb-19cb86ade2c0,'
	'https://job-openings.monster.com/charge-er-rn-payson-ut-us-mountain-view-hospital/dae6c221-378d-4774-8a32-887e5f49bee1,'
	'https://job-openings.monster.com/certified-nursing-assistant-ft-nights-m-s-renal-dialysis-ocala-fl-us-adventhealth-ocala/d2d35c72-9dbf-44d5-8d2f-1143ca9328d6,'
	'https://job-openings.monster.com/rn-icu-salt-lake-city-ut-us-st-marks-hospital/c63441ec-e786-467e-b7a8-c9ea1e6da95d,'
	'https://job-openings.monster.com/asc-606-842-technical-accounting-consultants-mclean-va-no-the-robert-joseph-group/213836109,'
	'https://job-openings.monster.com/occupational-health-technician-st-catherine-hospital-garden-city-ks-garden-city-ks-us-centura-health/f537f828-bc5e-4135-b312-6d3f756bb929,'
	'https://job-openings.monster.com/reservation-sales-agent-disney-reservation-center-tampa-fl-tampa-fl-us-disney-parks-resorts/569c245b-cb02-4a88-89eb-7278d74f11b4,'
	'https://job-openings.monster.com/rn-ortho-surgical-nights-part-time-colorado-springs-co-us-centura-health/fd834963-252e-428c-b2b2-9b8dc22cac2f,'
	'https://job-openings.monster.com/rn-registered-nurse-med-surg-colorado-springs-co-us-centura-health/d3286b85-3f4b-4bc0-9e2b-1e4978c66249,'
	'https://job-openings.monster.com/interventional-radiology-tech-non-reg-colorado-springs-co-us-centura-health/eba951d1-210c-4a21-b47a-5ae49d30a85c,'
	'https://job-openings.monster.com/telemetry-tech-lakewood-co-us-centura-health/f0be19fe-1216-4355-a54b-22b1c76054a0,'
	'https://job-openings.monster.com/anesthesia-tech-louisville-co-us-centura-health/e3bd7bbe-dd26-4c1a-8902-55af3f752ee7',
	'https://job-openings.monster.com/mental-health-coordinator-eloy-az-us-corecivic/d58e20f0-7624-4cda-9e92-6e5cd56d822f'
	]
	comparison_list = []
	for url in URL_list:
		#get page's soup
		page = requests.get(url)
		soup = bs(page.text, 'html.parser')
		
		# find job postings
		results = soup.find_all('section', class_='card-content', attrs = {'onclick':"MKImpressionTrackingMouseDownHijack(this, event)"})
		

		#get records for page's soup
		for record in results:
			# need to get company, location, etc for analysis later 11-11
			summary_url = parseURL(record.find('a', href = re.compile("https://job-openings.monster.com/*")),'"https://.*.\w"')[1:-1]
			# get rid of copies and ads
			if summary_url not in summary_list:
				summary_list.append(summary_url)
				summarydesc = getDescription(summary_url)
				# avoid writing empty and deleted descriptions
				if summarydesc != None:
					company = record.find('div', class_='company').find('span', attrs={'class':'name'}).contents[0]
					location = record.find('div', attrs={'class':'location'}).find('span', attrs={'class':'name'}).contents[0][2:-2]
					jobtitle = record.find('a', href = re.compile("https://job-openings.monster.com/*")).contents[0][:-2]
					
					# get rid of repeats of same jobs for different cities
					if [company, jobtitle] not in comparison_list:
						comparison_list.append([company,jobtitle])						
						#write description to csv
						try:
							writer.writerow([company, location, jobtitle, jobsearch, summary_url,summarydesc])
							# keep track of num records
							j+=1
							print(j)
						except:
							print('ERROR writing to CSV')
					else:
						print('copy of same job in different location')
				else:	
					print("Didn't pull text")
			else:
				print('copy or ad')

#function to get description from summary_url
def getDescription (url):
	
	# get soup for summary url
	summaryPage = requests.get(url)
	print(url)
	summarySoup = bs(summaryPage.text, 'html.parser')
	
	#find job description in soup
	summary = summarySoup.find('div', attrs={'id':'JobDescription'})
	
	try:
		#break into words
		text = summary.get_text()
		tokens = word_tokenize(text)
		#remove punctuation
		words = [word for word in tokens if word.isalpha()]
		# remove stop words
		stopwrds = stopwords.words('english')
		words = [i for i in words if not i in stopwrds]
		# normalize capitalization
		words = [word.lower() for word in words]
		
		# convert words list to string
		description = ' '.join(words)
	
		# returns str of cleaned words
		return description
	except:
		print('ERROR getting Description')

		
# input 
job = input('Enter Search Term (Ex: Data-Analyst): ')
url = 'https://www.monster.com/jobs/search/?q='+job

print('start:', datetime.datetime.now())
data = getSoup(url, job)
print('end:', datetime.datetime.now())

# test= getDescription('https://job-openings.monster.com/5139-data-quality-analyst-kennesaw-ga-us-qualitest/213012008')
#url = 'https://www.monster.com/jobs/search/?q=information-technology-entry-level'
# url = 'https://www.monster.com/jobs/search/?q=__27information-technology__27-entry-level&intcid=skr_navigation_nhpso_searchMainPrefill'
# url = 'https://www.monster.com/jobs/search/?q=__27information-technology__27-__27abet__27-accreditation-__2Dengineer&where=atlanta-ga'
# url = input('enter url: ')
# url = 'https://www.monster.com/jobs/search/?q=computer-science'
