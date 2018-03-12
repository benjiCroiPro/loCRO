from urllib.parse import urlsplit
from os.path import basename
import os, errno, re, shutil, urllib.request

def scrape_and_save(link, directory, file_name, original_url):
	orig_link = re.sub(r'\/$', '', link)
	orig_dir = re.sub(r'\/$', '', directory)
	if file_name == 'index.html':
		link_file_path = orig_dir + '/' + file_name
	else:
		f_p = file_path_generator(file_name)
		if f_p[0] != '/':
			f_p = '/' + f_p

		directory = orig_dir + '/' + f_p
		link_file_path = directory + '/' + url2name(file_name)
		if original_url in link:
			link  = original_url+'/'+re.sub(r"^/", '', link.replace(original_url, ''))
		elif link[0] == '/' and link[1] != '/':
			link  = original_url+'/'+re.sub(r"^/", '', link.replace(original_url, ''))
		elif link[0] == '/' and link[1] == '/':
			link  = 'https:'+link

	try:
		os.makedirs(directory)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

	try:
		urllib.request.urlretrieve(link, link_file_path)
	except Exception as e:
		raise e

	if file_name != 'index.html':
		print ("Saving ingredient: " + link)
		try:
			index = open(orig_dir+'/index.html', 'r')

		except Exception as e:
			raise e

		new_content = index.read().replace(orig_link, link_file_path)
		index.close()
		index = open(orig_dir+'/index.html', 'w')
		index.write(new_content)
		index.close()
	return True

def url2name(url):
	return basename(urlsplit(url)[2])

def file_path_generator(url):
	url = urlsplit(url)[2]
	file_name = basename(url)
	return url.replace(file_name, '')

def generate_dev_enviroment(config):
	client_directory = config["client_directory"]
	test_id = config["test_id"]
	test_directory = client_directory + test_id
	site_directory = test_directory + '/site'
	code_directory = test_directory + '/code'
	code_template = config["enviroment_template"]
	
	# insert locro tag
	try:
		index = open(site_directory+'/index.html', 'r')
	except Exception as e:
		raise e

	new_content = index.read().replace('</body>', '\t<script src="locro/locro.js"></script>\n</body>')
	index.close()
	index = open(site_directory+'/index.html', 'w')
	index.write(new_content)
	index.close()

	shutil.copytree(code_template, test_directory + '/code')

	# # create locro directory in site
	# try:
	# 	os.makedirs(site_directory + '/locro')
	# except OSError as e:
	# 	if e.errno != errno.EEXIST:
	# 		raise
	# # create locro tag
	# try:
	# 	copy('locro.js', site_directory + '/locro')
	# except Exception as e:
	# 	raise e

	# try:
	# 	os.makedirs(code_directory)
	# except OSError as e:
	# 	if e.errno != errno.EEXIST:
	# 		raise

	# try:
	# 	os.makedirs(code_directory + '/build')
	# except OSError as e:
	# 	if e.errno != errno.EEXIST:
	# 		raise

	# # JS Template
	# try:
	# 	v1_js = open(code_directory+'/build/v1.js', 'w')
	# except Exception as e:
	# 	raise e

	# v1_js.write('// Variation JS goes here\n')
	# v1_js.close()

	# # CSS Template
	# try:
	# 	v1_css = open(code_directory+'/build/v1.scss', 'w')
	# except Exception as e:
	# 	raise e

	# v1_css.write('/* Variation sass goes here */\n')
	# v1_css.close()
	
	# # Gulp Template/Boilerplate
	# try:
	# 	copy('gulpfile.js', code_directory)
	# except Exception as e:
	# 	raise e
	# # TODO
	# 	# CSS Preprocessor
	# 	# JS Transpiler