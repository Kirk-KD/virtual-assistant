import speech_recognition as sr
import pyttsx3 as tts

from command import CommandList


class Handler:
    def __init__(self, prefix):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.tts_engine = tts.init()
        self.tts_engine.setProperty("rate", 150)
        self.tts_engine.setProperty('voice', self.tts_engine.getProperty('voices')[1].id)

        self.prefix = prefix
        self.command_list = CommandList(self)

        self.input = ""
        self.command = []

    def start(self):
        self.tts("Starting python virtual assistant. Ready for command.")
        while True:
            try:
                self.get_input()
                print(self.input)

                if len(self.command) > 0 and self.next_arg(self.prefix):
                    for c in self.command_list.commands:
                        if self.next_arg(c.name):
                            c.command()
                            break

                        self.reset_command(remove_prefix=True)
                    else:
                        self.tts("Sorry, unknown command.")

                    self.tts("Ready for command.")
                else:
                    print("[Not Prefix]")
            except sr.UnknownValueError:
                print("[Unknown Value]")
            except IndexError:
                print("[Invalid Input]")

    def get_input(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
            audio = self.recognizer.listen(source)

        self.input = str(self.recognizer.recognize_google(audio)).lower()
        self.reset_command()

    def next_arg(self, arg: str):
        correct_arg = True

        for word in arg.split():
            if word != self.command[0]:
                correct_arg = False
                break
            else:
                self.command.pop(0)

        return correct_arg

    def reset_command(self, remove_prefix: bool = False):
        self.command = self.input.split()
        if remove_prefix:
            self.command.pop(0)

    def tts(self, text: str):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
