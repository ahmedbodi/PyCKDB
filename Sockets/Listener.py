from inspect import getmembers, isfunction
from thread import start_new_thread
import socket
import os
import struct
import logging
import threading
import Commands

class Listener(threading.Thread):

	listener_cmds = {}

	def __init__(self):
	    self.address = '/opt/ckdb/listener'
	    self.logger = logging.getLogger('Sockets.Listener')
	    self.get_available_commands()

	def get_available_commands(self):
            listener_cmds_set = [o for o in getmembers(Commands) if isfunction(o[1])]
	    for item in listener_cmds_set:
		# Add each command to the dict and remove the cmd_ tag
		self.listener_cmds[item[0][4:]] = item[1]

	def clear_old_sockets(self):
	    self.logger.debug("Deleting Old Sockets")
	    try:
		os.unlink(self.address)
	    except OSError:
		if os.path.exists(self.address):
		   raise

	    if os.path.exists(self.address):
	       os.remove(self.address)

	def run(self):
	    self.clear_old_sockets()
	    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	    self.logger.info("Binding to {0}".format(self.address))
	    sock.bind(self.address)

	    sock.listen(10)
	    while True:
		conn, address = sock.accept()
		start_new_thread(self.handle_client, (conn,))

	def handle_client(self, conn):
	    length = struct.unpack("<I", conn.recv(4))[0]
	    data = conn.recv(length)
	    method = data.split('.')[0]
	    id     = data.split('.')[1]
	    data   = data.split('=')[1]
	    self.logger.debug("Received Method: {0}".format(method))
	    self.handle_cmd(method, id, data, conn)

	def handle_cmd(self, method, id, data, conn):
	    try:
	       self.listener_cmds[method](id, data, conn)
	    finally:
	       conn.close()
