import joblib
import numpy as np
import configparser
import os
import shutil

np.set_printoptions(threshold=np.inf)  # 去除省略号
shape_zeros = np.zeros(300,)  # 创建shape参数初始化
pose_zeros = np.zeros(72,)  # 创建shape参数初始化

# 建立一个存放ini文件的文件夹
make_path = 'ini_file'
if os.path.exists(make_path):
    pass
else:
    os.mkdir('ini_file')

print("\n# ---------------------读取.pkl文件---------------------")
pkl_path = 'vibe_output.pkl'
inf = joblib.load(pkl_path)
print(inf.keys())
for k, v in inf[1].items():
    print(k, np.shape(v))

print("\n# ---------------------从.pkl中提取shape和pose参数---------------------")
print("\n# 读取shape参数")
frame_id_num = len(inf[1]['pose'])  # 29
for frame_id in range(frame_id_num):
    print("\n# 读取第 %d 帧shape参数" % frame_id)
    shape_zeros[0:10] = inf[1]["betas"][frame_id]
    shape_str = str(shape_zeros)  # 仅读取第一帧
    shape_str = shape_str[1:-2]  # 去除中括号
    shape_line = shape_str.split()  # 将其分割成一个字符列表
    shape_new_line = ','.join(shape_line) # 将字符列表用','拼接成一个新字符串
    shape_new_line = shape_new_line.strip(',')  # 将新字符串尾部产生的','去掉
    shape = shape_new_line

    print("\n# 读取第 %d 帧pose参数" % frame_id)
    inf[1]["pose"][frame_id][0] = np.pi
    inf[1]["pose"][frame_id][1:3] = 0
    pose_str = str(inf[1]["pose"][frame_id])
    pose_str = pose_str[1:-2]
    pose_line = pose_str.split()
    pose_new_line = ','.join(pose_line)
    pose_new_line = pose_new_line.strip(',')
    pose = pose_new_line

    print("\n# ---------------------读取.ini文件---------------------")
    shutil.copyfile('rest_pose.ini', 'ini_file/frame_%d.ini' % frame_id)
    ini_path = 'rest_pose.ini'
    rest = configparser.ConfigParser()
    rest.read(ini_path, encoding='utf-8')
    sections = rest.sections()

    print("\n# 写入shape和pose参数")
    rest.set(sections[0], "shape", shape)
    rest.set(sections[0], "pose", pose)

    rest.write(open('ini_file/frame_%d.ini' % (frame_id), "r+", encoding="utf-8"))  # r+模式

# print("\n# ---------------------从.ini中导入shape和pose参数---------------------")
# r_shape = shape[0:10]
# r_pose = pose

print("已完成")
