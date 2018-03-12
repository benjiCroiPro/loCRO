from bs4 import BeautifulSoup
from pathlib import Path
import mylib, json, requests, re

config_file = Path("config.json")
if config_file.is_file():
	print ("Config file exists")

	with open('config.json', 'r') as f:
		print ("Checking config file")
		config = json.load(f)
		original_url = config['url']
		client_directory = config["client_directory"]
		test_id = config["test_id"]
		test_directory = client_directory + test_id
		site_directory = test_directory + '/site'
		code_directory = test_directory + '/code'

		r  = requests.get(original_url)

		data = r.text

		print ("Making soup")
		soup = BeautifulSoup(data, "html.parser")

		print ("Saving the recipe")
		mylib.scrape_and_save(original_url, site_directory, 'index.html', original_url)

		print ("Getting the ingredients")
		asset_tags = soup.find_all("link")

		for a in soup.find_all("script"):
			asset_tags.append(a)

		for a in soup.find_all("img"):
			asset_tags.append(a)

		for a in soup.find_all("div"):
			asset_tags.append(a)

		for asset in asset_tags:
			href = False
			if asset.has_attr('href') and asset.has_attr("rel"):
				if "stylesheet" in asset.get("rel"):
					href = asset.get('href')
			elif asset.has_attr('src'):
				href = asset.get('src')
			elif asset.has_attr('data-original'):
				href = asset.get('data-original')
			elif asset.has_attr('data-src'):
				href = asset.get('data-src')
			elif asset.has_attr('data-image-lg'):
				href = asset.get('data-image-lg')

			if href != False:
				if "url" in href:
					href = re.sub(r"url|\(|\)|\"|\'", "", href)
					print ("Found ingredient: "+ href)
					mylib.scrape_and_save(href, site_directory, href, original_url)
				else:
					print ("Found ingredient: "+ href)
					mylib.scrape_and_save(href, site_directory, href, original_url)

		mylib.generate_dev_enviroment(config)