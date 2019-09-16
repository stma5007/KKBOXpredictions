# load webdriver function from selenium
from os import mkdir
from selenium import webdriver
from time import sleep
from random import randint

# Note that the program needs the webdriverbinary to be in PATH or to be in the expected folder
# Linux	 : /usr/bin/google-chrome
# Mac	 : /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
# Windows: %HOMEPATH%\Local Settings\Application Data\Google\Chrome\Application\chrome.exe

def setupDriver(link):
	#Setting up Chrome webdriver Options
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('start-maximized') # makes the instance start full screen
	chrome_options.add_argument("--lang=en-gb") # sets the language to english

	#creating Chrome webdriver instance with the set chrome_options
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get(link)

	return driver

def getSubPages(link):
	driver = setupDriver(link)

	links = driver.find_elements_by_xpath('//*[@id="block-mainpagecontent"]/article/div/div[2]/div/div/div/div/div/div/span/a')
	while len(links) < 989:
		links = driver.find_elements_by_xpath('//*[@id="block-mainpagecontent"]/article/div/div[2]/div/div/div/div/div/div/span/a')
		driver.execute_script("window.scrollBy(0, 500)")
		sleep(0.25)

	links = [link.get_attribute('href') for link in links]
	driver.close()

	# Get the actual text of the reviews
	for link in links:
		yield link

def getTranscript(link):
	driver = setupDriver(link)

	try:
		nottranscript = driver.find_element_by_xpath('//*[@id="block-mainpagecontent"]/article/div/div[2]/div[3]/div/div[1]/div/a')
		if nottranscript: nottranscript.click()
	except: pass
	name = driver.find_element_by_xpath('//*[@id="block-mainpagecontent"]/article/div/div[1]/div/div/p[1]').text.replace(' ', '_')
	date = driver.find_element_by_xpath('//*[@id="block-mainpagecontent"]/article/div/div[1]/div/div/p[2]').text.replace(' ', '_').replace(',', '')
	try: transcript = driver.find_element_by_xpath('//*[@id="dp-expandable-text"]/div').text.strip()
	except: transcript = driver.find_element_by_xpath('//*[@id="block-mainpagecontent"]/article/div/div[2]/div[3]').text.strip()
	driver.close()
	return ((name,date),transcript)

def writeToFile(misc,text):
	try: mkdir('../../TranscriptsOfPresidents/'+misc[0])
	except: pass
	f = open('../../TranscriptsOfPresidents/{}/{}.txt'.format(*misc), 'w+')
	f.write(text)

try: mkdir('../../TranscriptsOfPresidents/')
except: pass

for i in getSubPages('https://millercenter.org/the-presidency/presidential-speeches'):
	writeToFile(*getTranscript(i))
