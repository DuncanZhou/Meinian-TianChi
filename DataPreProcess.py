#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# 数据预处理,处理为 病人ID,各项体检结果,五项标签
import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('gbk')

import csv


# {A,B,C,D,E}分别代表五项指标
# 这两个txt文件以 $ 分隔
features_path1 = "meinian_round1_data_part1_20180408.txt"
features_path2 = "meinian_round1_data_part2_20180408.txt"
label_path = "meinian_round1_train_20180408.csv"

# 获取所有用户id和体检项目
def GetPID(path,ids,operations):
    with open(path,'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            row = line.split("$")
            ids.add(row[0])
            operations.add(row[1])
    return ids,operations

def Preprocess(path,patients):
    '''
    :param path: 文件路径
    :param patients: 病人集合(字典类型)
    :return:
    '''
    with open(path,'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            row = line.split("$")
            if not patients.has_key(row[0]):
                patients[row[0]] = {}
            patients[row[0]][row[1]] = row[2]
    return patients

# 读取五项指标
def ReadLabel(path):
    labels = {}
    with open(path,'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            row = line.split(",")
            labels[row[0]] = {}
            labels[row[0]]['A'] = row[1]
            labels[row[0]]['B'] = row[2]
            labels[row[0]]['C'] = row[3]
            labels[row[0]]['D'] = row[4]
            labels[row[0]]['E'] = row[5]
    return labels

# 将字典文件转换为csv文件
def ConvertToCSV(patients,operations,labels):
    Training = open("training.csv",'w')
    csv_writer = csv.writer(Training)
    # 先写入头
    header = ['id']
    features = [op for op in operations]
    label = ['A','B','C','D','E']
    header.extend(features)
    header.extend(label_path)
    csv_writer.writerow(header)
    count = 0
    for id in patients.keys():
        cur = [id]
        if not labels.has_key(id):
            continue
        temp = []
        for op in operations:
            if op in patients[id]:
                temp.append(patients[id][op])
            else:
                temp.append(None)
        for l in label:
            temp.append(labels[id][l])
        cur.extend(temp)
        csv_writer.writerow(cur)
        count += 1
    print "共写入%d个病人" % count
    Training.close()

def test():
    patients = {}
    ids = set()
    operations = set()
    GetPID(features_path1,ids,operations)
    GetPID(features_path2,ids,operations)
    print "共有%d个病人" % len(ids)
    print "共有%d种体检项目" % len(operations)
    print "正在读取病人体检信息"
    patients = Preprocess(features_path1,patients)
    patients = Preprocess(features_path2,patients)
    print "共有%d个病人" % len(patients)
    labels = ReadLabel(label_path)
    print "正在存入csv文件"
    ConvertToCSV(patients,operations,labels)

    # with open("training.csv",'r') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         print line
# test()

