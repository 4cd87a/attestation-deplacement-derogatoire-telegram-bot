# -*- coding: utf-8 -*-
import os.path, random, time
from datetime import datetime
import mysql.connector
import config


class SQLighter:

    def __init__(self, telid=None, idd=None, logger=None):
        self.logger = logger
        self.connection = mysql.connector.connect(
            host=config.mysql_host,
            port=config.mysql_port,
            user=config.mysql_user,
            passwd=config.mysql_passwd,
            database=config.mysql_database
        )
        self.cursor = self.connection.cursor()
        self.idd = None
        self.user = self.user_get(telid=telid,idd=idd)
        self.idd = None if self.user is None else self.user['id']

    def _print(self, txt, type="INFO"):
        if self.logger == None:
            #return
            print("[{}] : {}".format(type, txt))
        else:
            type = type.lower()
            if type == "info" or type == 'i':
                self.logger.info(txt)
            if type == "warning" or type == 'w':
                self.logger.warning(txt)
            if type == "error" or type == 'e':
                self.logger.error(txt)

    def close(self):
        self.cursor.close()
        self.connection.close()


    def getFromTable(self, table, field, like=""):
        field_text = ""
        for f in field:
            field_text += "`" + str(f) + "`,"
        field_text = field_text[0:-1]
        table = '`' + str(table) + '`'
        # with self.connection:
        self._print("SELECT " + field_text + " FROM " + str(table) + " " + like, 'i')
        self.cursor.execute("SELECT " + field_text + " FROM " + str(table) + " " + like)
        res = self.cursor.fetchall()

        self.connection.commit()

        if len(res):
            ret = []
            for j in range(len(res)):
                dic = {}
                for i, f in enumerate(field):
                    dic.update({f: res[j][i]})
                ret.append(dic)
            return ret
        else:
            return []

    def addToTable(self, table, field, whattoad):
        if len(field) != len(whattoad): raise ValueError("field and whattoad aren't the same leng in addToTable")
        field_text = "("
        add_text = "("
        for i in range(len(field)):
            # print(field[i])
            # print(whattoad[i])
            field_text += "`" + str(field[i]) + "`,"
            # if type(whattoad[i]) == int or type(whattoad[i]) == float: add_text += "" + str(whattoad[i]) + ","
            add_text += "'" + str(whattoad[i]) + "',"

        field_text = field_text[0:-1] + ")"
        add_text = add_text[0:-1] + ")"
        table = '`' + str(table) + '`'

        # with self.connection:
        self._print("INSERT INTO " + table + field_text + " VALUES " + add_text, 'i')
        self.cursor.execute("INSERT INTO " + table + field_text + " VALUES " + add_text)
        self.cursor.execute("SELECT max(id) from {}".format(table))
        res = self.cursor.fetchall()

        self.connection.commit()

        return res[0][0]

    def changeTable(self, table, field, whattoad, like):
        if len(field) != len(whattoad): raise ValueError("field and whattoad aren't the same leng in changeTable")
        if len(field) == 0: return True

        field_text = ""
        for i in range(len(field)):
            field_text += "`" + str(field[i]) + "`" + "=" + "'" + str(whattoad[i]) + "',"
        field_text = field_text[0:-1]
        table = '`' + str(table) + '`'

        # with self.connection:
        self._print("UPDATE " + table + " SET " + field_text + " " + like, 'i')
        self.cursor.execute("UPDATE " + table + " SET " + field_text + " " + like)

        self.connection.commit()

        return True

    def deleteFromTable(self, table, like):
        table = '`' + str(table) + '`'
        # with self.connection:
        self._print("DELETE FROM " + table + " " + like, 'w')
        self.cursor.execute("DELETE FROM " + table + " " + like)

        self.connection.commit()

        return True

    def user_add(self,telid, telusername, mode=0):
        return self.addToTable('users',
                               ['telid', 'telusername', 'mode'],
                               [telid, telusername, mode])

    def user_add_all(self,telid, telusername, name, birthday,placeofbirth,adress,place,mode=0):
        return self.addToTable('users',
                               ['telid', 'telusername', 'name', 'birthday','placeofbirth','adress','place','mode','admin'],
                               [telid, telusername, name, birthday, placeofbirth, adress, place, mode,0])

    def user_get(self,idd=None, telid=None,all=False):
        like = None
        if idd and type(idd)==int:
            like = "WHERE `id`={}".format(idd)
        if telid and type(telid)==int:
            like = "WHERE `telid`={}".format(telid)
        if like is None and self.idd is not None:
            like = "WHERE `id`={}".format(self.idd)
        if like is None: return None

        if all:
            res = self.getFromTable('users',['id','telid', 'telusername', 'name', 'birthday','placeofbirth','adress','place','mode','admin'],like)
        res = self.getFromTable('users',['id','telid','name', 'birthday','placeofbirth','adress','place','mode','admin'],like)
        if len(res): return res[0]
        return None

    def user_update(self,idd=None, telid=None, telusername=None, name=None, birthday=None,placeofbirth=None,adress=None,place=None,mode=None):
        like = None
        if idd and type(idd) == int:
            like = "WHERE `id`={}".format(idd)
        if telid and type(telid) == int:
            like = "WHERE `telid`={}".format(telid)
        if like is None and self.idd is not None:
            like = "WHERE `id`={}".format(self.idd)
        if like is None: return None

        fields = []
        values = []
        if telusername:
            fields.append('telusername')
            values.append(telusername)
        if name:
            fields.append('name')
            values.append(name)
        if birthday:
            fields.append('birthday')
            values.append(birthday)
        if placeofbirth:
            fields.append('placeofbirth')
            values.append(placeofbirth)
        if adress:
            fields.append('adress')
            values.append(adress)
        if place:
            fields.append('place')
            values.append(place)
        if mode is not None and type(mode)==int:
            fields.append('mode')
            values.append(mode)

        return self.changeTable('users',fields,values,like)

    def user_set_mode(self,idd=None, telid=None,mode=0):
        return self.user_update(idd=idd,telid=telid,mode=mode)

    def user_all(self):
        res = self.getFromTable('users',['id','telid'])
        if len(res): return res
        return None


    def live_update_list(self,delta=1200,active_duration=10800):
        timenow = time.time()
        like = "WHERE `live_update_start`>'{}' AND `live_update_last`<'{}' ORDER BY `live_update_last`".format(round(timenow - active_duration),round(timenow - delta))
        return self.getFromTable('users', ['id', 'telid', 'live_update_start', 'live_update_last', 'live_update_mode'], like)


    def live_update_update(self,idd=None, telid=None,last=None,start=None,mode=None):
        like = None
        if idd and type(idd) == int:
            like = "WHERE `id`={}".format(idd)
        if telid and type(telid) == int:
            like = "WHERE `telid`={}".format(telid)
        if like is None and self.idd is not None:
            like = "WHERE `id`={}".format(self.idd)
        if like is None: return None

        fields = ['live_update_last']
        if last==None:
            last = round(time.time())
        values = [last]

        if start==-1:
            fields.append('live_update_start')
            values.append(round(time.time()))
        elif start != None:
            fields.append('live_update_start')
            values.append(start)

        if mode!=None:
            fields.append('live_update_mode')
            values.append(mode)

        return self.changeTable('users', fields, values, like)

    def log_add(self,idd=None, typ=0, message=''):
        message = message.replace('"','').replace("'","")
        like = idd or self.idd
        if like is None: return None

        return self.addToTable('logs',
                               ['id_user', 'typ', 'message'],
                               [like, typ, message])
