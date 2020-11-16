import bot
from core import core
from sql import SQLighter
import requests, time


print("main: {}".format(__name__))
if __name__=="__main__":
    print("start0")
    db = SQLighter()
    while True:
        print('New check')
        if True:
            users = db.live_update_list()
            print("Get {} users".format(len(users)))
            if users:
                for u in users:
                    cor = core(idd=u['id'])
                    command, messid, *_ = u['live_update_mode'].split(';')
                    if command=='sport':
                        commandall = '/{} -20'.format(command)
                    else:
                        commandall = '/{}'.format(command)
                    data = cor.command(commandall,live_update=True)
                    data['messId'] = messid
                    data['command'] = command
                    data['live_update'] = True
                    print(data)
                    sent_info = bot.send(data=data,to=u['telid'])
                    cor.close(data=data, sent_info=sent_info, mode = 'command')


        # except Exception as e:
        #     print("{!s}\n{!s}".format(type(e), str(e)))
        # time.sleep(20)
        time.sleep(600)