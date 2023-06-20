from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import random, threading

bin = "/usr/local/bin/chromedriver"
path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# url = "file:///Users/joogps/Desktop/Queue-it.html"
# url = "https://google.com"
url = "https://taylor-swift-rj.sales.ticketsforfun.com.br/"

pageNumberID = "MainPart_lbQueueNumber"
buttonID = "hlLinkToQueueTicket2Text"
linkID = "queueIdLinkURL"

seekNumber = False
grabLinks = False

totalTabs = 0
openDrivers = 0

numbers = []
indexes = []
links = []
updateLinks = False

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-web-security");
    chrome_options.add_argument("--dns-prefetch-disable")
    chrome_options.binary_location = path
    return webdriver.Chrome(options=chrome_options, desired_capabilities=caps)

def open_queue(index):
    driver = get_driver()

    driver.get(url)

    global openDrivers
    openDrivers = openDrivers + 1
    
    if openDrivers == totalTabs:
        print("Opened last driver")
    else:    
        print("Opened driver "+str(openDrivers))

    number = None;
    # time.sleep(25);
    while (not number):
        if seekNumber:
            try:
                el = driver.find_element(By.ID, pageNumberID)
                html = el.get_attribute("innerHTML")

                # Mock a random chance of 0.9 that html is a number
                # html = str(random.randint(0, 1000000)) if random.random() > 0.1 else html

                if html.isdigit():
                    print("Number available – driver "+str(index)+": "+html)
                    number = int(html)
                    numbers.append((index, number))
                    check_numbers()
                    break
                else:
                    print("Element "+str(index)+" is not a number: "+html)
            except:
                print("Element "+str(index)+" not found")
                driver.quit()
                break;

        time.sleep(5)
    
    grabbed = False;
    while (not grabbed):
        if grabLinks:
            if index in indexes:
                link = driver.find_element(By.ID, linkID).get_attribute("innerHTML")
                # link = "MOCK_LINK" if random.random() > 0.2 else link
                if not "".__eq__(link):
                    print("Grabbed link for "+str(index)+", number " + str(number) + ": "+link)
                    links.append((number, link))
                    grabbed = True
                    break;
                
        time.sleep(5)

def check_numbers():
    if len(numbers) >= totalTabs:
        sort_numbers()

def sort_numbers():
    seekNumber = False
    numbers.sort(key=lambda tup: tup[1])
    print("Numbers available: "+str(len(numbers)))
    global indexes
    indexes = [x[0] for x in numbers[0:15]]
    print("Indexes: "+str(indexes))

threadLocal = threading.local()

workers = []

def open_tabs(number):
    print("Opening " + str(number) + " drivers")
    global totalTabs
    totalTabs = totalTabs + number
    for i in range(number):
        worker = threading.Thread(target=open_queue, args=(totalTabs+i,))
        worker.start()
        workers.append(worker)
        time.sleep(1)

print("Type SEEK to start seeking numbers, SORT to sort numbers, GRAB to grab links, ID to update an ID")
open_tabs(10)

while True:
    result = input()

    if result == "SEEK":
        print("Seeking numbers")
        seekNumber = True
    elif result == "SORT":
        sort_numbers()
    elif result == "GRAB":
        print("Grabbing links")
        grabLinks = True
    elif result == "ID":
        print("Which ID? (number, button or link)")
        id = input()
        if id == "number":
            newID = input()
            pageNumberID = newID
            print("New number ID: "+newID)
        elif id == "button":
            newID = input()
            buttonID = newID
            print("New button ID: "+newID)
        elif id == "link":
            newID = input()
            linkID = newID
            print("New link ID: "+newID)
        else:
            print("Unknown ID")
    elif result.isdigit():
        open_tabs(int(result))
    
    if grabLinks:
        links.sort(key=lambda tup: tup[0])
        for link in links:
            print("Número: "+str(link[0])+", link: "+link[1])
