from . import Database
from Config import Config
import pymysql.cursors
import logging

class MySQLMPOS(Database):
	logger = logging.getLogger("Database.MySQLMPOS")
	def connect(self):
	    # Connect to the database
	    connection = pymysql.connect(host=Config.DATABASE_HOST, user=Config.DATABASE_USER,
		password=Config.DATABASE_PASSWORD, db=Config.DATABASE_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)
	    return connection

	def authorise(self, *args, **kwargs):
	    self.logger.info("Checking Auth For User: {0}".format(kwargs['username']))
	    connection = self.connect()
	    try:
		with connection.cursor() as cursor:
		   cursor.execute("SELECT id FROM `pool_worker` WHERE `username` = %(username)s", kwargs)
		   result = cursor.fetchone()
		   if result is None:
		      return 0
		   return result['id']
	    except Exception as e:
		self.logger.error(e)
		return False
	    return False

        def insert_shares(self, *args, **kwargs):
	    kwargs['lres'] = 'Y' if kwargs['lres'] == True else 'N'
            connection = self.connect()
            try:
                with connection.cursor() as cursor:
            	   cursor.execute("""INSERT INTO `shares` (time, rem_host, username, our_result, upstream_result, reason, solution, difficulty)
                	VALUES  (FROM_UNIXTIME(%(time)s), %(host)s, %(uname)s, %(lres)s, 'N', %(reason)s, %(solution)s, %(difficulty)s)""", kwargs)
		connection.commit()
            except Exception as e:
                self.logger.error(e)
                return False
            return False


