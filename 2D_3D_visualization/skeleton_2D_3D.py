# -*- coding: utf-8 -*-
"""
@Time ： 2023/6/18 下午2:29
@Auth ： 陌尘小小
@File ：skeleton_2D_3D.py
@EMAIL ：wmj142326@163.com
@Note： 关键点骨骼绘制与可视化
"""

import os.path
import cv2
import numpy as np
import matplotlib.pyplot as plt


def visualization2d(j2d, skeleton, img, color_point=(0, 0, 255), color_skeleton=(0, 255, 0)):
    skeleton = np.array(skeleton)

    for i in range(len(j2d)):
        cv2.circle(img, (int(j2d[i][0]), int(j2d[i][1])), 3, color_point, -1)
        cv2.putText(img, str(i), (int(j2d[i][0]), int(j2d[i][1])), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
    for pair in skeleton:
        partA = pair[0]
        partB = pair[1]
        if (j2d[partA]).any() and (j2d[partB]).any():
            cv2.line(img, (int(j2d[partA][0]), int(j2d[partA][1])),
                     (int(j2d[partB][0]), int(j2d[partB][1])), color_skeleton, 1)

    return img


def visualization3d(j3d, skeleton, color_point='blue', color_skeleton='red'):
    coordinates = np.array(j3d)
    skeleton = np.array(skeleton)

    # 创建一个图形对象
    fig = plt.figure()
    # 创建一个三维坐标轴
    ax3D = fig.add_subplot(111, projection='3d')

    # 提取X、Y和Z坐标
    X = coordinates[:, 0]
    Y = coordinates[:, 1]
    Z = coordinates[:, 2]

    # 绘制关节点
    ax3D.scatter(X, Y, Z, color=color_point)
    for i in range(len(j3d)):
        ax3D.text(X[i], Y[i], Z[i], str(i))
    # 绘制骨架
    for skel in skeleton:
        x_skel = [coordinates[skel[0], 0], coordinates[skel[1], 0]]
        y_skel = [coordinates[skel[0], 1], coordinates[skel[1], 1]]
        z_skel = [coordinates[skel[0], 2], coordinates[skel[1], 2]]
        ax3D.plot(x_skel, y_skel, z_skel, color=color_skeleton)

    # 设置坐标轴标签
    ax3D.set_xlabel('X')
    ax3D.set_ylabel('Y')
    ax3D.set_zlabel('Z')
    ax3D.set_xticklabels([])
    ax3D.set_yticklabels([])
    ax3D.set_zticklabels([])

    return fig


def main():
    joint_3d = [[724.77026, 288.7396, 26.478497],
                [721.19275, 360.58636, 29.028776],
                [679.1147, 361.42322, 29.762249],
                [613.02795, 363.6459, 32.28158],
                [540.773, 364.15228, 28.764874],
                [763.73346, 359.8205, 28.988762],
                [803.6927, 366.88297, 24.546938],
                [828.0679, 371.67868, 20.280685],
                [698.81616, 492.36417, 31.815529],
                [698.755, 587.3082, 32.55538],
                [693.98846, 670.7277, 33.58216],
                [749.7504, 489.57004, 31.85844],
                [750.3075, 589.11285, 31.89966],
                [742.4283, 670.9277, 32.639297],
                [724.20953, 492.15393, 32.],
                [721.70044, 423.42517, 32.026024],
                [722.7298, 333.2311, 27.22057],
                [519.70184, 368.29916, 27.29874],
                [836.64685, 374.86874, 17.843727],
                [671.773, 689.5878, 30.834776],
                [751.82715, 695.18945, 28.92236]]
    joint_2d = np.array(joint_3d)[:, :2]
    skeleton = [[0, 16], [16, 1], [1, 15], [15, 14], [14, 8], [14, 11], [8, 9], [9, 10], [10, 19], [11, 12], [12, 13],
                [13, 20], [1, 2], [2, 3], [3, 4], [4, 17], [1, 5], [5, 6], [6, 7], [7, 18]]

    img = cv2.imread("data/test.jpg")

    result_2d = visualization2d(joint_2d, skeleton, img)

    result_3d = visualization3d(joint_3d, skeleton)
    plt.show()
    cv2.imshow('frame', result_2d)
    cv2.waitKey()


if __name__ == '__main__':
    main()
