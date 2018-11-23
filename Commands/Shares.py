from Database.MySQLMPOS import MySQLMPOS
import json
import time
import struct

database = MySQLMPOS()

def cmd_shares(id, data, conn):
    data = json.loads(data)
    if not data.has_key('reject-reason'):
       data['reject-reason'] = None 

    share_values = {'time': int(time.time()), 'host': data['address'], 'uname': data['workername'], 'lres': data['result'], 'reason': data['reject-reason'],
	'solution':  data['hash'], 'difficulty': data['diff']}

    database.insert_shares(**share_values)
    result = "{0}.{1}.ok.queued".format(id, time.time())
    length = struct.pack("<I", len(result))
    conn.send(length)
    conn.send(result)
    return


