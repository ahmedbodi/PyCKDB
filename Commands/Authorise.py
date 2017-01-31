from Database.MySQLMPOS import MySQLMPOS
from Arguments import parser
import json
import time
import struct

database = MySQLMPOS()
arguments = parser.parse_args()

def cmd_authorise(id, data, conn):
    data = json.loads(data)
    username = data['workername']
    id = database.authorise(username=username, create_user=arguments.create_user)
    result = "{0}.{1}.failed.DBE".format(id, int(time.time()))
    if id > 0:
       result = "{0}.{1}.ok.addrauth={2}".format(id, int(time.time()), json.dumps({'secondaryuserid': str(id), 'difficultydefault': 1}))
    length = struct.pack("<I", len(result))
    conn.send(length)
    conn.send(result)
    return

