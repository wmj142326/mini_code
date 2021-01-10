import os
import json

# 选出.json文件
dir_path = "C:/Users/王美军/Desktop/road2021/road2021_wmj"
json_path = []
jpg_path = []
dir_path_list = os.listdir(dir_path)  # 返回指定路径下的文件和文件夹列表
for item in dir_path_list:
    filepath = os.path.join(dir_path, item)
    if os.path.isfile(filepath):
        (filename, extension) = os.path.splitext(filepath)
        if extension == ".json":
            json_path.append(filepath)
        if extension == ".jpg":
            jpg_path.append(filepath)
json_num = len(json_path)  # 图片数量
jpg_unm = len(jpg_path)  # json文件数量


# 计算各个标注数目
num_D00 = 0
num_D10 = 0
num_D20 = 0
num_D30 = 0
num_D40 = 0

for file in json_path:
    with open(file, "r") as f:
        json_line = f.read()

    your_dict = json.loads(json_line)
    firs_tkey = your_dict.get("shapes")
    second_key = str(firs_tkey)

    D00 = second_key.count("D00")
    D10 = second_key.count("D10")
    D20 = second_key.count("D20")
    D30 = second_key.count("D30")
    D40 = second_key.count("D40")

    num_D00 += D00
    num_D10 += D10
    num_D20 += D20
    num_D30 += D30
    num_D40 += D40

    num_all = num_D00 + num_D10 + num_D20 + num_D30 + num_D40

    rate_D00 = num_D00/num_all
    rate_D10 = num_D10/num_all
    rate_D20 = num_D20/num_all
    rate_D30 = num_D30/num_all
    rate_D40 = num_D40/num_all

print("\n共有{}张图片，{}个json文件，\n标注框{}个，其中：".format(jpg_unm, json_num, num_all))
print('\n纵向裂缝 D00: ', num_D00, "占比{:.2%}".format(rate_D00),
      '\n横向裂缝 D10: ', num_D10, "占比{:.2%}".format(rate_D10),
      '\n龟裂    D20: ', num_D20, "占比{:.2%}".format(rate_D20),
      '\n其他    D30: ', num_D30, "  占比{:.2%}".format(rate_D30),
      '\n坑洞    D40: ', num_D40, " 占比{:.2%}".format(rate_D40))