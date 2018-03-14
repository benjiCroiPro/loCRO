# import relevant packages for use in this script
from bs4 import BeautifulSoup
from pathlib import Path
import mylib, json, requests, re

# set config file path
config_file = Path("config.json")
# check if config file exists
if config_file.is_file():
	# success message
	print ("Config file exists")

	# open config file
	with open('config.json', 'r') as f:
		# relevant messaging
		print ("Checking config file")
		# set variables based on config settings
		config = json.load(f)
		original_url = config['url']
		client_directory = config["client_directory"]
		test_id = config["test_id"]
		test_directory = client_directory + test_id
		site_directory = test_directory + '/site'
		code_directory = test_directory + '/code'

		# get the requested url
		r  = requests.get(original_url)

		# store html from url in variable
		data = r.text

		# parse the HTML with BeautifulSoup package
		print ("Making soup")
		soup = BeautifulSoup(data, "html.parser")

		# pass the requested url data over to the scrape and save function in the mylib package
		print ("Saving the recipe")
		mylib.scrape_and_save(original_url, site_directory, 'index.html', original_url)

		# store all link tags in variable
		print ("Getting the ingredients")
		asset_tags = soup.find_all("link")

		# loop through all script tags and push to asset_tags variable (array)
		for a in soup.find_all("script"):
			asset_tags.append(a)

		# loop through all img tags and push to asset_tags variable (array)
		for a in soup.find_all("img"):
			asset_tags.append(a)

		# loop through all div tags and push to asset_tags variable (array)
		for a in soup.find_all("div"):
			asset_tags.append(a)

		# empyt array to store downloaded asset hrefs, this is checked to ensure assets are not downloaded more than once
		downloaded_assets = []

		# loop through all stored tags in asset_tags variable
		for asset in asset_tags:
			# set href variable to false because setting it in the else statement caused errors
			href = False
			# loop through attributes and match regex for any known and desired filetype 
			for attr in asset.attrs:
				val = str(asset.get(attr))
				if re.search(r"\.(ico|png|webP|jpg|jpeg|gif|bmp|js|css|scss|sass|woff|svg|json|pdf|txt)", val):
					href = val
			# if href not equal to false
			if href != False:
				# check if href not in list of already downloaded assets
				if href not in downloaded_assets:
					# add href to downloaded_assets
					downloaded_assets.append(href)
					# if url in href (doing this to detect 'url("")' in attributes)
					if "url" in href:
						# regex to strip unwanted characters
						href = re.sub(r"url|\(|\)|\"|\'", "", href)
						# print asset href and pass details onto scrape_and_save function
						print ("Found ingredient: "+ href)
						mylib.scrape_and_save(href, site_directory, href, original_url)
					else:
						# print asset href and pass details onto scrape_and_save function
						print ("Found ingredient: "+ href)
						mylib.scrape_and_save(href, site_directory, href, original_url)
				else:
					print("already downloaded: " + href)
					
		# Once done pass config file onto generae_dev_enviroment (function found in mylib file)
		mylib.generate_dev_enviroment(config)