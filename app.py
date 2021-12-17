from tkinter import Button, Entry, Frame, Label, Menu, Tk, messagebox
import json
from tkinter.filedialog import askdirectory
from tkinter.ttk import Combobox
import pyperclip
import webbrowser
import pytube


class App:
    root = Tk()
    settings = json.load(
        open('resources/data/settings.json', "r", encoding="utf-8"))
    language = None

    def __init__(self):
        App.language = json.load(open(
            "resources/data/languages/{}.json".format(App.settings["language"]), encoding="utf-8"))
        App.root.iconbitmap(App.settings["logo"])
        App.root.minsize(600, 400)
        App.root.title(App.language["title"])
        App.root.resizable(False, False)
        MenuBar()
        Main()

    def update():
        App.root.title(App.language["title"])
        MenuBar.update()
        Main.update()

    def change_lang(lang):
        App.settings["language"] = lang
        json.dump(App.settings, open('resources/data/settings.json',
                  "w", encoding="utf-8"), indent=4)
        App.settings = json.load(
            open('resources/data/settings.json', "r", encoding="utf-8"))
        App.language = json.load(open(
            "resources/data/languages/{}.json".format(App.settings["language"]), encoding="utf-8"))
        App.update()


class Main:
    top = Frame(App.root)

    def __init__(self):
        Main.top.place(width=600, height=380)
        self.head = Frame(Main.top, bg="#333333")
        self.head.place(y=0, width=600, height=40)

        self.welcome = Label(
            self.head, text=App.language['welcome'], bg="#333333", fg="white", font=(18), pady=10)
        self.welcome.pack()
        self.body = Frame(self.top)
        self.body.place(y=40, width=600, height=340)

        self.label_for_main_folder = Label(
            self.body, text=App.language['main_folder'], font=(18), bg="#eee")
        self.entry_for_main_folder = Entry(
            self.body, width=70)
        self.entry_for_main_folder.insert(0, App.settings['main_folder'])
        self.entry_for_main_folder.configure(state="readonly")

        self.chose = Button(
            self.body, text=App.language['chose_folder'], width=12, command=self.chose_file)

        self.label_for_url = Label(
            self.body, text=App.language['label_two'], font=(18), bg="#eee")
        self.url = Entry(self.body, width=70)
        self.label_for_type = Label(
            self.body, text=App.language['label_three'], font=(18), bg="#eee")
        self.options = Combobox(self.body,
                                values=[
                                    App.language['highest_resolution'],
                                    App.language['lowest_resolution'],
                                    App.language['audio_only']],
                                width=41
                                )
        self.options.current(0)
        self.download = Button(
            self.body, text=App.language['download'], width=12, command=self.download)

        if App.settings['language'] == "english":
            self.label_for_main_folder.place(x=20, y=20)
            self.entry_for_main_folder.place(x=23, y=60)
            self.chose.place(x=460, y=56)
            self.label_for_url.place(x=20, y=100)
            self.url.place(x=23, y=140)
            self.label_for_type.place(x=20, y=180)
            self.options.place(x=180, y=185)
            self.download.place(x=460, y=240)
        else:
            self.label_for_main_folder.place(x=(App.root.winfo_width(
            ) - self.label_for_main_folder.winfo_reqwidth()) - 20, y=20)
            self.entry_for_main_folder.place(x=(App.root.winfo_width(
            ) - self.entry_for_main_folder.winfo_reqwidth()) - 23, y=60)
            self.chose.place(x=(App.root.winfo_width(
            ) - self.chose.winfo_reqwidth()) - 460, y=56)
            self.label_for_url.place(x=(App.root.winfo_width(
            ) - self.label_for_url.winfo_reqwidth()) - 20, y=100)
            self.url.place(x=(App.root.winfo_width() -
                           self.url.winfo_reqwidth()) - 23, y=140)
            self.label_for_type.place(
                x=(App.root.winfo_width() - self.label_for_type.winfo_reqwidth()) - 20, y=180)
            self.options.configure(justify="right")
            self.options.place(x=(App.root.winfo_width() -
                               self.options.winfo_reqwidth()) - 180, y=185)
            self.download.place(x=(App.root.winfo_width() -
                                   self.download.winfo_reqwidth()) - 460, y=240)

        App.root.mainloop()

    def update():
        Main.top.destroy()
        Main.top = Frame(App.root)
        Main()

    def chose_file(self):
        self.entry_for_main_folder.configure(state="normal")
        self.entry_for_main_folder.delete(0, "end")
        self.entry_for_main_folder.insert(0, askdirectory())
        self.entry_for_main_folder.configure(state="readonly")
        App.settings['main_folder'] = self.entry_for_main_folder.get()
        json.dump(App.settings, open('resources/data/settings.json',
                  "w", encoding="utf-8"), indent=4)

    def download(self):
        if self.entry_for_main_folder.get() == "":
            return messagebox.showinfo(title=App.language['error'], message=App.language['error_massege_for_main_folder'])
        if self.url.get() == "":
            return messagebox.showinfo(title=App.language['error'], message=App.language['error_massege_for_url'])
        try:
            if self.options.get() == "Highest resolution" or self.options.get() == "أعلى دقة":
                pytube.YouTube(self.url.get()).streams.get_highest_resolution().download(
                    self.entry_for_main_folder.get())
            elif self.options.get() == "Lowest resolution" or self.options.get() == "أدنى دقة":
                pytube.YouTube(self.url.get()).streams.get_lowest_resolution().download(
                    self.entry_for_main_folder.get())
            elif self.options.get() == "Audio only" or self.options.get() == "صوت فقط":
                pytube.YouTube(self.url.get()).streams.get_audio_only().download(
                    self.entry_for_main_folder.get())
            else:
                pytube.YouTube(self.url.get()).streams.get_highest_resolution().download(
                    self.entry_for_main_folder.get())
        except:
            return messagebox.showinfo(title=App.language['error'], message=App.language['error_massege_for_bad_url'])
        messagebox.showinfo(
            title=App.language['success'], message=App.language['success_massege'])


