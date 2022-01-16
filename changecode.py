import re
import tkinter as tk
from tkinter.filedialog import *
from tkinter.messagebox import *

import os
import json

def getVideoFilename():
    filepath = askopenfilename()  # 选择打开什么文件，返回文件名
    videoFilename.set(filepath)  # 设置变量filename的值
    print("videoFilename=",filepath)

def fileSave():
    outputFilePath = askdirectory()  # 选择目录，返回目录名
    savepath.set(outputFilePath)  # 设置变量outputpath的值
    print("savepath=",outputFilePath)


def tmpPath():
    tmpPath = askdirectory()  # 选择目录，返回目录名
    tmppath.set(tmpPath)  # 设置变量outputpath的值
    print("tmppath=",tmpPath)

def mergeFile():
    print("开始合并选择文件")
    print(videoFilename.get())

    videoFilename1=videoFilename.get().replace("/","//")
    audioFilename1 = audioFilename.get().replace("/", "//")
    savepath1 = savepath.get().replace("/", "//")
    cmd = "ffmpeg.exe -report -i " + videoFilename1 + " -i " + audioFilename1 + " -c copy " + savepath1 + "/output.mp4"
    print("cmd=",cmd)
    os.system(cmd)

def mergeFile1():
    print("开始简单合并")
    print(tmppath.get())

    videoFilename1=tmppath.get()+"/1/80/video.m4s"
    audioFilename1 = tmppath.get()+"/1/80/audio.m4s"
    savepath1 = "D:/bilibili/"
    jsonPath=tmppath.get()+"/1/entry.json"
    print("jsonPath=",jsonPath)
    tmpJson = json.load(open(jsonPath,'r',encoding='utf-8'))
    print("tmpJson=", tmpJson)
    title = tmpJson['title'].strip().replace(" ",'_')

    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    title = re.sub(rstr, "_", title)

    print("title",title)

    # 检查参数
    errormessage = "";
    if len(videoFilename1) == 0:
        showinfo("错误", "视频为空")
        return
    if not os.path.isfile(videoFilename1):
        showinfo("错误", "视频文件不存在")
        return
    if len(audioFilename1) == 0:
        showinfo("错误", "音频为空")
        return
    if not os.path.isfile(audioFilename1):
        showinfo("错误", "音频文件不存在")
        return

    if len(savepath1) == 0:
        showinfo("错误", "保存为空")
        return
    if not os.path.exists(savepath1):
        showinfo("错误", "保存路径不存在")
        return

    cmd = "ffmpeg.exe -report -i " + videoFilename1 + " -i " + audioFilename1 + " -c copy " + savepath1 + title + ".mp4"
    print("cmd=",cmd)
    os.system(cmd)


if __name__ == '__main__':
    root = tk.Tk()
    videoFilename = tk.StringVar()
    audioFilename = tk.StringVar()
    savepath = tk.StringVar()
    tmppath = tk.StringVar()


    # 选择存储的目录
    tk.Label(root, text='选择缓存的目录').grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=tmppath).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text='选择', command=tmpPath).grid(row=1, column=2, padx=5, pady=5)

    # 合并按钮
    tk.Button(root, text='简单合并', command=mergeFile1).grid(row=2, column=1, padx=5, pady=5)

    # 构建“选择文件”这一行的标签、输入框以及启动按钮，同时我们希望当用户选择图片之后能够显示原图的基本信息
    tk.Label(root, text='选择视频文件').grid(row=3, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=videoFilename).grid(row=3, column=1, padx=5, pady=5)
    tk.Button(root, text='打开', command=getVideoFilename).grid(row=3, column=2, padx=5, pady=5)

    # 构建“保存文件”这一行的标签、输入框以及启动按钮
    tk.Label(root, text='选择保存目录').grid(row=5, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=savepath).grid(row=5, column=1, padx=5, pady=5)
    tk.Button(root, text='选择', command=fileSave).grid(row=5, column=2, padx=5, pady=5)

    # 合并按钮
    tk.Button(root, text='高级合并', command=mergeFile).grid(row=6, column=1, padx=5, pady=5)



    root.mainloop()
