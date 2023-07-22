# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/22 下午9:12
@Auth ： 陌尘小小
@File ：wget_download.py
@EMAIL ：wmj142326@163.com
@Note：wget自动下载文件脚本
"""

import os
import subprocess


def download_url(url, outdir):
    print(f'Downloading files from {url}')
    cmd = ['wget', '-c', url, '-P', outdir]
    subprocess.call(cmd)


if __name__ == '__main__':
    url = 'https://pjreddie.com/media/files/yolov3.weights'
    outdir = os.path.dirname('./my/models/yolov3.weights')
    os.makedirs(outdir, exist_ok=True)
    download_url(url, outdir)
