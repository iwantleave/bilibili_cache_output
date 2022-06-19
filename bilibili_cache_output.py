import re
import tkinter as tk
from tkinter.filedialog import *
from tkinter.messagebox import *

import os
import json


def getVideoFilename():
    filepath = askopenfilename()  # 选择打开什么文件，返回文件名
    videoFilename.set(filepath)  # 设置变量filename的值
    print("videoFilename=", filepath)


def getAudioFilename():
    filepath = askopenfilename()  # 选择目录，返回目录名
    audioFilename.set(filepath)  # 设置变量outputpath的值
    print("audioFilename=", filepath)


def fileSave():
    outputFilePath = askdirectory()  # 选择目录，返回目录名
    savepath.set(outputFilePath)  # 设置变量outputpath的值
    print("savepath=", outputFilePath)


def getVideoPath():
    selectedPath = askdirectory(initialdir=tmppath.get())  # 选择目录，返回目录名
    print("selectedPath=", selectedPath)
    if(len(selectedPath)>0):
        tmppath.set(selectedPath)  # 设置变量outputpath的值


def mergeFile():
    print("开始合并选择文件")
    print(videoFilename.get())

    videoFilename1 = videoFilename.get().replace("/", "//")
    audioFilename1 = audioFilename.get().replace("/", "//")
    savepath1 = savepath.get().replace("/", "//")
    cmd = "ffmpeg.exe -report -i " + videoFilename1 + " -i " + audioFilename1 + " -c copy " + savepath1 + "/output.mp4"
    print("cmd=", cmd)
    os.system(cmd)


def doJob(mergePath, savepath,jobCnt, totalFileCnt):
    jsonPath = mergePath + "/entry.json"
    print("jsonPath=", jsonPath)
    entryJson = json.load(open(jsonPath, 'r', encoding='utf-8'))
    print("entryJson=", entryJson)
    title = entryJson['title'].strip().replace(" ", '_')
    type_tag = entryJson['type_tag'].strip()
    bvid = entryJson['bvid'].strip()
    owner_id = str(entryJson['owner_id'])
    print("type_tag=", type_tag, "bvid=", bvid, "owner_id=", owner_id)

    # 获取文件路径
    inputVideoFilename = mergePath + "/" + type_tag + "/video.m4s"
    inputAudioFilename = mergePath + "/" + type_tag + "/audio.m4s"

    # 处理不合适的字符
    rstr = r"[\/\\\:\*\?\"\<\>\|&]"  # '/ \ : * ? " < > | &'
    title = re.sub(rstr, "_", title)
    title = title.replace("《", "_").replace("》", "_").replace("【", "_").replace("】", "_") \
        .replace("__","_").strip("_") #去掉书名号《》【】

    print("title", title)

    # 输出文件格式 文件名_bvid_ownerid.mp4
    outputFileName=""
    if totalFileCnt==1:
        outputFileName = savepath + title + "_" + bvid + "_" + owner_id + ".mp4"
    elif totalFileCnt>1:
        outputFileName = savepath + title + "_" + bvid + "_" + owner_id + "_" + str(jobCnt) + ".mp4"

    # 检查参数
    errormessage = ""
    if len(inputVideoFilename) == 0:
        print("错误，视频为空！")
        showwarning("错误", "视频为空")
        return
    if not os.path.isfile(inputVideoFilename):
        print("错误，视频文件不存在！")
        showwarning("错误", "视频文件不存在")
        return
    if len(inputAudioFilename) == 0:
        print("错误，音频为空！")
        showwarning("错误", "音频为空")
        return
    if not os.path.isfile(inputAudioFilename):
        print("错误，音频文件不存在！")
        showwarning("错误", "音频文件不存在")
        return

    if len(savepath) == 0:
        print("错误，保存路径为空！")
        showwarning("错误", "保存路径为空")
        return
    if not os.path.exists(savepath):
        print("错误，保存路径不存在！")
        showwarning("错误", "保存路径不存在")
        return
    if os.path.isfile(outputFileName):
        print("错误，输出视频文件已存在！")
        showwarning("错误", "输出视频文件已存在")
        return

    cmd = "ffmpeg.exe -report -i " + inputVideoFilename + " -i " + inputAudioFilename + " -c copy " + outputFileName
    print("cmd=", cmd)
    if os.system(cmd) == 0:
        print("合并完成！")
        showinfo(title="成功", message="合并完成！" + outputFileName)
    else:
        print("合并失败！")
        showerror(title="失败", message="合并失败！")


def SimpleMergeFile():
    print("开始简单合并")
    print("tmppath=", tmppath.get())

    savePath = "D:/bilibili/"
    tmppathList = os.listdir(tmppath.get())
    totalFileCnt = len(tmppathList)
    jobCnt = 0
    for i in tmppathList:
        mergePath=tmppath.get()+"/"+i
        print("处理路径"+mergePath)
        jobCnt=jobCnt+1
        doJob(mergePath, savePath,jobCnt, totalFileCnt)





def startApp():
    pass


if __name__ == '__main__':
    root = tk.Tk()
    videoPath="D:/bilibli"
    videoFilename = tk.StringVar()
    audioFilename = tk.StringVar()
    savepath = tk.StringVar()
    tmppath = tk.StringVar()

    root.title('B站工具')
    root.geometry('500x400')

    tmppath.set(videoPath)

    # 选择存储的目录
    tk.Label(root, text='选择缓存的目录').grid(row=1, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=tmppath).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text='选择', command=getVideoPath).grid(row=1, column=2, padx=5, pady=5)

    # 合并按钮
    tk.Button(root, text='简单合并', command=SimpleMergeFile).grid(row=2, column=1, padx=5, pady=5)

    # 构建“选择文件”这一行的标签、输入框以及启动按钮，同时我们希望当用户选择图片之后能够显示原图的基本信息
    tk.Label(root, text='选择视频文件').grid(row=3, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=videoFilename).grid(row=3, column=1, padx=5, pady=5)
    tk.Button(root, text='打开', command=getVideoFilename).grid(row=3, column=2, padx=5, pady=5)

    tk.Label(root, text='选择音频文件').grid(row=4, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=audioFilename).grid(row=4, column=1, padx=5, pady=5)
    tk.Button(root, text='打开', command=getAudioFilename).grid(row=4, column=2, padx=5, pady=5)

    # 构建“保存文件”这一行的标签、输入框以及启动按钮
    tk.Label(root, text='选择保存目录').grid(row=5, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=savepath).grid(row=5, column=1, padx=5, pady=5)
    tk.Button(root, text='选择', command=fileSave).grid(row=5, column=2, padx=5, pady=5)

    # 合并按钮
    tk.Button(root, text='高级合并', command=mergeFile).grid(row=6, column=1, padx=5, pady=5)

    tk.Text(root, height=10).grid(row=7, column=0, columnspan=24,padx=5, pady=5)

    root.mainloop()
