#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np


class TrieNode:
    def __init__(self):
        self.child = {}


class AgeTree:

    def __init__(self):
        self.algorithm = "age_attribute_tree"
        self.root = TrieNode()

    def add_keyword(self, keyword):
        node_curr = self.root
        for index in keyword:
            if node_curr.child.get(index) is None:
                node_next = TrieNode()
                node_curr.child[index] = node_next  # 把孩子节点w
            node_curr = node_curr.child[index]
        return self.root

    def add_keywords_from_list(self, attribute_split):
        for vals in attribute_split:
            self.add_keyword(vals)

    def to_vect(self, age_value):
        vect = np.zeros(0, dtype=int)
        index_age = self.age_to_tree(age_value)
        node_curr = self.root
        for path in index_age:
            if path == age_value:
                end = node_curr.child.keys()
                ind = list(end)[0].index(age_value)
                T = np.zeros(10, dtype=int)
                T[ind] = 1
                vect = np.concatenate((vect, T), axis=0)
            if node_curr.child.get(path) is not None:
                key = node_curr.child.keys()
                vect_len = len(key)
                T = np.zeros(vect_len, dtype=int)
                ind = list(key).index(path)
                T[ind] = 1
                vect = np.concatenate((vect, T), axis=0)
                node_curr = node_curr.child[path]
        return vect

    def age_to_tree(self, index):
        if index < 30:
            if index < 10:
                age = ['1-100', '0-30', '0-10', index]
            elif index < 20:
                age = ['1-100', '0-30', '10-20', index]
            elif index < 30:
                age = ['1-100', '0-30', '20-30', index]
        elif index < 60:
            if index < 40:
                age = ['1-100', '30-60', '30-40', index]
            elif index < 50:
                age = ['1-100', '30-60', '40-50', index]
            elif index < 60:
                age = ['1-100', '30-60', '50-60', index]
        elif index < 100:
            if index < 70:
                age = ['1-100', '60-100', '60-70', index]
            elif index < 80:
                age = ['1-100', '60-100', '70-80', index]
            elif index < 90:
                age = ['1-100', '60-100', '80-90', index]
            elif index < 100:
                age = ['1-100', '60-100', '90-100', index]
        return age

    def build_dict(self):
        age_dict = {}
        for age_value in range(0, 100):
            age_vect = self.to_vect(age_value)
            age_dict1 = {age_value: age_vect}
            age_dict.update(age_dict1)
        age_rang = {'60-100': [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    '0-30': [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    '20-30': [1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
        age_dict.update(age_rang)
        return age_dict

