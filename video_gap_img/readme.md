1.将要抽帧的多个视频放于video文件夹下；

2.修改抽帧间隔：
```csharp
    video_src_path = "videos"  # 保存视频的文件夹
    image_save_path = "images"  # 输出图片的文件夹
    frame_gap = 10  # 每隔10帧读取一帧
    end_with_video = [".mp4", ".avi"]  # 要抽帧的视频后缀
    end_with_img = ".jpg"  # 要保存的图片格式
    file_tree = True  # 是否保留原有视频文件结构, 默认为False
```

3.img文件夹将生成视频名的图像文件夹,按照原本文件路径

4.过程：
    遍历videos下所有指定格式视频文件；
    获得每个视频文件相对路径
    将每个视频gap抽帧
    保存路径，以视频名为图片文件夹最小单位
  
5.测试视频来源：[MPI-INF-3DHP数据集](https://paperswithcode.com/dataset/mpi-inf-3dhp)
