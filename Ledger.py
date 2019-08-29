#!ust/bin/env python3
#-*- encoding: utf-8 -*-
__author__ = "QCF"

import os
import time
import sqlite3

class AccountBook:
    # 账本类
    def __init__(self, name, creat_date):
        # 账本名字与账本创建日期
        self.name = name
        self.creat_data = creat_date
        # 账本所在目录
        self.path = "./data/"
        self.filepath = "./data/" + self.name

        self.CreatFile(self.path)

        self.conn = sqlite3.connect(self.filepath)
        self.curs = self.conn.cursor()

        self.CreatTable('Main', {'Time':'varchar(255)', 'Cost':'int',
                                 'Note':'varchar(255)'})
        

    def CreatFile(self, path):
        # 创建账本文件目录
        try:
            if os.path.isdir(self.path):
                pass
            else:
                os.makedirs(self.path)
            END = True
        except Exception as e:
            END = e
        finally:
            return END

    def CreatTable(self, table_name, column_dic):
        # 为数据库文件创建表
        # 构造字段名及数据类型序列
        temp_command = ''
        for item in column_dic.keys():
            temp_command += (item + ' ' + column_dic[item] + ', ')
        temp_command = '(' + temp_command.rstrip(', ') + ')'
        
        try:
            sql_command = "CREATE TABLE IF NOT EXISTS {} {}".format(table_name, temp_command)
            self.conn.execute(sql_command)
            pass
        except Exception as e:
            print("[!]Error: ", e)

    def Add(self, table_name, value_tuple):
        # 添加记录
        try:
            sql_command = "INSERT INTO {} VALUES {}".format(table_name, value_tuple)
            self.conn.execute(sql_command)
            pass
        except Exception as e:
            print("[!]Error: ", e)
    def Update(self, table_name, target_tuple, update_dic):
        # 更新纪录
        update_str = ''
        for item in update_dic:
            update_str += (item + ' = ' + update_dic[item])
        try:
            sql_command = "UPDATE {} SET {} WHERE {} = {}".format(table_name, update_str, target_tuple[0], target_tuple[1])
            self.conn.execute(sql_command)
            pass
        except Exception as e:
            print("[!]Error: ", e)

    def Delete(self, table_name, del_tuple):
        # 删除记录
        try:
            sql_command = "DELETE FROM {} WHERE {} = {}".format(table_name, del_tuple[0], del_tuple[1])
            self.conn.execute(sql_command)
            pass
        except Exception as e:
            print("[!]Error: ", e)

    def Search(self, search_method, table_name, pattern='', data=''):
        # 通过特定模式进行查询
        try:
            if search_method == '1':
                sql_command = "SELECT * FROM {} WHERE {} = {}".format(table_name, pattern, data)
                search_ends = self.conn.execute(sql_command).fetchall()
            elif search_method == '2':
                sql_command = "SELECT * FROM {}".format(table_name)
                search_ends = self.conn.execute(sql_command).fetchall()
            else:
                raise Exception("Input Error! Please input the string 1 or 2.", search_method)
        except Exception as e:
            print("[!] Error:", e)
        finally:
            return search_ends

    def Command(self):
        # 类似cmd
        sql_command = input(">>> ")
        if sql_command == 'q':
            return 0
        try:
            END = self.conn.execute(sql_command).fetchall()
            print(END)
        except Exception as e:
            print(e)
        finally:
            return 1


    def Close(self):
        # 关闭光标，提交更改，关闭数据库连接
        self.curs.close()
        self.conn.commit()
        self.conn.close()



while True:
    sql_command = "select name from sqlite_master where type='table' order by name"
    OAB = AccountBook("Data.db", time.strftime("%Y%m%d%H%M%S"))
    TableName = OAB.conn.execute(sql_command).fetchall()
    print("[test]",TableName)
    print("Input quit() to exit")
    print("="*60)
    print("{:<15s}{:<15s}".format("1) Add","2) Update"))
    print("{:<15s}{:<15s}".format("3) Delete","4) Search"))
    print("{:<15s}{:<15s}".format("5) Show","6) Command"))
    print("="*60)
    com = input("Please input the command: ")
    if com == '1':
        try:
            print("-"*60)
            print("Exiting Table: {}".format(' '.join(TableName[0])))
            table_name = input("[*] Which table do you want to add infomation: ")
            temp_Time = input("[*] When did you spend the monkey(e.g. 20190821): ")
            temp_Cost = input("[*] How much monkey did you spend(￥): ")
            temp_Note = input("[*] Do you want to write some note about this spending?('Enter' to exit.)\n")
            value_tuple = (temp_Time, temp_Cost, temp_Note)
            print("[test]",value_tuple)
            OAB.Add(table_name, value_tuple)
        except Exception as e:
            print("[!] Error!!!, {}".format(e))
        finally:
            print("-"*60)
    elif com == '2':
        try:
            print("-"*60)
            update_dic = {}
            print("Exiting Table: {}".format(' '.join(TableName[0])))
            table_name = input("[*] Which table do you want to add infomation: ")
            target_tuple = tuple(input("[*] What condition do you want to update your table(e.g. 'name'='qcf'): "))
            print("When input the updated name, press 'Enter' to exit")
            while True:
                update_name = input("[*] The updated name is: ")
                if update_name == '':
                    break
                update_value = input("[*] The updated value is: ")
                update_dic[update_name] = update_value
            OAB.Update(table_name, target_tuple, update_dic)
        except Exception as e:
            print("[!] Error!!!, {}".format(e))
        finally:
            print("-"*60)
    elif com == '3':
        try:
            print("-"*60)
            print("Exiting Table: {}".format(' '.join(TableName[0])))
            table_name = input("[*] Which table do you want to delete infomation: ")
            temp_name = input("[*] What item are you want to delete: ")
            temp_value = input("[*] The value you want to delete is: ")
            del_tuple = (temp_name, temp_value)
            OAB.Delete(table_name, del_tuple)
        except Exception as e:
            print("[!] Error!!!, {}".format(e))
        finally:
            print("-"*60)
    elif com == '4':
        try:
            print("-"*60)
            print("Exiting Table: {}".format(' '.join(TableName[0])))
            table_name = input("[*] Which table do you want to search infomation: ")
            temp_name = input("[*] What item are you want to search: ")
            temp_value = input("[*] The value of the name is: ")
            search_ends = OAB.Search('1', table_name, temp_name, temp_value)
        except Exception as e:
            print("[!] Error!!!, {}".format(e))
        finally:
            print("[*]The searching ends are as follows:\n\t",search_ends)
            print("-"*60)
    elif com == '5':
        try:
            print("-"*60)
            print("Exiting Table: {}".format(' '.join(TableName[0])))
            table_name = input("[*] Which table do you want to show infomation: ")
            search_ends = OAB.Search('2', table_name)
        except Exception as e:
            print("[!] Error!!!, {}".format(e))
        finally:
            print("[*]The searching ends are as follows:\n", end = '')
            for item in search_ends:
                print("\n\t", item)
            print("-"*60)
    elif com == '6':
        try:
            while True:
                code = OAB.Command()
                if code == 0:
                    break
        except Exception as e:
            print("[*] Error!", e)
        finally:
            print("Exit Command Function.")
            print("-"*60)
            time.sleep(3)
    elif com == "quit()":
        break
    else:
        print("[!] Error!!!, {}".format("Wrong Input!!!"))
    OAB.Close()
exit()
