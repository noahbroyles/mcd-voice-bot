# mcd-voice-bot
# by Noah Broyles
#
# This program was written because the McDonald's voice survey is too long and redundant for a human with a normal time schedule to take every time they eat McDonald's.
# While humans might hate and avoid this survey, a selenium bot will eat it right up! (Lots of pun intended)
# So if McDonald's really wanted accurate voice survey responses, they ought to put a QR code right on the receipt, which linked to a sensible, one page, 2 - 3 question survey.
# And none of this "handing out voice cards" crap. It doesn't work, especially with this long boring survey linked to it. (I know, I work there ;)
#


# Imports
import random
from selenium import webdriver


def getChoice(customChoices=["Opt5", "Opt4", "Opt3", "Opt2", "Opt1"], customWeights=(40, 30, 15, 10, 5)):
    """
    Chooses a weighted random option for the survey options. Better answers are weighted higher ;)
    :param customChoices: Custom list[string] to make choices from
    :param customWeights: Custom weights to choose from
    :return: a random choice from customChoices, appropriately weighted
    """
    # We've got to make this random, but not TOO random... if you know what I mean ;)
    return random.choices(customChoices, weights=customWeights, k=1)[0]


def clickNext():
    """
    Clicks the "Next" button in the survey
    :return: nothing
    """
    # Click the next button
    browser.find_element_by_id("NextButton").click()


if __name__ == "__main__":

    # This list stores those crazy, 26 digit, nobody-has-the-time-for-these receipt codes that you need to take the crazy survey
    RECEIPT_CODES = ["16588-13401-21420-15544-00021-5"]

    # Set up the browser
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

        # Click to the next page
        clickNext()

        # Now we're on the page 1 where you say how you ordered, Drive-Thru, Carry-Out, Mobile, etc.
        # For now, we're all gonna be driving through
        # Drive thru is ALWAYS Opt2, for now
        browser.find_element_by_class_name("Opt2").find_element_by_class_name("radioSimpleInput").click()
        browser.find_element_by_id("NextButton").click()

        # Page 2
        # This is the page where you rate how satisfied overall you are with your visit
        choice = getChoice()
        # Choose an option
        browser.find_element_by_class_name(choice).find_element_by_class_name("radioSimpleInput").click()
        clickNext()

        # Page 3
        # This is the page where you rate certain things about your visit, crew, food taste and temperature, etc.
        table = browser.find_element_by_tag_name("table")
        trs = table.find_elements_by_css_selector(".InputRowOdd, .InputRowEven")
        for tr in trs:
            choice = getChoice(customChoices=["Opt5", "Opt4", "Opt3", "Opt2"], customWeights=(50, 20, 20, 10))
            tr.find_element_by_class_name(choice).find_element_by_class_name("radioSimpleInput").click()
        clickNext()

        # Page 4
        # This is the page where you rate some redundant crap about your food and order.
