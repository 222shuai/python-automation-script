"""
下面这个代码是【小小明大佬】手撸的一个代码，使用了列表append()方法，效率虽说会低一些，
但是处理上百上千个文件，仍然不在话下。
需要注意的是代码中的第6行和第7行，获取文件路径，其中**代表的是文件夹下的子文件递归。
另外就是.xls*了，这个是正则写法，表示的是既可以处理xls格式，也可以处理xlsx格式的Excel文件，真是妙哉！
"""
# -*- coding: utf-8 -*-
import glob
import pandas as pd

path = "E:\\PythonCrawler\\python_crawler-master\\MergeExcelSheet\\file\\"
data = []
for excel_file in glob.glob(f'{path}/**/[!~]*.xls*'):
    # for excel_file in glob.glob(f'{path}/[!~]*.xlsx'):
    excel = pd.ExcelFile(excel_file)
    for sheet_name in excel.sheet_names:
        df = excel.parse(sheet_name)
        data.append(df)
# print(data)

df = pd.concat(data, ignore_index=True)
df.to_excel("小小明提供的代码(合并多表)--glob和pandas库列表append方法--所有表合并.xlsx", index=False)
print("合并完成!")
