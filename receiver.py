import sublime
import sublime_plugin

import socket
import json

class chooser(sublime_plugin.TextCommand):

    def run(self, edit):
        self.scripts = self.get_scripts()
        # print(self.scripts)
        self.script_list = [x['guid'] + " | " + x['name'] for x in self.scripts['scriptStates']]
        # self.items = ['hello','whaaaaaaat','aaaaaaaa','2222222222222','4421asd']
        self.window = sublime.active_window()
        # print(self.script_list)
        self.window.show_quick_panel(self.script_list, self.on_done)
        print("ok picker go!")
        


    def on_done(self, index):
        sel_item = self.scripts["scriptStates"][index]
        print("picked")
        print(json.dumps(sel_item, indent=4))
        if 'ui' in sel_item:
            print("has ui")
            print(sel_item['ui'])
            self.open_file(sel_item['guid'] + " | " + sel_item['name'] + " | ui", sel_item['ui'])
        else:
            print("nope but heres a new one")
            self.open_file(sel_item['guid'] + " | " + sel_item['name'] + " | ui", "")

        if 'script' in sel_item:
            print(sel_item['script'])
            self.open_file(sel_item['guid'] + " | " + sel_item['name'] + " | script", sel_item['script'])
        else:
            print("nope but heres a new one")
            self.open_file(sel_item['guid'] + " | " + sel_item['name'] + " | script", "")


    def get_scripts(self):
        # its like poking a bear | poke = message | bear == addr
        # will return scripts

        HOST = '127.0.0.1'  # The server's hostname or IP address
        PORT = 39999        # The port used by the server

        data = json.dumps({"messageID":0})

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(data.encode("UTF-8"))
            print("sent it")
            # data = s.recv(1024)

        # print('Received', repr(data))
        full_data = ""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            print("listening")
            c.bind((HOST, 39998))
            c.listen(1)
            conn, addr = c.accept()
            with conn:
                print("connected by", addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    full_data += data.decode("UTF-8")
        # print(json.dumps(full_data, indent=4))
        # print("\n\n-------------------------")
        # print(json.loads(full_data)['scriptStates']['name'])
        json_string = json.loads(full_data)
        return json_string
        # for script in json_string['scriptStates']:
        #     print(json.dumps(script, indent=4))
        #     print("---------------")


    def open_file(self, name, contents):
        current = self.window.new_file()
        current.set_name(name)
        current_view = self.window.active_view()
        # current_view.tts_write('catcat', {"message": contents})
        # write_out
        # current_view.insert(self.edit_obj, 0, contents)


class tts_write(sublime_plugin.TextCommand):
    def run(self, edit, message):
        self.view.insert(edit, 0, message)

class tts_save(sublime_plugin.TextCommand):
    # make sure to switch to name() as opposed to file_name() for testing and dev purposes
    def run(self, edit):
        current_window = sublime.active_window()
        current_view = current_window.active_view()
        # current_type = 'script' if current_view.name().split(" | ", 1)[0]
        target_name = current_view.file_name().split("\\", 10)[-1].split(".py")[0].split(" | ", 2)[-1]

        print(target_name)
        # for x in sublime.windows():
        #     for c in x.views():
        #         print(c)
        #         print(c.name())
