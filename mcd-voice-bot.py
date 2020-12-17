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
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


# Load up the feedback
with open("responses.txt", "r") as responseFile:
    POSSIBLE_FEEDBACK = [f for f in responseFile.read().split("\n")]


def getChoice(customChoices: list = ["Opt5", "Opt4", "Opt3", "Opt2", "Opt1"], customWeights=(40, 30, 15, 10, 5)):
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
    table = browser.find_element_by_tag_name("table")
    trs = table.find_elements_by_css_selector(".InputRowOdd, .InputRowEven")
    for tr in trs:
        opt = getChoice()
        tr.find_element_by_class_name(opt).find_element_by_class_name("radioSimpleInput").click()


def solveCheckBoxes():
    if "What items did you order?" in browser.page_source:
        # We're on a page with a bunch of boxes to check. We only want to check a random amount.
        # We're on the page where you check what you ordered.
        cataListDiv = browser.find_element_by_class_name("cataListContainer")
        checkBoxDivs = cataListDiv.find_elements_by_class_name("cataOption")[:-1]  # Except for the last one, nobody ordered "other" and want to talk about it
        boxesToCheck = random.randrange(1, len(checkBoxDivs) - random.randrange(1, int(len(checkBoxDivs)/2)))
        random.shuffle(checkBoxDivs)
        for i in range(boxesToCheck):
            checkBoxDivs[i].find_element_by_class_name("checkboxSimpleInput").click()
    elif "What type of problem" in browser.page_source:
        # Gosh, this is bad! Only click a few buttons!
        cataListDiv = browser.find_element_by_class_name("cataListContainer")
        checkBoxDivs = cataListDiv.find_elements_by_class_name("cataOption")
        boxesToCheck = getChoice(customChoices=[1, 2, 3, 4], customWeights=(50, 20, 15, 15))
        random.shuffle(checkBoxDivs)
        for i in range(boxesToCheck):
            checkBoxDivs[i].find_element_by_class_name("checkboxSimpleInput").click()
    elif "Which of the following areas should we focus on to improve" in browser.page_source:
        cataListDiv = browser.find_element_by_class_name("cataListContainer")
        checkBoxDivs = cataListDiv.find_elements_by_class_name("cataOption")
        boxesToCheck = getChoice(customChoices=[1, 2, 3, 4], customWeights=(50, 20, 15, 15))
        random.shuffle(checkBoxDivs)
        for i in range(boxesToCheck):
            checkBoxDivs[i].find_element_by_class_name("checkboxSimpleInput").click()


def solveYesNo():
    if "experience a problem" in browser.page_source:
        table = browser.find_element_by_tag_name("table")
        # Let's choose whether or not we had an issue. Opt2 is good
        opt = getChoice(customChoices=["Opt1", "Opt2"], customWeights=(20, 80))  # So every 8 out of ten times, there was no problem
        table.find_element_by_class_name(opt).find_element_by_class_name("radioSimpleInput").click()

        # Gucci! Now let's just return what we picked to the program can know
        return opt
    elif "place your order at a kiosk" in browser.page_source:
        # No, ofc not you fool
        browser.find_element_by_class_name("Opt2").find_element_by_class_name("radioSimpleInput").click()
        return False


def leaveComment():
    commentBox = browser.find_element_by_tag_name("textarea")
    if getChoice([True, False], (40, 60)):
        # We've gotta leave some feedback.
        feedback = random.choice(POSSIBLE_FEEDBACK)
        if len(feedback) > 30:
            POSSIBLE_FEEDBACK.remove(feedback)
        commentBox.send_keys(feedback)
        return True
    return False


def solveSingleRadioOption():
    optionLists = browser.find_element_by_class_name("rbListContainer").find_elements_by_class_name("rbList")
    choice = random.choice(optionLists)
    choice.find_element_by_class_name("radioSimpleInput").click()


