import cv2
import time

def main():
    interval = 1  # 捕获图像的间隔，单位：秒
    num_frames = 20  # 捕获图像的总帧数

    timeF = 2400  # 视频帧计数间隔
    keys_frame = 0  # 设置起始帧率

    out_fps = 30  # 输出文件的帧率

    ask = input("本地摄像头请输入 a，USB摄像头请输入 b，本地视频请输入 c:")
    path = Camera_Or_Video(ask)
    cap, video = Set_Config(ask, path, out_fps)

    if ask == 'a' or 'b':
        Camera_Output(cap, video, num_frames, interval)
    else:
        Video_Output(cap, video, keys_frame, timeF)

    release(cap, video)


# 选择视频获取方式
def Camera_Or_Video(ask):
    if ask == 'a':
        option = 0
        return option
    if ask == 'b':
        option = 1
        return option
    elif ask == 'c':
        option = input("please input the dir：")
        return option
    else:
        print("error")

# 设置视频的格式等相关参数
def Set_Config(ask,option, out_fps):
    if ask != 'c':
        cap = cv2.VideoCapture(option, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(option)
    # 获取捕获的分辨率
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # 设置要保存视频的编码，分辨率和帧率
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(
        "E:/P_V/video/time_lapse.mp4",
        fourcc,
        out_fps,
        size)
    return cap, video

# 对本地视频输出处理
def Video_Output(cap,video,keys_frame,timeF):
    if cap.isOpened():  # 判断是否正常打开
        print("视频工作正常，即将开始：")
        rval, frame = cap.read()
    else:
        print("视频工作异常，请检查：")
        rval = False
    while rval:
        cap.set(cv2.CAP_PROP_POS_FRAMES, keys_frame)
        rval, frame = cap.read()
        video.write(frame)
        keys_frame += timeF

        # 显示摄像头画面
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("Over!")
    return

# 对摄像头视频输出处理
def Camera_Output(cap,video,num_frames,interval):
    if cap.isOpened():  # 判断是否正常打开
        print("相机工作正常，即将开始：")
    else:
        print("相机异常！！，请检查！！")

    for i in range(4):
        cap.read()

    # 开始捕获，通过read()函数获取捕获的帧
    try:
        for i in range(num_frames):
            ret, frame = cap.read()
            video.write(frame)

            # 如果希望把每一帧也存成文件，比如制作GIF，则取消下面的注释
            # filename = '{:0>6d}.png'.format(i)
            # cv2.imwrite(filename, frame)

            print('Frame {} is captured.'.format(i))
            time.sleep(interval)

            # 显示摄像头画面
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print("Over!")
    except KeyboardInterrupt:
        # 提前停止捕获
        print('Stopped! {}/{} frames captured!'.format(i, num_frames))
    return


# 释放资源
def release(cap,video):
    video.release()
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()


# 'E:/P_V/video/pro.mp4'