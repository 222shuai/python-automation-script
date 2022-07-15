"""
下面这个代码是基于【小小明大佬】提供的单Sheet表合并代码改进所得到的，关键点在于
将sheet_name=None这个参数带上，代表获取Excel文件中的所有sheet表，其返回的是
一个字典，所有在后面遍历的时候，是以字典的形式进行取值的，之后在15行的地方，需要
注意使用的是extend()方法进行追加，如果使用append()方法，得到的就只有最后一个表
格的合并结果，这个坑小编亲自踩过，感兴趣的小伙伴也可以踩下坑。
"""
# -*- coding: utf-8 -*-
import os
import pandas as pd
result = []
path = r"E:\\PythonCrawler\\python_crawler-master\\MergeExcelSheet\\testfile\\file"
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        if name.endswith(".xls") or name.endswith(".xlsx"):
            df = pd.read_excel(os.path.join(root, name), sheet_name=None)
            result.append(df)

data_list = []
for data in result:
    # print(data.values())
    data_list.extend(data.values())  # 注意这里是extend()函数而不是append()函数

df = pd.concat(data_list)
df.to_excel("testfile所有表合并.xlsx", index=False)
print("合并完成!")