# -*- coding = utf-8 -*-
# @time:2021/3/8 23:47
# Author:wmj
# @File:R2E.py
# @Software:PyCharm
# @Function:旋转矩阵与欧拉角转换
# 在摄影测量学科中，国际摄影测量遵循OPK系统，即是xyz转角系统，而工业中往往使用zyx转角系统。
# 旋转矩阵的意义：描述相对地面的旋转情况，yaw-pitch-roll对应zyx对应k,p,w

import cv2
import numpy as np
import math
import random


def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6  # 判断R是否奇异


def rotationMatrixToEulerAngles(R):
    assert (isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


def eulerAnglesToRotationMatrix(theta):
    R_x = np.array([[1, 0, 0],
                    [0, math.cos(theta[0]), -math.sin(theta[0])],
                    [0, math.sin(theta[0]), math.cos(theta[0])]
                    ])

    R_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1])],
                    [0, 1, 0],
                    [-math.sin(theta[1]), 0, math.cos(theta[1])]
                    ])

    R_z = np.array([[math.cos(theta[2]), -math.sin(theta[2]), 0],
                    [math.sin(theta[2]), math.cos(theta[2]), 0],
                    [0, 0, 1]
                    ])

    R = np.dot(R_x, np.dot(R_y, R_z))

    return R


if __name__ == '__main__':
    e = np.random.rand(3) * math.pi * 2 - math.pi
    R = eulerAnglesToRotationMatrix(e)  # 旋转矩阵：R = ？

    e1 = rotationMatrixToEulerAngles(R)  # 转化结果
    R1 = eulerAnglesToRotationMatrix(e1)

    print("\nInput Euler angles :\n{0}".format(e))
    print("\nR :\n{0}".format(R))
    print("\nOutput Euler angles :\n{0}".format(e1))
    print("\nR1 :\n{0}".format(R1))
