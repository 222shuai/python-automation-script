"""
下面这个代码是【小小明大佬】手撸的另外一个代码，使用了sheet_name=None和列表extend()方法，
将sheet_name=None这个参数带上，代表获取Excel文件中的所有sheet表，其返回的是一个字典，
所有在后面遍历的时候，是以字典的形式进行取值的，效率比前面的方法都要高一些。
需要注意的是代码中的第6行和第7行，获取文件路径，其中**代表的是文件夹下的子文件递归。
另外就是.xls*了，这个是正则写法，表示的是既可以处理xls格式，也可以处理xlsx格式的Excel文件，真是妙哉！
"""
# -*- coding: utf-8 -*-
import glob
import pandas as pd
path = r"E:\PythonCrawler\python_crawler-master\MergeExcelSheet\file"
data = []
# for excel_file in glob.glob(f'{path}/**/[!~]*.xlsx'):
for excel_file in glob.glob(f'{path}/[!~]*.xlsx'):
    dfs = pd.read_excel(excel_file, sheet_name=None).values()
    data.extend(dfs)
# print(data)

df = pd.concat(data, ignore_index=True)
df.to_excel("小小明提供的代码(合并多表)--glob和pandas库列表extend方法--简洁--所有表合并.xlsx", index=False)
print("合并完成!")