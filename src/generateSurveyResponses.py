import speech_recognition as sr

r = sr.Recognizer()

with open("../lib/responses.txt", 'r') as f:
    SURVEY_RESPONSES = [r for r in f.read().split("\n")]

while True:
    try:
        with sr.Microphone() as source:
            print("Speak now...")
            audio = r.record(source, duration=5)
            text = r.recognize_google(audio, language='en', show_all=True)
            try:
                response = text["alternative"][0]["transcript"]
            except TypeError:
                continue
            print(f"Recognized: {response}")
            SURVEY_RESPONSES.append(response)
    except KeyboardInterrupt:
        print(SURVEY_RESPONSES)
        responseString = "\n".join(SURVEY_RESPONSES)
        with open("../lib/responses.txt", "w") as f:
            f.write(responseString)
        break