def log(c, problemOccurred:bool, passes:int, exceptions:int, validationCode:int, commentLeft=False):
    # Whip out the data
    with open("blockchain.json", 'r') as jsonFile:
        jsonData = jsonFile.read()
    jsonData = json.loads(jsonData)

    codeData = {
        "code": c,
        "problemOccurred": problemOccurred,
        "passesTaken": passes,
        "exceptionsOccurred": exceptions,
        "validationCode": validationCode,
        "commentLeft": commentLeft
    }

    jsonData["codes"].append(codeData)

    # Store it back
    with open("blockchain.json", 'w') as jsonFile:
        jsonFile.write(json.dumps(jsonData, indent=4))


def bruteForceSurvey(surveyCode):
    """
    This method hacks its way through the survey, catching exceptions along the way
    :return: nothing
    """
    exceptionCount = 0
    passCount = 0
    PROBLEM = False
    COMMENT_LEFT = False

    while True:
        try:
            vc = browser.find_element_by_class_name("ValCode").text.split(": ")[1]
            print(f"Done! Validation code: {vc}")
            print(f"Problem: {'yes' if PROBLEM else 'no'}")
            print(f"Number of exceptions: {exceptionCount}")
            print(f"Passes made: {passCount}")
            print(f"Comment left: {'yes' if COMMENT_LEFT else 'no'}")
            log(surveyCode, PROBLEM, passCount, exceptionCount, validationCode=vc, commentLeft=COMMENT_LEFT)
            break
        except NoSuchElementException:
            pass

            try:
                passCount += 1
                COMMENT_LEFT = leaveComment()
            except NoSuchElementException:
                exceptionCount += 1

            try:
                solveTablesWithRadioButtons()
            except NoSuchElementException:
                exceptionCount += 1

            try:
                problem = True if solveYesNo() == "Opt1" else False
                clickNext()
                if problem:
                    PROBLEM = True
                    # Okay, here we have more tables with radio buttons. However, there are more options than just here. There is an N/A option(currently Opt9) as well
                    # We are going to custom solve this.
                    opt = getChoice(options + ["Opt9"], (20, 30, 10, 10, 10, 20))
                    browser.find_element_by_tag_name("table").find_element_by_class_name(opt).find_element_by_class_name("radioSimpleInput").click()
                    clickNext()
            except NoSuchElementException:
                exceptionCount += 1

            try:
                solveCheckBoxes()
            except NoSuchElementException:
                exceptionCount += 1

            try:
                solveSingleRadioOption()
            except NoSuchElementException:
                exceptionCount += 1

        clickNext()


if __name__ == "__main__":

    # This list stores those crazy, 26 digit, nobody-has-the-time-for-these receipt codes that you need to take the crazy survey
    RECEIPT_CODES = ["16588-13291-21620-15088-00021-5"]

    # Here is a convenient list for slicing
    options = ["Opt5", "Opt4", "Opt3", "Opt2", "Opt1"]

    for code in RECEIPT_CODES:
        if not len(code) == 31:
            print(f"Ignoring invalid code {code}")
            continue

        print(f"Taking the survey with code {code}...")

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

        # Check if for some reason the code wasn't valid
        if "Error: We are unable to continue the survey based on the information you provided." in browser.page_source:
            print(f"Ignoring invalid code {code}")
            browser.close()
            browser.quit()
            continue

        # Now we're on the page 1 where you say how you ordered, Drive-Thru, Carry-Out, Mobile, etc.
        # For now, we're all gonna be driving through
        # Drive thru is ALWAYS Opt2, Dine-in Opt1, Carry out Opt3
        browser.find_element_by_class_name("Opt3").find_element_by_class_name("radioSimpleInput").click()
        browser.find_element_by_id("NextButton").click()

        # Page 2
        # This is the page where you rate how satisfied overall you are with your visit
        choice = getChoice()
        # Choose an option
        browser.find_element_by_class_name(choice).find_element_by_class_name("radioSimpleInput").click()
        clickNext()

        # Since the survey is dynamic, I ran into a bit of an issue. No matter, brute force time!
        # We are going to run through all the pages, completing the appropriate actions along the way.
        bruteForceSurvey(code)
        # That should end us

        # Close the browser
        browser.close()
        browser.quit()

        # Let us know
        print(f"Finished survey with code {code}\n")
