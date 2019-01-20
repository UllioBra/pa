import sqlite3

class sql():
    def __init__(self, db_name):
        self.connect = sqlite3.connect(db_name)
        print("Open database successfully")


    def cur_exe(self, ask):
        cursor = self.connect.cursor()
        cursor.execute(ask)
        self.connect.commit()
        return cursor


    def creat_table(self, name, dic = {'ID INT PRIMARY' : 'KEY'}):
        '''
            根据name,dic创建表

            name : 表名

            dic : 键值和类型
        '''
        if self.exists_table(name):
            print("Table has existed ! ")
            return 
        bs = ''
        for i,j in dic.items():
            bs = bs + i + ' ' + j + ','
        bs = bs.rstrip(',')
        ask = '''CREATE TABLE %s(%s);''' % (name, bs)
        self.cur_exe(ask)
        print("Table %s has been created ! " % name)


    def exists_table(self, table_name):
        '''
            根据表名查询数据库中是否存在指定表

            Return 1(True) 0(False)
        '''
        ask = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s'" % (table_name)
        ans = self.cur_exe(ask).fetchall()
        return int(ans[0][0])


    def insert_one(self, table_name, dic = {'id':1}):
        '''
            根据表名在指定表插入数据
        '''
        key = ()
        value = ()
        for i,j in dic.items():
            key = key + (i,)
            value = value + (j,)
        ask = 'INSERT INTO %s %s VALUES %s' % (table_name, key, value)
        ans = self.cur_exe(ask).rowcount
        return ans

    
    def select(self, table_name, dic):
        '''
            正在施工

            简易查询数据

            若高级请使用cur_exe自定义语句
        '''
        pass


    def close(self, is_commit = 1):
        '''
            关闭数据库

            iscommit : 是否提交,默认提交
        '''
        if is_commit:
            self.connect.commit()
        self.connect.close()


    
    