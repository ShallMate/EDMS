import csv

from Crypto.Cipher import AES
import base64
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import num_tree
from attribute_tree import AgeTree
from tool import get_feature, get_age_dict, get_diag_dict, get_num_dict


def get_attrkeyword(path):
    df = pd.read_csv(path)
    keyword = []
    all_keyword = []
    dicts = {}
    index = 0
    for key in get_feature(path):
        list = ['age', 'diag_1', 'diag_2', 'rand1', 'rand2', 'rand3', 'rand4','rand5','rand6']
        if key in list:
            all_key = df[key].drop_duplicates().values.tolist()  # 获取数据并去重
            all_key = sorted(all_key)
            all_keyword = all_keyword + all_key
            continue
        keyword1 = df[key].drop_duplicates().values.tolist()  # 获取数据并去重
        keyword1 = sorted(keyword1)
        sort_dict = {}
        for key_dict in keyword1:
            sort_dict1 = {key_dict: index}
            index = index + 1
            sort_dict.update(sort_dict1)
        dict1 = {key: sort_dict}
        # dicts = dict(dicts, **dict1)
        dicts.update(dict1)
        keyword = keyword + keyword1
        all_keyword = all_keyword + keyword1
    return all_keyword, keyword, dicts


def get_attrvect(df):
    age_dict = get_age_dict()
    diag_dict = get_diag_dict()
    num_dict = get_num_dict()
    raw_convert_data = np.array(df)
    f = raw_convert_data[:, 3:44]
    age_list = raw_convert_data[:, 0]  # age
    diag_list = raw_convert_data[:, 1:3]  # diag列
    num_list = raw_convert_data[:, 44:]
    model_enc = OneHotEncoder()  # 建立标志转换模型对象（也称为哑编码对象）
    df_new2 = model_enc.fit_transform(f).toarray().astype(int)  # 标志转换
    vect_x = len(df_new2)  # 记录个数
    vect_y = len(df_new2[0]) + 2 * len(diag_dict[0]) + len(age_dict[0]) + 1 * len(num_dict[0])  # 向量维度
    df_vect = np.zeros((vect_x, vect_y), dtype=int)

    for i, vect in enumerate(df_new2):
        age = age_list[i]
        age_vect = age_dict[age]
        diag1 = diag_list[i][0]
        diag2 = diag_list[i][1]
        diag1_vect = diag_dict[diag1]
        diag2_vect = diag_dict[diag2]
        rand1 = num_list[i][0]
        rand1_vect = num_dict[rand1]
        vect = np.concatenate((age_vect, diag1_vect, diag2_vect, rand1_vect, vect),
                              axis=0)
        df_vect[i] = vect
    return df_vect


