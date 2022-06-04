import threading
from tkinter import *
from tkinter import filedialog, messagebox
from manageUI import *
import asyncio

class UI:
    window = None
    btnStart = None
    lblFileToParse = None
    lblFileWithAcc = None
    lblProxy = None
    fileToParse = None
    fileWithAccountsForParse = None
    fileWithProxy = None
    btnAskFileToParse = None
    btnAskFileWithAccForParse = None
    btnAskFileProxy = None

    def __init__(self, async_loop):
        self.async_loop = async_loop
        self.window = Tk()
        self._init_ui()
        self.window.mainloop()

    def _init_ui(self):
        self.window.geometry('660x500')
        self.window.title("Instagram parser")
        self.lblFileToParse = Label(self.window, text="Select txt with usernames for parse divided by lines")
        self.lblFileToParse.grid(column=0, row=0, pady=5)
        self.btnAskFileToParse = Button(self.window, text="Select file", command=self.ask_for_file_to_parse)
        self.btnAskFileToParse.grid(column=0, row=3, pady=5)

        self.lblFileWithAcc = Label(self.window, text="Select txt with accounts that will be used for parsing ("
                                                      "username:password)")
        self.lblFileWithAcc.grid(column=0, row=5, pady=5)
        self.btnAskFileWithAccForParse = Button(self.window, text="Select file",
                                                command=self.ask_for_file_with_acc_to_parse)
        self.btnAskFileWithAccForParse.grid(column=0, row=7, pady=5)

        self.lblProxy = Label(self.window, text="Select txt with proxy")
        self.lblProxy.grid(pady=5)
        self.btnAskFileProxy = Button(self.window, text="Select proxy (ip:port)", command=self.ask_for_proxy)
        self.btnAskFileProxy.grid(pady=5)

        self.btnStart = Button(self.window, text="StartParse", command=self.btn_start_clicked)
        self.btnStart.grid(column=0, row=15, pady=100)

    def __asyncio_thread(self):
        self.async_loop.run_until_complete(start_parse(self))

    def btn_start_clicked(self):
        if self.fileToParse is None or self.fileWithAccountsForParse is None or self.fileWithProxy is None:
            messagebox.showinfo('Ошибка', 'Вы выбрали не все файлы')
            return
        #self.window.update_idletasks()

        threading.Thread(target=self.__asyncio_thread, args=()).start()
        #asyncio.run(start_parse(self))

    def ask_for_file_to_parse(self):
        self.fileToParse = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))

    def ask_for_file_with_acc_to_parse(self):
        self.fileWithAccountsForParse = filedialog.askopenfilename(
            filetypes=(("Text files", "*.txt"), ("all files", "*.*")))

    def ask_for_proxy(self):
        self.fileWithProxy = filedialog.askopenfilename(
            filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
