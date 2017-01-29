import json
import time
import struct

def cmd_workinfo(id, data, conn):
    result = "{0}.{1}.ok.queued\n".format(id, int(time.time()))
    length = struct.pack("<I", len(result))
    conn.send(length)
    conn.send(result)
    return
