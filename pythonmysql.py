import pymysql


# 定义类用来创建玩家对象
class Player(object):
    def __init__(self, name, passwd, conn, money=200.0):
        self.name = name
        self.passwd = passwd
        self.c = conn
        self.money = money
        self.moneychange = 0.0
        self.result = 0


def register(player):
    print('enter register')
    db = pymysql.connect('localhost', 'root', '123456', 'game', charset='utf8')
    cur = db.cursor()
    sql = 'select * from players;'
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    for i in data:
        if player.name == i[0]:
            cur.close()
            db.close()
            return False
    else:
        sql = "insert into players values('%s', '%s',%f);" % (player.name, player.passwd, player.money)
        cur.execute(sql)
        print(sql)
        db.commit()
        cur.close()
        db.close()
        return True


def update(player):
    print('enter update')
    db = pymysql.connect('localhost', 'root', '123456', 'game', charset='utf8')
    cur = db.cursor()
    sql = 'select * from players;'
    cur.execute(sql)
    data = cur.fetchall()
    for i in data:
        if player.name == i[0]:
            player.money = player.money + player.moneychange
            break
    sql1 = "update players set money=%f where name='%s';" % (player.money, player.name)
    cur.execute(sql1)
    print(sql1)
    db.commit()
    cur.close()
    db.close()


def match(player):
    print('enter match')
    db = pymysql.connect('localhost', 'root', '123456', 'game', charset='utf8')
    cur = db.cursor()
    sql = 'select * from players;'
    cur.execute(sql)
    data = cur.fetchall()
    for i in data:
        if player.name == i[0] and player.passwd == i[1]:
            player.money = i[2]
            cur.close()
            db.close()
            return True
    else:
        cur.close()
        db.close()
        return False
