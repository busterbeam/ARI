from tkinter import * # Tk, Label, Entry, Listbox, Text, Button, StringVar, TOP, X, Y, END, BOTTOM, LEFT, RIGHT, ACTIVE, CENTER
from math import ceil
import os
import re

class ARI:
    def __init__(self):
        self.root = Tk()
        self.s = StringVar()
        self.s.set('Search Mode')
        self.root.title('ARI')
        self.root.protocol('WM_DELETE_WINDOW',lambda wdw=self.root: wdw.quit())
        self.finish = None
        self.root.resizable(width=False, height=False)
        self.root.geometry('400x500')
        self.listoffiles = Listbox(self.root, height=17)
        self.store = Button(self.root, text='Save',
                            command=self.storage, font=('Courier', 18))
        self.searchb = Button(self.root, textvariable=self.s,
                              command=self.mode, font=('Courier', 18))
        self.instructs = Label(self.root, text='Entry Mode',
                               font=('Courier', 18))
        self.tstr = StringVar()
        self.tstr.set("Title of your 'Text'")
        self.entry = Entry(self.root, textvariable=self.tstr,
                           font=('Courier', 18), justify=CENTER)
        self.entry.bind('<FocusIn>', lambda x: \
                        self.entry.selection_range(0, END))
        self.text = Text(self.root,height=17)
        self.dstr = StringVar()
        self.details = Label(self.root, textvariable=self.dstr,
                             justify=LEFT, font=('Courier', 12))
        self.instructs.pack(side=TOP,fill=X,expand=True)
        self.entry.pack(side=TOP,fill=X,expand=True)
        self.searchb.pack(fill=X,expand=True)
        self.text.pack(fill=BOTH,expand=True)
        self.details.pack(fill=X,side=LEFT,expand=True)
        self.store.pack(side=RIGHT,fill=Y,expand=True,pady=5,padx=5)
        self.process_text()
        self.root.mainloop()

    def reading_age_of_text(self, text):
        characters = len(text)
        words = len(text.split(' '))
        sentences = len(re.split(r"[.!?]", text))
        method = ceil(float(4.71 * (characters / words) + 0.5 * (words
                      / sentences) - 21.43))
        if method < 0:
            method = 0
        return (str(characters - 1), str(words - 1), str(sentences
                - 1), str(method))

    def process_text(self):
        text = self.text.get('0.0', END)
        new = '\n'
        (c, w, s, m) = self.reading_age_of_text(text)
        des = 'There ' + (('is ' if int(c) == 1 else 'are '))
        self.dstr.set(des + c + ((' character' if int(c)
                      == 1 else ' characters')) + new + des + w
                      + ' words' + new + des + s + ' sentences' + new
                      + 'The reading age of the text is ' + m)
        self.details.after(10, self.process_text)

    def search(self):
        self.locks(self.tstr.get())
        if self.tstr.get() == "Title of your 'Text'":
            pass
        elif len(self.tstr.get()) > 2:
            if self.tstr.get() in self.text.get('0.0', END):
                index = self.text.search(self.tstr.get(), '0.0')
                last = '%s+%dc' % (index, len(self.tstr.get()))
                self.text.tag_add('key', index, last)
                self.text.tag_config('key', background='red',
                        foreground='white')
        if self.tstr.get() == '':
            self.text.tag_delete('key')
        self.sfinish=self.entry.after(100, self.search)

    def wide_search(self):
        self.listoffiles.delete(0, END)
        inp = str(self.tstr.get())
        filenames = self.lsting()
        if len(self.tstr.get()) > 0:
            for x in filenames:
                file = open(x,'r').read()
                self.locks(inp)
                out=self.keys(inp)
                if out[0]==file[-2:]:
                    for y in range(1,len(out)):
                        if out[y] in file.lower():
                            if x not in self.listoffiles.get(0):
                                self.listoffiles.insert(END, x)
        self.wfinish = self.listoffiles.after(100, self.wide_search)

    def keys(self,input):
        ilist=input.split(';')
        return ilist

    def locks(self, inp):
        try:
            if inp[-1] == ' ':
                self.tstr.set(inp.rstrip(' ') + ';')
                self.entry.icursor(END)
        except IndexError:
            return
        return

    def mode(self):
        if self.instructs['text'] == 'Text Search Mode':
            self.search_mode()
            return
        if self.instructs['text'] == 'Search Mode':
            self.entry_mode()
            return
        if self.instructs['text'] == 'Entry Mode':
            self.file_search_mode()
            return

    def search_mode(self):
        self.tstr.set('Enter age then keys')
        self.instructs['text'] = 'Search Mode'
        self.s.set('Entry Mode')
        self.store['text'] = 'Load'
        self.store['command'] = self.load
        self.text.pack_forget()
        self.store.pack_forget()
        self.details.pack_forget()
        self.listoffiles.pack(fill=X,side=TOP,expand=True)
        self.listoffiles.bind('<FocusIn>', lambda x: \
                              self.listoffiles.after_cancel(self.wfinish))
        self.store.pack(fill=Y,side=RIGHT,expand=True,pady=5,padx=5)
        self.wide_search()
        try:
            self.entry.after_cancel(self.sfinish)
        except ValueError:
            return
        return

    def entry_mode(self):
        try:
            self.entry.after_cancel(self.wfinish)
        except AttributeError:
            return
        self.store.pack_forget()
        self.listoffiles.pack_forget()
        self.text.pack(fill=BOTH,expand=True)
        self.store['text']='Save'
        self.store.pack(fill=Y,side=RIGHT,expand=True,pady=5,padx=5)
        self.s.set('Text Search Mode')
        self.instructs['text'] = 'Entry Mode'
        self.details.pack_forget()
        self.details.pack(fill=X,side=LEFT,expand=True)
        self.tstr.set("Title of your 'Text'")
        return

    def file_search_mode(self):
        self.s.set('Search Mode')
        self.search()
        self.instructs['text'] = 'Text Search Mode'
        self.tstr.set("Just Keyword")
        self.details.pack_forget()
        return

    def storage(self):
        stream = open(self.tstr.get() + '.txt', 'w+')
        stream.write(self.text.get('0.0', END) + '\n'
                     + self.dstr.get()[-2:])
        stream.close()
        return

    def load(self):
        file=self.listoffiles.get(ACTIVE)
        words=open(file,'r').read()
        words=words[:-2]
        self.text.delete("0.0",END)
        self.text.insert("0.0",words)
        self.entry_mode()

    def lsting(self):
        files = []
        for x in os.listdir('.'):
            if '.txt' in x:
                files.append(x)
        return files

ARI()
