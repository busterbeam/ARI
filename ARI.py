#!/usr/bin/python
# -*- coding: utf-8 -*-
from tkinter import Tk, Label, Entry, Listbox, Text, Button, StringVar, \
    TOP, X, Y, END, BOTTOM, LEFT, RIGHT, ACTIVE, CENTER
from math import ceil
import os
import re


class ARI:

    def __init__(self):
        self.root = Tk()
        self.s = StringVar()
        self.s.set('Search Mode')
        self.root.title('ARI')
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
        self.text = Text(self.root, height=17)
        self.dstr = StringVar()
        self.details = Label(self.root, textvariable=self.dstr,
                             justify=LEFT, font=('Courier', 12))
        self.instructs.pack(side=TOP, fill=X)
        self.entry.pack(fill=X)
        self.searchb.pack(fill=X)
        self.text.pack()
        self.details.pack(fill=X, side=LEFT)
        self.store.pack(side=RIGHT, fill=Y)
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
        self.entry.after(100, self.search)

    def wide_search(self):
        self.listoffiles.delete(0, END)
        inp = str(self.tstr.get())
        filenames = self.lsting()
        if len(self.tstr.get()) > 0:
            for x in filenames:
                file = open(x, 'r').read()
                if inp[:2] == file[-2:]:
                    self.locks(inp)
                    if inp[3:] != ' ':
                        if inp[3:] in file[:-2]:
                            self.listoffiles.insert(END, x)
        self.finish = self.listoffiles.after(100, self.wide_search)

    def locks(self, inp):
        if inp[-1] == ' ':
            self.tstr.set(inp.rstrip(' ') + ';')
            self.entry.icursor(END)
        return

    def mode(self):
        if self.s.get() == 'Search Mode':
            self.tstr.set('Enter age then keys')
            self.instructs['text'] = 'Search Mode'
            self.s.set('Entry Mode')
            self.store['text'] = 'Load'
            self.store['command'] = self.load
            self.text.pack_forget()
            self.store.pack_forget()
            self.details.pack_forget()
            self.listoffiles.pack(fill=X, side=TOP)
            self.listoffiles.bind('<FocusIn>', lambda x: \
                                  self.root.after_cancel(self.finish))
            self.store.pack(side=RIGHT, fill=Y)
            self.wide_search()
            return
        if self.s.get() == 'Entry Mode':
            self.text.pack()
            self.listoffiles.pack_forget()
            self.s.set('Search Mode')
            self.instructs['text'] = 'Entry Mode'
            self.details.pack_forget()
            self.details.pack(fill=X, side=LEFT)
            self.tstr.set("Title of your 'Text'")
            return

    def storage(self):
        stream = open(self.tstr.get() + '.txt', 'w+')
        stream.write(self.text.get('0.0', END) + '\n'
                     + self.dstr.get()[-2:])
        stream.close()
        return

    def load(self):
        file = self.listoffiles.get(ACTIVE)

    def lsting(self):
        files = []
        for x in os.listdir('.'):
            if '.txt' in x:
                files.append(x)
        return files
ARI()
