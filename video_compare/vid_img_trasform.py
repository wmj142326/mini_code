# -*- coding: utf-8 -*-
# @Time : 2022/7/26
# @Author : wmj
# @Email : wmj142326@163.com
# @File : vid_img_trasform.py
# @Note : 图片和视频相互转换
# ---------------------------
import os
import cv2
import subprocess
import os.path as osp


def images_to_video(img_folder, output_vid_file):
    os.makedirs(img_folder, exist_ok=True)
    print("\n")
    print(f'Saving result video to {output_vid_file}')
    command = [
        'ffmpeg', '-y', '-threads', '16', '-i', f'{img_folder}/%06d.jpg', '-profile:v', 'baseline',
        '-level', '3.0', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-an', '-v', 'error', output_vid_file,
    ]

    print(f'Running \"{" ".join(command)}\"')
    subprocess.call(command)


def video_to_images(vid_file, img_folder=None, return_info=False, output_folder=None):
    if img_folder is None:
        img_folder = osp.join(output_folder,
                              osp.basename(vid_file).replace('.mp4', ''), 'frames')

        vid_name = osp.basename(vid_file).replace('.mp4', '')

    os.makedirs(img_folder, exist_ok=True)

    command = ['ffmpeg',
               '-i', vid_file,
               '-f', 'image2',
               '-v', 'error',
               f'{img_folder}/%06d.png']
    print(f'Running \"{" ".join(command)}\"')
    subprocess.call(command)

    print(f'Images saved to \"{img_folder}\"')

    img_shape = cv2.imread(osp.join(img_folder, '000001.png')).shape

    if return_info:
        return img_folder, len(os.listdir(img_folder)), img_shape
    else:
        return img_folder


def main():
    pass


if __name__ == "__main__":
    main()
    print("finished!")
