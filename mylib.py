# import relevant packages for use in this script
from urllib.parse import urlsplit
from os.path import basename
import os, errno, re, shutil, urllib.request

# define scrape and save function, arguments are link, directory, file name and original url
def scrape_and_save(link, directory, file_name, original_url):
	# stip trailing slash and store original link and directory variables 
	orig_link = re.sub(r'\/$', '', link)
	orig_dir = re.sub(r'\/$', '', directory)
	# if the filename is index.html, set the filepath to original_directory
	if file_name == 'index.html':
		link_file_path = orig_dir + '/' + file_name
	else:
		# else, get the file_name from the file_path_generator function (pass file_name from original function call to this function)
		f_p = file_path_generator(re.sub(r'^ | $', '', file_name))
		# if filepath doesn't start with '/', add a '/'
		if f_p[0] != '/':
			f_p = '/' + f_p
		# set new directory variable for file parent folder 
		directory = orig_dir + f_p
		print (directory)
		# set link_file_path variable for filepath directly to file, uses url2name function (pass file_name from original function call to this function)
		link_file_path = directory + '/' + url2name(re.sub(r'^ | $', '', file_name))
		# if original link is in the asset
		if original_url in link:
			# set link variable to original_url + link (using regex to remove orinal url from link. This ensure consistent urls) 
			link  = original_url+'/'+re.sub(r"^/", '', link.replace(original_url, ''))
		# if first character of link is '/' and second character isn't 
		elif link[0] == '/' and link[1] != '/':
			# set link variable to original_url + link (using regex to remove orinal url from link. This ensure consistent urls) 
			link  = original_url+'/'+re.sub(r"^/", '', link.replace(original_url, ''))
		# if first character and second character of link is '/' 
		elif link[0] == '/' and link[1] == '/':
			# asset is 3rd party, add 'https:' to start of string
			link  = 'https:'+link
		elif 'http' not in link:
			# set link variable to original_url + link
			link  = original_url+'/'+re.sub(r"^/", '', link.replace(original_url, ''))

	# try and make new directory
	try:
		os.makedirs(directory)
	# raise error if error not errno.EExist
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

	# set user agent to prevent 403 errors
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0')]
	urllib.request.install_opener(opener)
	error_404 = False
	# try and download asset
	try:
		urllib.request.urlretrieve(link, link_file_path)
	# raise errors
	except urllib.error.HTTPError as e:
		if e.code == 404:
			error_404 = True
			print ("404 Error - File not found")
		else:
			raise e
	except Exception as ex:
		raise ex

	# if filename isn't index.html
	if file_name != 'index.html' and error_404 != True:
		# log message to console
		print ("Saving ingredient: " + link)
		# try opening index.html file with read permissions
		try:
			index = open(orig_dir+'/index.html', 'r')
		# raise errors
		except Exception as e:
			raise e
		# store file content and replace original asset link with local equivalent
		new_content = index.read().replace(orig_link, link_file_path)
		# close index file
		index.close()
		# reopen with write permissions
		index = open(orig_dir+'/index.html', 'w')
		# replace file content with new version
		index.write(new_content)
		# close file
		index.close()
	#  return True end of function
	return True

# finds and returns file name from url
def url2name(url):
	return basename(urlsplit(url)[2])

# returns filepath without filename
def file_path_generator(url):
	url = urlsplit(url)[2]
	file_name = basename(url)
	return url.replace(file_name, '')

# function to generate dev enviroment from template folder
def generate_dev_enviroment(config):
	# set variables based on config file
	client_directory = config["client_directory"]
	test_id = config["test_id"]
	test_directory = client_directory + test_id
	site_directory = test_directory + '/site'
	code_template = config["enviroment_template"]
	
	# try opening local site index.html with read permissions 
	try:
		index = open(site_directory+'/index.html', 'r')
	except Exception as e:
		raise e

	# update index content to include locro script tag and store in variable
	new_content = index.read().replace('</body>', '\t<script src="locro/locro.js"></script>\n</body>')
	# close file
	index.close()
	
	# open local site index.html with write permissions 
	index = open(site_directory+'/index.html', 'w')
	# replace index content with updated content
	index.write(new_content)
	# close file
	index.close()

	# try create locro directory in local site folder
	try:
		os.makedirs(site_directory + '/locro')
	# raise error if error not errno.EEXIST
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
	# try copying locro.js file to local site locro folder
	try:
		shutil.copy('locro.js', site_directory + '/locro')
	# raise error
	except Exception as e:
		raise e

	if os.path.isdir(test_directory + '/code') != True:
		print ("importing code template")
		shutil.copytree(code_template, test_directory + '/code')
