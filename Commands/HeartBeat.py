import json
import time
import struct

def cmd_heartbeat(id, data, conn):
    result = "{0}.{1}.ok.pulse".format(id, time.time())
    length = struct.pack("<I", len(result))
    conn.send(length)
    conn.send(result)
    return

