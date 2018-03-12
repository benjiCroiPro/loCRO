loCRO v0.1.3

loCRO is a local development tool aimed specifically at Conversion Optimisation Developers (COD's), allowing them to integrate local versions of client web pages with their local dev enviroments.


How to use it

1. Python 3

	Download and install the lastest version Python 3

	Please note: You may need to set up enviroment variables in order to correctly run the program

2. config.json

	Open the config.json file to configure the program.
	There are 4 key/value pairs in this file:
		
		client_directory - This is the absolute path to your client directory, where each individual test is stored. To easily get this, hold SHIFT and right click the folder you want the test to be stored in and select "Copy as path" to copy the absolute path. In order for Python to use the filepath, you will need to escape (double up) each backslash, like so; "C:\\Users\\Public\\Desktop\\Client\\"
		
		test_id -  This is the test id/name, this is a single string and can be named as you see fit.

		url -  This is the url you want to download

		enviroment_template - This should remain as is unless you specifically want to use a different enviroment_template. To use a different enviroment_template, please refer to the section below for instructions.

3. Run it

	Once the config.json file has been updated, simply open a terminal window in the folder containing scrape.py, type "python scrape.py" and press enter.


The Enviroment Template
	
	The Enviroment Template is essentially a template of your standard code folder and setup. The default template contains a gulpfile, package.json and build folder containing template V1 JS and SCSS files. this can be altered to match your personal preferences