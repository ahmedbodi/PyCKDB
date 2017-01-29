from Sockets.Listener import Listener
from daemonize import Daemonize
import logging
import argparse
import setproctitle

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--daemonize', type=bool)
parser.add_argument('-v', '--verbose', default=False, type=bool)

pid = "/opt/ckdb/PyCKDB.pid"

def main():
    setproctitle.setproctitle("PyCKDB")
    listener = Listener()
    listener.run()

if __name__ == "__main__":
   args =  parser.parse_args()
   if args.verbose:
      logging.basicConfig(level=logging.DEBUG)
   else:
       logging.basicConfig(level=logging.INFO)

   if args.daemonize:
      daemon = Daemonize(app="PyCKDB", pid=pid, action=main)
      daemon.start()
   else:
	main()
