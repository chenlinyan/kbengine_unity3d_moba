# -*- coding: utf-8 -*-

import csv
import KBEngine
import codecs


class CSV_Helper:
    """
    这是一个配置文件类
    """

    def __init__(self):

        self.datas = {}


    def getTable(self,table):
        if table  in self.datas:
            return self.datas[table]
        else:
            return self.loadFile(table)

    def getRow(self,table,row_index):
        '''

        :param table: csv file name
        :param index: id
        :return: dic
        '''

        table_data = self.getTable(table)
        if table_data is None:
            return None

        index = int(row_index)

        return table_data.get(index,None)

    def getColumn(self,table,row_index,column):
        '''

        :param table: csv file name
        :param row_index: row id
        :param column: row field
        :return:
        '''

        rowData = self.getRow(table,row_index)
        if rowData is None:
            return None
        return rowData.get(column,None)

    def isNum(self,valueStr):
        '''

        :param valueStr: input value string
        :return: bool  is numberic
        '''

        try:
            eval(valueStr)
        except TypeError:
            return False
        except ValueError:
            return False
        except SyntaxError:
            return False
        else:
            return True


    def convert(self,typeName,valueStr):
        '''

        :param typeName: type string
        :param valueStr: value string
        :return: value
        '''

        if valueStr is None:
            return None

        value = None

        if typeName == 'int':
            if self.isNum(valueStr):
                value = int(eval(valueStr))
            else:
                value = 0

        elif typeName == 'float':
            if self.isNum(valueStr):
                value = float(eval(valueStr))
            else:
                value = 0.0
        else:
            value = valueStr

        return value


    def loadFile(self,fileName):
        '''
        :param fileName: csv 文件名
        :return: 有返回一个 table,没有返回 None
        '''
        reader = csv.reader(KBEngine.open("data/"+fileName,"r+",'UTF-8'))

        table = [line for line in reader]

        if len(table) < 3:
            return  None

        keys = table[0];
        types = table[1];
        #descs = table[2];

        rows = {}
        for row in table[3:]:
            row_dic = {}
            for index, column  in enumerate(row):
                key_str = keys[index]
                type_str = types[index]
                row_dic[key_str] = self.convert(type_str,column)
            rows[int(row[0])] = row_dic

        self.datas[fileName] = rows

        return self.datas.get(fileName,None)


'''
Usage:

conf = CSV_Helper()
table =  conf.getTable('d_team.csv')

for key,value in table.items():
    print(key,value)

'''


