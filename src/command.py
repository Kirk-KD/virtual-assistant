import inspect
import subprocess
import urllib.parse

import settings


class Command:
    def __init__(self, name: str, handler):
        self.name = name
        self.handler = handler

    def command(self):
        raise NotImplementedError()


class CommandList:
    def __init__(self, handler):
        self.handler = handler
        self.commands = []

        command_names = [command_name for command_name in dir(self) if not command_name.startswith("__")]
        for command in command_names:
            if inspect.isclass(getattr(self, command)):
                self.commands.append(getattr(self, command)(self.handler))

    class CSay(Command):
        def __init__(self, handler):
            super().__init__("say", handler)

        def command(self):
            self.handler.tts(" ".join(self.handler.command))
            return " ".join(self.handler.command)

    class CStart(Command):
        def __init__(self, handler):
            super().__init__("start", handler)

        def command(self):
            app_name = " ".join(self.handler.command)

            if app_name in settings.APPS.keys():
                subprocess.run(r'start "" "{}"'.format(settings.APPS[app_name]), shell=True)
                self.handler.tts("Started app: \"{}\"".format(app_name))
            else:
                self.handler.tts("Unknown app: \"{}\"".format(app_name))

    class CSearchFor(Command):
        def __init__(self, handler):
            super().__init__("search for", handler)

        def command(self):
            search_phrase = " ".join(self.handler.command)
            search_url = "" + urllib.parse.quote(search_phrase)
            subprocess.run('start "" "{}" "{}"'.format(settings.CHROME_PATH, search_url), shell=True)

    class CGoTo(Command):
        def __init__(self, handler):
            super().__init__("go to", handler)

        def command(self):
            url = " ".join(self.handler.command)
            subprocess.run('start "" "{}" "{}"'.format(settings.CHROME_PATH, url), shell=True)
