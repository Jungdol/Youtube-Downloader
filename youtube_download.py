from tkinter import *
from tkinter import filedialog

from pytube import YouTube
from pytube import Playlist
from pytube.exceptions import RegexMatchError

import webbrowser
import pandas as pd

import pytube_download as pydown

placeholder = '유튜브 링크'
res_placeholder = 'resolution: high, 1440p, 1080p, 720p 480p ...'

win = Tk()
win.title('Youtube Downloader')

single = False
multi = False
is_download = False

download_path = ""
excel_path = ""
download_state = StringVar()


def download_complete():
    global download_state, is_download

    if is_download == False:
        complete = Label(win, textvariable=download_state)
        complete.pack()
        is_download = True


def download_dir():
    global download_path
    download_path = filedialog.askdirectory(
        initialdir="path",
        title="select download path")

    if download_path != '':
        download_dir_label = Label(text=download_path)
        download_dir_label.pack()
        single_btn.pack(pady=5)
        multi_btn.pack(pady=5)


def window_center():
    w = 700
    h = 325

    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()

    x = (sw - w)/2
    y = (sh - h-200)/2

    win.geometry('%dx%d+%d+%d' % (w, h, x, y))
    win.resizable(False, False)


def single_download():
    global single, multi, excel_dir_label, single_down_btn, multi_down_btn
    if not single:
        single = True
        multi = False

        if single_ent.get() != placeholder:
            single_ent.insert(0, placeholder)

        single_ent.pack(side="top", fill="x", padx=200, pady=25)
        multi_setting_btn.pack_forget()
        excel_dir_label.pack_forget()
        multi_down_btn.pack_forget()

        def clear(event):
            if single_ent.get() == placeholder:
                single_ent.delete(0, len(single_ent.get()))

        single_ent.bind("<Button-1>", clear)

        def pytube_single_download():
            def link_error(out=''):
                out += '유튜브 링크를 입력해주세요.'
                print(out)
                download_state.set(out)

            if single_ent.get() != '':
                try:
                    if single_ent.get().find('playlist') != -1:
                        p = Playlist(single_ent.get())
                        for video in p.videos:
                            download_state.set(pydown.pytube_down(video, resolution_ent.get(), download_path))
                    else:
                        video = YouTube(single_ent.get())
                        download_state.set(pydown.pytube_down(video, resolution_ent.get(), download_path))
                except RegexMatchError:
                    link_error('올바른 ')
            else:
                link_error()

        single_down_btn = Button(win, text="다운로드", command=pytube_single_download)
        single_down_btn.pack()
        download_complete()


def multi_download():
    global single, multi, excel_path,single_down_btn , multi_down_btn
    if not multi:
        multi = True
        single = False

        multi_setting_btn.pack(pady=25)
        single_ent.pack_forget()
        single_down_btn.pack_forget()

        def pytube_multi_download():
            data_pd = pd.read_excel(excel_path, sheet_name=0).fillna('')
            links = data_pd['링크'].values.tolist()

            for i in range(len(links)):
                video = YouTube(links[i])
                download_state.set(pydown.pytube_down(video, resolution_ent.get(), download_path, f'top_{i+1}.mp4'))

        def excel_dir():
            global excel_path, excel_dir_label, multi_down_btn
            excel_path = filedialog.askopenfilename(
                initialdir="path",
                title="select Java path",
                filetypes=[("excel", "*xlsx"),
                           ("all files", "*.*")])

            if excel_path != '':
                excel_dir_label = Label(text=excel_path)
                excel_dir_label.pack()

                multi_down_btn = Button(win, text="다운로드", command=pytube_multi_download)
                multi_down_btn.pack()
                download_complete()

        multi_setting_btn.config(text="엑셀 경로 지정", command=excel_dir)


window_center()

resolution_ent = Entry(win)
resolution_ent.insert(0, res_placeholder)


def clear(event):
    if resolution_ent.get() == res_placeholder:
        resolution_ent.delete(0, len(resolution_ent.get()))


resolution_ent.bind("<Button-1>", clear)

resolution_ent.pack(ipadx=50)

download_dir_btn = Button(win, text="저장 경로 지정", command=download_dir).pack()

single_ent = Entry(win)
multi_setting_btn = Button(win)

single_down_btn = Button(win)
multi_down_btn = Button(win)

single_btn = Button(win, text="링크 다운로드", overrelief="solid", width=15, command=single_download, repeatdelay=1000, repeatinterval=100)
multi_btn = Button(win, text="엑셀 파일 다운로드", overrelief="solid", width=15, command=multi_download, repeatdelay=1000, repeatinterval=100)

excel_dir_label = Label(text=excel_path)


def github_link():
    webbrowser.open_new(r"https://github.com/Jungdol")


developer_btn = Button(text='Developer Github', command=github_link).pack(side='bottom')
developer_label = Label(text='Developer: Jungdol').pack(side='bottom')

win.mainloop()