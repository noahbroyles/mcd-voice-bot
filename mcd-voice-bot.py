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
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# Load up the feedback
with open("responses.txt", "r") as responseFile:
    POSSIBLE_FEEDBACK = [f for f in responseFile.read().split("\n")]


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


def solveTablesWithRadioButtons():
    while True:
        table = browser.find_element_by_tag_name("table")
        trs = table.find_elements_by_css_selector(".InputRowOdd, .InputRowEven")
        for tr in trs:
            opt = getChoice()
            tr.find_element_by_class_name(opt).find_element_by_class_name("radioSimpleInput").click()
        clickNext()


def solveCheckBoxes():
    while True:
        # We're on a page with a bunch of boxes to check. We only want to check a random amount.
        cataListDiv = browser.find_element_by_class_name("cataListContainer")
        checkBoxDivs = cataListDiv.find_elements_by_class_name("cataOption")
        boxesToCheck = random.randrange(int(0.2 * len(checkBoxDivs)), len(checkBoxDivs) - 1)
        random.shuffle(checkBoxDivs)
        for i in range(boxesToCheck):
            checkBoxDivs[i].find_element_by_class_name("checkboxSimpleInput").click()
        clickNext()


def solveYesNo():
    table = browser.find_element_by_tag_name("table")
    # Let's choose whether or not we had an issue. Opt2 is good
    opt = getChoice(customChoices=["Opt1", "Opt2"], customWeights=(20, 80))  # So every 8 out of ten times, there was no problem
    table.find_element_by_class_name(opt).find_element_by_class_name("radioSimpleInput").click()

    # Gucci! Now let's just return what we picked to the program can know
    return opt


def bruteForceSurvey():
    """
    This method hacks its way through the survey, catching exceptions along the way
    :return: nothing
    """
    exceptionCount = 0
    passCount = 0

    while exceptionCount < 30:
        try:
            vc = browser.find_element_by_class_name("ValCode")
            print(f"Done! SITE RESPONSE: {vc.text}")
            print(f"Number of exceptions: {exceptionCount}")
            print(f"Passes made: {passCount}")
            break
        except NoSuchElementException:
            pass
        try:
            print("Making a pass...")
            passCount += 1
            solveTablesWithRadioButtons()
        except NoSuchElementException:
            exceptionCount += 1
            try:
                solveCheckBoxes()
            except NoSuchElementException:
                exceptionCount += 1
                try:
                    problem = True if solveYesNo() == "Opt1" else False
                    clickNext()
                    if problem:
                        print("Shit, there was a problem with the order!")
                        # Okay, here we have more tables with radio buttons. However, there are more options than just here. There is an N/A option(currently Opt9) as well
                        # We are going to custom solve this.
                        opt = getChoice(options + ["Opt9"], (20, 30, 10, 10, 10, 20))
                        browser.find_element_by_tag_name("table").find_element_by_class_name(opt).find_element_by_class_name("radioSimpleInput").click()
                        clickNext()
                except NoSuchElementException:
                    exceptionCount += 1
                    try:
                        # Let's try leaving feedback (or not)
                        if getChoice([True, False], (20, 80)):
                            # We've gotta leave some feedback.
                            feedback = random.choice(POSSIBLE_FEEDBACK)
                            commentBox = browser.find_element_by_tag_name("textarea")
                            commentBox.send_keys(feedback)
                            clickNext()
                        else:
                            # Sorry MCD, no feedback today!
                            clickNext()
                    except NoSuchElementException:
                        exceptionCount += 1


if __name__ == "__main__":

    # This list stores those crazy, 26 digit, nobody-has-the-time-for-these receipt codes that you need to take the crazy survey
    RECEIPT_CODES = []

    # Here is a convenient list for slicing
    options = ["Opt5", "Opt4", "Opt3", "Opt2", "Opt1"]

    for code in RECEIPT_CODES:
        print(f"Taking the survey with code {code}")

        # Set up the browser
        browser = webdriver.Chrome(executable_path=".drivers/chromedriver")

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

        # Since the survey is dynamic, I ran into a bit of an issue. No matter, brute force time!
        # We are going to run through all the pages, completing the appropriate actions along the way.
        bruteForceSurvey()
        # That should end us

        # Close the browser
        browser.close()
        browser.quit()

        # Let us know
        print(f"Finished survey with code {code}\n")
