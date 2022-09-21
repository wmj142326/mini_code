# -*- coding: utf-8 -*-
# @Time : 2022/9/21
# @Author : wmj
# @Email : wmj142326@163.com
# @File : video_gap_img.py
# @Note : 将视频按间隔提取帧
# ---------------------------
# -*- coding:utf-8 -*-
import cv2
import os


def main():
    video_src_path = "videos"  # 保存视频的文件夹
    image_save_path = "images"  # 输出图片的文件夹
    frame_gap = 10  # 每隔10帧读取一帧
    end_with_video = [".mp4", ".avi"]  # 要抽帧的视频后缀
    end_with_img = ".jpg"  # 要保存的图片格式
    file_tree = True  # 是否保留原有视频文件结构

    video_gap_img(video_src_path, image_save_path, frame_gap, end_with_video, end_with_img, file_tree)


# 获取路径下所有相同后缀名文件
def Re_file(input_path, out_list, end_with=[]):
    """
    :param input_path: files root path.
    :param out_list: [].
    :param end_with: file extension ->list.
    :return: out list of file path.
    """
    for i in os.listdir(input_path):
        i = os.path.join(input_path, i)
        if os.path.isfile(i):
            for j in range(len(end_with)):
                if os.path.splitext(i)[1] == end_with[j]:
                    out_list.append(i)
        else:
            Re_file(i, out_list, end_with)
    return out_list


# 视频间隔抽帧
def video_gap_img(video_src_path,
                  image_save_path,
                  frame_gap,
                  end_with_video=[],
                  end_with_img=".jpg",
                  file_tree=False):
    """
    :param video_src_path: video_files root path.
    :param image_save_path: img_output save path.
    :param frame_gap: The gap of video extraction.
    :param end_with_video: video_file extension ->list[].
    :param end_with_img: image_file extension.
    :param file_tree: Whether to keep the original video structure.
    """
    out_list = []
    videos = Re_file(video_src_path, out_list, end_with=end_with_video)

    for each_video_idx, each_video in enumerate(videos):
        each_video_name, _ = each_video.split('.')
        if file_tree:
            each_img_file = each_video_name.replace(each_video_name.split("/")[0], image_save_path)
        else:
            each_img_file = os.path.join(image_save_path, each_video_name.split("/")[-1])
        if not os.path.exists(each_img_file):
            os.makedirs(each_img_file)

        cap = cv2.VideoCapture(each_video)

        if cap.isOpened():
            print('open video succeeded')
        else:
            print('open video failed')

        count = 0  # 统计帧数
        success = True
        i = 0
        # 每隔10帧读取一帧
        while (success):
            success, frame = cap.read()
            i = i + 1
            if i == frame_gap:  # 每个10帧读取第10帧
                img_name = each_img_file.split("/")[-1] + '_{}{}'.format(count, end_with_img)
                print("[{}/{}]".format(each_video_idx + 1, len(videos)),
                      each_video, "-->", img_name)
                params = []
                params.append(int(cv2.IMWRITE_JPEG_QUALITY))
                params.append(95)
                cv2.imwrite(os.path.join(each_img_file, img_name), frame, params)
                count = count + 1
                i = 0

        cap.release()


if __name__ == "__main__":
    main()
    print("finished!")
