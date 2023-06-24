# -*- coding: utf-8 -*-
# @Time    : 2023/6/12 21:04
# @Author  : 宋楚嘉
# @FileName: process_soil.py
# @Software: PyCharm
# @Blog    ：https://github.com/Polumm

from tifffile import imread
import numpy as np
import pandas as pd
from scipy import ndimage
from scipy import stats

# ***选择填补参数***
# 1、填充H_T_USDA
fill_index = 'H_T_USDA'
# 2、填充H_S_USDA
# fill_index = 'H_S_USDA'

# 读取soil关键像元位置，构建numpy矩阵
soil_code = imread('data/point_position.tif').astype(np.int32)
# 现在，'image'是一个包含土壤矩阵数据的NumPy数组。
print(soil_code.shape)
# 读取CSV文件，将'#N/A'视为缺失值，然后将缺失值替换为0
data = pd.read_csv('data\data_origin.csv', na_values='#N/A').fillna(0)

# 保留原始土壤矩阵
soil_value = np.copy(soil_code)

# 遍历data中的每一行
for index, row in data.iterrows():
    # 找到土壤矩阵中等于GRID值的像素，并将其替换为H_T_USDA或者H_S_USDA的值
    soil_value[soil_value == row['GRID']] = row[fill_index].astype(np.int32)
    # image[image == row['GRID']] = row['H_S_USDA'].astype(np.int32)


# 去除点转栅格造成的间隙
rows_to_delete = np.all(soil_value == -1, axis=1)
cols_to_delete = np.all(soil_value == -1, axis=0)
# 删除这些行和列
soil_value = soil_value[~rows_to_delete, :]
soil_value = soil_value[:, ~cols_to_delete]
# 将numpy数组保存为CSV文件，确保保存的是整形数据
np.savetxt('soil_code_origin_' + fill_index + '.csv', soil_code.astype(np.int32), delimiter=',', fmt='%i')

# 创建过滤器函数
def filter_func(values):
    center = values[len(values) // 2]
    # 如果中心像素是0，则返回窗口像素中非-1的众数
    if center == 0:
        mode = stats.mode(values[values != -1], keepdims=True)[0][0]
        return mode
    # 否则返回中心像素的值
    else:
        return center



# 创建一个新的土壤矩阵用于保存结果
new_soil_value = np.copy(soil_value)
# 初始化窗口大小
n = 3

while True:  # 外层迭代，若无法填充则逐步扩大窗口大小
    # 初始化一个变量来跟踪迭代的次数
    iteration = 0
    # 初始化一个变量来跟踪上一次迭代的土壤矩阵
    last_image = np.copy(new_soil_value)

    while True:  # 内层迭代，对当前窗口大小进行填充
        # 使用generic_filter函数应用过滤器
        new_soil_value = ndimage.generic_filter(new_soil_value, filter_func, size=n)
        iteration += 1
        print(f"Iteration {iteration} with window size {n}")
        # 如果土壤矩阵没有变化，或者已经执行了100次迭代，则跳出循环
        if np.array_equal(new_soil_value, last_image) or iteration >= 100:
            break
        # 否则，将当前的土壤矩阵保存为上一次迭代的土壤矩阵
        last_image = np.copy(new_soil_value)

    # 如果土壤矩阵中仍有0，增大窗口并继续外部循环
    if np.any(new_soil_value == 0):
        n += 2  # 窗口大小增加
    else:
        break  # 如果土壤矩阵中没有0了，就跳出外部循环

# 将numpy数组保存为CSV文件，确保保存的是整形数据
np.savetxt('filled_soil_value_' + fill_index + '.csv', new_soil_value.astype(np.int32), delimiter=',', fmt='%i')

# 找到所有非-1的像素
non_minus_one_pixels = new_soil_value[soil_value != -1]
# 将这些像素转换为一维数组
column = non_minus_one_pixels.flatten()
# 将numpy数组保存为CSV文件，确保保存的是整形数据
np.savetxt('flatten_filled_soil_value_' + fill_index + '.csv', column.astype(np.int32), delimiter=',', fmt='%i')
