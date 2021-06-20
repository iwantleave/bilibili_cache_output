# bilibili_cache_output Bilibili缓存视频合并
bilibili的缓存视频，单独视频文件video.m4s与音频文件audio.m4s，这个python代码调用ffmpeg，把视频与音频文件合成一个mp4文件。

简单合并功能：选择bilibli的缓存文件夹，合并视频文件。

高级合并功能：手动选择视频与音频文件和导出文件位置，合并视频文件。

前提，在ffmpeg网站（ http://www.ffmpeg.org/download.html ）下载ffmpeg，与py文件放在一起，并设置合适的导出文件存储路径

依赖ffmpeg做视频合并，并不做重新编码，处理速度非常快。

代码不依赖第三方库，尽管没有测试，以我浅薄的认识，可以支持windows、linux、macos上运行。
