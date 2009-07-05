" tell.py: written by sklnd in July 2009"

import datetime, time
import sqlite3
import hook
import os
from timesince import timesince

dbname = "skydb"

def adapt_datetime(ts):
    return time.mktime(ts.timetuple())

sqlite3.register_adapter(datetime.datetime, adapt_datetime)

@hook.command(hook=r'(.*)', prefix=False, ignorebots=True)
def tellinput(bot,input):
    dbpath = os.path.join(bot.persist_dir, dbname)
    conn = dbconnect(dbpath)

    cursor = conn.cursor()
    command = "select count(name) from tell where name = ? and chan = ?"
    results = cursor.execute(command, (input.nick,input.chan)).fetchone()


    if results[0] > 0:
        command = "select id, user_from, quote, date from tell where name = ? and chan = ?"
        tells = cursor.execute(command, (input.nick, input.chan)).fetchall()

        for tell in tells:
            reltime = timesince(datetime.datetime.fromtimestamp(tell[3]))
            bot.reply('%(teller)s said %(reltime)s ago: %(quote)s' % \
                    {'teller': tell[1], 'quote': tell[2], 'reltime': reltime})
            command = "delete from tell where id = ?"
            cursor.execute(command, (tell[0],))

        conn.commit()
    conn.close()
        


@hook.command
def tell(bot, input):
    
    ".tell <nick> - Tell somebody something later. Unless you suck, in which case tell yourself to go take a hike"

    if len(input.msg) < 6:
        return tell.__doc__

    query = input.msg[6:].strip().partition(" ")

    if query[0] == input.nick:
        return "No."


    if query[2] != "":
        dbpath = os.path.join(bot.persist_dir, dbname)
        conn = dbconnect(dbpath)

        command = "select count(*) from tell_probation where name=?"
        if conn.execute(command, (input.nick,)).fetchone()[0] > 0:
            return "No."

        command = "select count(*) from tell where name=? and user_from=?"
        if conn.execute(command, (query[0], input.nick)).fetchone()[0] >= 3:
            return "You've told that person too many things."

        cursor = conn.cursor()
        command = "insert into tell(name, user_from, quote, chan, date) values(?,?,?,?,?)"
        cursor.execute(command, (query[0], input.nick, query[2], input.chan, datetime.datetime.now()))
            
        conn.commit()
        conn.close()
        return "I'll let (him|her|it) know."

    else: 
        return tell.__doc__

# check to see that our db has the the seen table, and return a connection.
def dbconnect(db):
    conn = sqlite3.connect(db)
    results = conn.execute("select count(*) from sqlite_master where name=?", ("tell" ,)).fetchone()

    if results[0] == 0:
        conn.execute("create table if not exists "+ \
                     "tell(id integer primary key autoincrement, name varchar(50), user_from varchar(50), "+ \
                     " quote varchar(250), chan varchar(50), date datetime);")

        conn.commit()

    results = conn.execute("select count(*) from sqlite_master where name=?", ("tell_probation" ,)).fetchone()
    if results[0] == 0:
        conn.execute("create table if not exists "+ \
                     "tell_probation(name varchar(50),"+ \
                     "primary key(name));")
        conn.commit()

    return conn

