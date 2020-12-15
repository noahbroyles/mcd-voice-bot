import random

import selenium
from selenium import webdriver

RECEIPT_CODES = ["16588-13401-21420-15544-00021-5"]
browser = webdriver.Chrome(executable_path=".drivers/chromedriver")

for code in RECEIPT_CODES:
    # Go to the voice survey site
    browser.get("https://mcdvoice.com")

    # Get all the boxes
    cn1 = browser.find_element_by_id("CN1")
    cn2 = browser.find_element_by_id("CN2")
    cn3 = browser.find_element_by_id("CN3")
    cn4 = browser.find_element_by_id("CN4")
    cn5 = browser.find_element_by_id("CN5")
    cn6 = browser.find_element_by_id("CN6")

    # Get the code parts
    codeParts = code.split("-")

    # Fill all the boxes with the right code parts
    cn1.send_keys(codeParts[0])
    cn2.send_keys(codeParts[1])
    cn3.send_keys(codeParts[2])
    cn4.send_keys(codeParts[3])
    cn5.send_keys(codeParts[4])
    cn6.send_keys(codeParts[5])

    # Click the next button
    browser.find_element_by_id("NextButton").click()

    # Now we're on the page 1 where you say how you ordered, Drive-Thru, Carry-Out, Mobile, etc.
    # For now, we're all gonna be driving through
    # Drive thru is ALWAYS Opt2, for now
    driveThruSpan = browser.find_element_by_class_name("Opt2").find_element_by_class_name("radioSimpleInput").click()
    browser.find_element_by_id("NextButton").click()

    # Page 2
    # This is the page where you rate how satisfied overall you are with your visit

