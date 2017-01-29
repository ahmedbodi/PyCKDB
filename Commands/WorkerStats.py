import json
import time
import struct

def cmd_workerstats(id, data, conn):
    result = "{0}.{1}.ok.queued".format(id, time.time())
    length = struct.pack("<I", len(result))
    conn.send(length)
    conn.send(result)
    return

