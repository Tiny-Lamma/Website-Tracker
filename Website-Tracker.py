#!/usr/bin/python3

import requests
import hashlib
import pytz
import os
import csv
import sys
from urllib.parse import urlparse
from datetime import datetime


def read_file(filename):
	pass

def write_file(filename, contents, append=False):
	if append:
		file_object = open(filename, "a+")
	else:
		file_object = open(filename, "w+")
	file_object.write(contents)
	file_object.close()

def collect_website(url):
	user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'
	header = {'user-agent': user_agent}
	return requests.get(url, headers=header).text

def get_hash(contents):
	return hashlib.md5(contents.encode('utf-8')).hexdigest()

def get_previous_hash(website_id):
	#get latest hash from site_id.csv
	with open('site_db.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row['ID'] == website_id:
				return row['Latest Hash']
	return False

def get_number_of_versions(website_id):
	count = 0
	for name in os.listdir('.'):
		if website_id in name:
			count += 1
	return count

def add_to_site_db(website_id, website_url, latest_hash, versions, last_updated):
	fieldnames = ['ID', 'URL', 'Latest Hash', 'Versions', 'Last Updated']
	with open('site_db.csv', 'a+') as write_file:
		writer = csv.DictWriter(write_file, fieldnames=fieldnames)
		writer.writerow({'ID': website_id, 'URL': website_url, 'Latest Hash': latest_hash, 'Versions': versions, 'Last Updated': last_updated})

def update_site_db(website_id, website_url, latest_hash, versions, last_updated):
	with open('site_db.csv') as read_file, open('site_db-temp.csv', 'w+') as write_file:
		fieldnames = ['ID', 'URL', 'Latest Hash', 'Versions', 'Last Updated']

		reader = csv.DictReader(read_file, fieldnames=fieldnames)
		writer = csv.DictWriter(write_file, fieldnames=fieldnames)

		writer.writeheader()
		for row in reader:
			if row['ID'] == website_id:
				writer.writerow({'ID': website_id, 'URL': website_url, 'Latest Hash': latest_hash, 'Versions': versions, 'Last Updated': last_updated})
			else:
				if row['ID'] != 'ID':
					writer.writerow({'ID': row['ID'], 'URL': row['URL'], 'Latest Hash': row['Latest Hash'], 'Versions': row['Versions'], 'Last Updated': row['Last Updated']})
	os.remove('site_db.csv')
	os.rename('site_db-temp.csv', 'site_db.csv')

def capture_website(website_url):
	website_id = get_hash(website_url)
	timestamp = datetime.now(pytz.timezone('Australia/Sydney'))

	response = collect_website(website_url)
	hash = get_hash(response)

	previous_hash = get_previous_hash(website_id)

	if not previous_hash:
		print('[{0}] New site: {1}'.format(timestamp, website_url))
		add_to_site_db(website_id, website_url, hash, 1, timestamp)
	elif hash == previous_hash:
		print('[{0}] No changes: {1}'.format(timestamp, website_url))
		versions = get_number_of_versions(website_id)
		update_site_db(website_id, website_url, hash, versions, timestamp)
	else:
		print('[{0}] Change detected: {1}'.format(timestamp, website_url))
		versions = get_number_of_versions(website_id) + 1
		update_site_db(website_id, website_url, hash, versions, timestamp)

	write_file('[{0}]-{1}.html'.format(website_id, hash), 'URL: {0}\nCaptured: {1}\n{2}'.format(website_url, timestamp, response))

def main():
	if len(sys.argv) == 2:
		capture_website(sys.argv[1])
	else:
		capture_website('https://www.canihazip.com/s')  # static example (changes with wan ip address change).
		capture_website('https://www.google.com')	# dynamic each time

if __name__ == "__main__":
   main()