class MenuBar:
    menu = Menu(App.root)

    def __init__(self):
        self.window = Menu(MenuBar.menu, tearoff=0)
        self.language = Menu(self.window, tearoff=0)
        self.language.add_radiobutton(
            label=App.language['en'], command=self.en)
        self.language.add_radiobutton(
            label=App.language['ar'], command=self.ar)
        self.window.add_cascade(
            label=App.language['language'] + "          ", menu=self.language)
        self.window.add_separator()
        self.window.add_command(
            label=App.language['exit'], command=App.root.destroy)
        self.menu.add_cascade(
            label=App.language['window'], menu=self.window)
        self.edit = Menu(MenuBar.menu, tearoff=0)
        self.edit.add_command(
            label=App.language['copy'] + "          ", command=MenuBar.copy)
        self.edit.add_command(
            label=App.language['cut'], command=MenuBar.cut)
        self.edit.add_command(
            label=App.language['paste'], command=MenuBar.paste)
        self.menu.add_cascade(label=App.language['edit'], menu=self.edit)

        self.help = Menu(MenuBar.menu, tearoff=0)
        self.help.add_command(
            label=App.language['what_is_new'] + "          ", command=MenuBar.what_is_new)
        self.help.add_command(label=App.language['check_for_updates'],
                              command=MenuBar.check_for_updates)
        self.help.add_separator()
        self.help.add_command(
            label=App.language['about'], command=MenuBar.about)
        self.menu.add_cascade(label=App.language['help'], menu=self.help)

        App.root.config(menu=MenuBar.menu)

    def update():
        MenuBar.menu.destroy()
        MenuBar.menu = Menu(App.root)
        MenuBar()

    def en(self):
        App.change_lang("english")

    def ar(self):
        App.change_lang("arabic")

    def copy():
        pyperclip.copy(App.root.focus_get().selection_get())

    def cut():
        MenuBar.copy()
        text = App.root.focus_get().get()
        text = text.replace(pyperclip.paste(), "")
        App.root.focus_get().delete(0, "end")
        App.root.focus_get().insert(0, text)

    def paste():
        x = App.root.focus_get().get()
        App.root.focus_get().delete(0, "end")
        App.root.focus_get().insert(0, x+pyperclip.paste())

    def what_is_new():
        webbrowser.open("www.google.com")

    def check_for_updates():
        messagebox.showinfo(
            title=App.language['check_for_updates'], message=App.language['no_updates'] + "         ")

    def about():
        msg = """Version: 0.0.1


Developer: Fowaz Ayed          """
        if App.settings["language"] == "arabic":
            msg = """الاصدار: 0.0.1

المطور: فواز عايد          """
        messagebox.showinfo(title=App.language['about'], message=msg)


App()
