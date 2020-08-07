import os
import subprocess
import webbrowser

import PySimpleGUI as gui
import psutil as psutil


class GitHubPagesProject:

    def __init__(self):
        self.window = None
        self.test_process = None
        self.deploy_process = None
        self.path = 'jpgrafika.github.io'

    def event_handler(self, event_key, values):
        if event_key.startswith('test'):
            self.test_process = subprocess.Popen(f'exec ./test.sh', shell=True, cwd=self.path)
            webbrowser.open('http://0.0.0.0:8000')
        elif event_key.startswith('stop'):
            if self.test_process:
                self.kill_process(self.test_process)
                self.test_process = None
                print('stopped')
            else:
                print('wasn\'t running')
        elif event_key.startswith('download'):
            password = values.get('pass')
            if os.path.exists(self.path):
                os.system(f'git -C {self.path} pull')
                print('updated')
            else:
                os.system(f'git clone https://jpgrafika:{password}@github.com/jpgrafika/jpgrafika.github.io.git')
                print('downloaded')
        elif event_key.startswith('deploy'):
            self.deploy_process = subprocess.Popen(f'exec ./deploy.sh', shell=True, cwd=self.path)
        else:
            self.show_error('Unknown command: {}'.format(event_key))

    @staticmethod
    def kill_process(process):
        ps_process = psutil.Process(process.pid)
        for proc in ps_process.children(recursive=True):
            proc.kill()
        ps_process.kill()

    @staticmethod
    def show_error(error):
        gui.popup_no_buttons(error, keep_on_top=True)

    @staticmethod
    def close_popup():
        gui.PopupAnimated(None)

    def draw_window(self):
        gui.change_look_and_feel('DarkAmber')

        column = [
            [gui.Text('Wpisz hasło do github')],
            [gui.InputText(key='pass')],
            [gui.Button('Pobierz projekt', key='download', border_width=0)],
            [gui.Button('Testuj projekt', key='test', border_width=0)],
            [gui.Button('Skończ test', key='stop', border_width=0)],
            [gui.Button('Umieść projekt w internecie', key='deploy', border_width=0)],
        ]

        layout = [
            [gui.Column(column)]
        ]
        self.window = gui.Window('Projekt', layout)

        try:
            while True:
                event, values = self.window.read()
                if event in (None, 'Exit'):  # if user closes window or clicks cancel
                    break
                self.event_handler(event, values)
        except Exception as e:
            print('unexpected error!')
            print(e)
        finally:
            self.window.close()
            if self.test_process:
                self.kill_process(self.test_process)
            if self.deploy_process:
                self.kill_process(self.deploy_process)


if __name__ == '__main__':
    project = GitHubPagesProject()
    project.draw_window()
