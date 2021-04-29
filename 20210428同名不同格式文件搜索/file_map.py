# # -*- coding = utf-8 -*-
# # @time:2021/4/28 17:21
# # Author:wmj
# # @File:file_map.py
# # @Software:PyCharm
# # @Function:根据挑选的jpg文件找出对应的xml、json、shp、dbf、shx文件
import os
import shutil

filepath1 = "C:\\Users\\王美军\\Desktop\\Czech\\images"  # 源文件做参考
filepath2 = "G:\\项目备份\\20210427_道路病害标注项目\\road2020\\train\\Czech\\labels"  # 需要拷出的文件位置
filepath3 = filepath2+"_copy"      # 拷入新的文件夹

if os.path.exists(filepath3):
    pass
else:
    os.mkdir(filepath3)

file_list_1 = os.listdir(filepath1)
file_list_2 = os.listdir(filepath2)

aa, bb = os.path.splitext(file_list_2[0])


def main():
    n = 0
    for file in os.listdir(filepath1):
        filename, extension = os.path.splitext(file)
        map_fil = filename + bb
        if map_fil in file_list_2:
            srcfile = os.path.join(filepath2, map_fil)
            dstfile = os.path.join(filepath3, map_fil)
            # shutil.move(srcfile, dstfile)#剪切功能
            shutil.copyfile(srcfile, dstfile) # 拷贝出来
            n = n+1
            print("已完成:  %d / %d" % (n, len(file_list_1)))


if __name__ == '__main__':
    main()
