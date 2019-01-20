import sqlite3


class BaseDBProject():
    def __init__(self, path):
        self.path = path
        self.connnect = sqlite3.connect(path)
        # print("Opened database successfully")

    def check(self):
        if self.connnect is None:
            self.connnect = sqlite3.connect(self.path)

    def cur_exe(self, ask):
        # print("Sql statement executed : " + ask)
        cursor = self.connnect.cursor()
        return cursor.execute(ask)

    def fetchall(self, cur):
        ans = cur.fetchall()
        cur.close()
        return ans

    def commit(self):
        '''
            提交操作
        '''
        self.connnect.commit()

    def rollback(self):
        '''
            撤销操作
        '''
        self.connnect.rollback()

    def close(self):
        '''
            关闭连接
        '''
        self.connnect.close()

    def create_table(self, table_name, dic):
        '''
            dic : 键名和类型
        '''
        if self.exist_table(table_name):
            print("Existed table ! ")
            return
        ask = 'create table %s ' % table_name + \
            ' (%s) ' % ','.join(i+' '+j for i, j in dic.items())
        cur = self.cur_exe(ask)
        self.commit()
        # print("Table created successfully")
        return cur

    def exist_table(self, table_name):
        condition = "type='table' and name = '%s'" % table_name
        if self.fetchall(self.selete(condition=condition)) != []:
            return True

    def insert(self, table_name, dic):
        condition = "id=%s" % str(dic['id'])
        if self.fetchall(self.selete(name=table_name, lis=['id'], condition=condition)) != []:
            return self.update(table_name, condition, dic)

        ask = 'insert into %s ' % table_name + ' (%s) ' % ','.join(
            i[0] for i in dic.items()) + ' values(%s) ' % ','.join("'%s'" % str(i[1]) for i in dic.items())
        cur = self.cur_exe(ask)
        self.commit()
        # print("Records created successfully")
        return cur

    def selete(self, lis=['sql'], name='sqlite_master', condition="type='table'", distinct=1):
        '''
            name : 可以是表名,sqlite_master

            distinct : 1->允许args.value重复

            lis : 待查询
        '''
        if distinct == True:
            ask = 'select %s ' % ','.join(
                i for i in lis) + 'from %s ' % name + 'where %s' % condition
        else:
            ask = 'select distinct %s ' % ','.join(
                i for i in lis) + 'from %s ' % name + 'where %s' % condition
        cur = self.cur_exe(ask)
        # print("Selete done successfully")
        return cur

    def update(self, table_name, condition, change_dic):
        '''
            condition : sql表达式

            change_list : 待修改的键和值组成的字典
        '''
        ask = ' update %s set ' % table_name + \
            ','.join((i+'='+"'%s'" % j) for i, j in change_dic.items()) + \
            ' where %s ' % condition
        cur = self.cur_exe(ask)
        self.commit()
        # print("Update done successfully")
        return cur

    def delete(self, table_name, condition):
        '''
            condition : sql表达式
        '''
        ask = 'delete from %s where %s ' % (table_name, condition)
        cur = self.cur_exe(ask)
        self.commit()
        # print("Delete done successfully")
        return cur
