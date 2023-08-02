#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version 2.7.13 or 3.7.2

import random
import re
# 导入某个模块的部分类或方法
from datetime import datetime, timedelta

# 导入常量并重命名
import constant as const


class IdNumber(str):

    def __init__(self, id_number):
        super(IdNumber, self).__init__()
        self.id = id_number
        self.area_id = int(self.id[0:6])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_area_name(self):
        """根据区域编号取出区域名称"""
        return const.AREA_INFO[self.area_id]

    def get_birthday(self):
        """通过身份证号获取出生日期"""
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def get_age(self):
        """通过身份证号获取年龄"""
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def get_sex(self):
        """通过身份证号获取性别，女生：0，男生：1"""
        return int(self.id[16:17]) % 2

    def get_check_digit(self):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'

    @classmethod
    def verify_id(cls, id_number):
        """校验身份证是否正确"""
        if re.match(const.ID_NUMBER_18_REGEX, id_number):
            check_digit = cls(id_number).get_check_digit()
            return str(check_digit) == id_number[-1]
        else:
            return bool(re.match(const.ID_NUMBER_15_REGEX, id_number))

    @classmethod
    def random_generate_id(cls, sex=0):
        """随机生成身份证号，sex = 0 表示女性，sex = 1 表示男性"""

        # 随机生成一个区域码 (6 位数)
        area_id = str(random.choice(list(const.AREA_INFO.keys())))
        # id_number = str(random.choice(list(const.AREA_INFO.keys())))
        # 限定出生日期范围 (8 位数)
        start, end = datetime.strptime("1949-01-01", "%Y-%m-%d"), datetime.strptime("2022-12-31", "%Y-%m-%d")
        birth_days = datetime.strftime(start + timedelta(random.randint(0, (end - start).days + 1)), "%Y%m%d")
        id_number = area_id + str(birth_days)
        # 顺序码 (2 位数)
        id_number += str(random.randint(10, 99))
        # 性别码 (1 位数)
        id_number += str(random.randrange(sex, 10, step=2))
        # 校验码 (1 位数)
        return id_number + str(cls(id_number).get_check_digit())

    @classmethod
    def generate_id(cls, area_id, birth_days, sex=0):
        # 男 (1) 女 (0)
        id_number = str(area_id) + str(birth_days)

        # 顺序码 (2 位数)
        id_number += str(random.randint(10, 99))
        # 性别码 (1 位数)
        id_number += str(random.randrange(sex, 10, step=2))
        # 校验码 (1 位数)
        return id_number + str(cls(id_number).get_check_digit())

if __name__ == '__main__':
    print("###随机生成身份证号###")
    sex = random.randint(0, 1)  # 随机生成男 (1) 或女 (0)
    random_idcard = IdNumber.random_generate_id(sex) # 随机生成身份证号
    print(random_idcard)

    random_instance = IdNumber(random_idcard)

    print("地址编码：", random_instance.area_id)
    print("地址：", random_instance.get_area_name())
    print("生日：", random_instance.get_birthday())
    print("年龄：", random_instance.get_age())
    print("性别 (女 0):", random_instance.get_sex())
    print("校验码：", random_instance.get_check_digit())
    print("身份证是否正确：", IdNumber.verify_id(random_idcard))
    print()

    print("###生成身份证号###")
    idcard = IdNumber.generate_id("130101", "19901107")
    print(idcard)

    instance = IdNumber(idcard)

    print("地址编码：", instance.area_id)
    print("地址：", instance.get_area_name())
    print("生日：", instance.get_birthday())
    print("年龄：", instance.get_age())
    print("性别 (女 0):", instance.get_sex())
    print("校验码：", instance.get_check_digit())
    print("身份证是否正确：", IdNumber.verify_id(idcard))
    print()
