import sublime
import sublime_plugin

import socket
import json

class tts_open_file(sublime_plugin.TextCommand):

    def run(self, edit):
        self.scripts = self.get_scripts()
        self.script_list = [x['guid'] + " | " + x['name'] for x in self.scripts['scriptStates']]
        self.script_list += {"cancel"}
        # print(self.scripts)
        self.window = sublime.active_window()
        window = sublime.active_window()
        window.show_quick_panel(self.script_list, self.on_done)

    def on_done(self, index):
        try:
            sel_item = self.scripts["scriptStates"][index]
            if 'ui' in sel_item:
                # print(sel_item['ui'])
                self.open_file(sel_item['guid'] + " | " + sel_item['name'] + " | ui", sel_item['ui'])
            else:
                # print("no ui")
                self.open_file(sel_item['guid'] + " | " + sel_item['name'] + " | ui", "")
            if 'script' in sel_item:
                # print(sel_item['script'])
                self.open_file(sel_item['guid'] + " | " + sel_item['name'] + " | script", sel_item['script'])
            else:
                # print("no script")
                self.open_file(sel_item['guid'] + " | " + sel_item['name'] + " | script", "")
        except Exception as e:
            # print ("FUCK")
            pass

    def get_scripts(self):
        HOST = '127.0.0.1'
        PORT = 39999

        data = json.dumps({"messageID":0})

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(data.encode("UTF-8"))

        full_data = ""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            # print("listening")
            c.bind((HOST, 39998))
            c.listen(1)
            conn, addr = c.accept()
            with conn:
                # print("connected by", addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    full_data += data.decode("UTF-8")
        json_string = json.loads(full_data)
        return json_string

    def open_file(self, name, contents):
        # print("this is the contents:>>>>>>>>>" + contents)
        current = self.window.new_file()
        current.set_name(name)
        # new_view = self.window.active_view()
        # print(new_view)
        # current.run_command('tts_writer', {"contents": contents})
        current.run_command('tts_write', {"contents": contents})    
        # current_view = self.active_window()

class tts_write(sublime_plugin.TextCommand):
    def run(self, edit, contents):
        # print("i am printing >>>:" + contents)
        self.view.insert(edit, 0, contents)

class tts_saver(sublime_plugin.TextCommand):
    def run(self, edit):
        current_window = sublime.active_window()
        current_view = current_window.active_view()

        current_guid = current_view.name().split(" | ", 3)[0]
        current_name = current_view.name().split(" | ", 3)[1]
        current_type = current_view.name().split(" | ", 3)[2]
        current_buffer = current_view.substr(sublime.Region(0, current_view.size()))

        # print(current_guid)
        # print(current_name)
        # print(current_type)

        found_buffer = ""

        if current_type == 'ui':
            #check for script to upload or upload blank
            for x in sublime.windows():
                for c in x.views():
                    if current_guid == c.name().split(" | ", 3)[0] and current_type != c.name().split(" | ", 3)[2]:
                        found_buffer = c.substr(sublime.Region(0, c.size()))
                        message = ({"messageID": 1, "scriptStates": [{"name": current_name, "guid": current_guid, "script": found_buffer, "ui": current_buffer}]})
                        break
                        #punch it out and take it 

        if current_type == 'script':
            #check for script to upload or upload blank
            for x in sublime.windows():
                for c in x.views():
                    if current_guid == c.name().split(" | ", 3)[0] and current_type != c.name().split(" | ", 3)[2]:
                        found_buffer = c.substr(sublime.Region(0, c.size()))
                        message = ({"messageID": 1, "scriptStates": [{"name": current_name, "guid": current_guid, "script": current_buffer, "ui": found_buffer}]})
                        break
                        #punch it out and take it

        self.send_script(message)

        # once check for files and contents
        # if they had other an accompanying script / ui it will have been saved if not it will still be defualt value of ""
        # prepare message to send back to tts

    def send_script(self, message):
        HOST = '127.0.0.1'
        PORT = 39999

        data = json.dumps(message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(data.encode("UTF-8"))
            # print("send")