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

	def get_uid(self, username):
	    connection = self.connect()
	    try:
		with connection.cursor() as cursor:
		   user = username.split('.', 1)[0]
		   cursor.execute("SELECT `id`, `is_locked` FROM `accounts` where `username`='{0}'".format(user))
        	   row = cursor.fetchone()
		   if row is None:
			return False
		   elif	row['is_locked'] == 2:
			self.logger.error("User {} is banned by admin".format(user))
			return False
		   else:
			return row['id']
		   return False
	    except Exception as exc:
		self.logger.error(exc)
		return False

	def authorise(self, *args, **kwargs):
	    self.logger.info("Checking Auth For User: {0}".format(kwargs['username']))
	    connection = self.connect()
	    uid = self.get_uid(kwargs['username'])
	    if uid is None:
		return False
	    else:
		return uid
	    return False

        def insert_shares(self, *args, **kwargs):
	    kwargs['lres'] = 'Y' if kwargs['lres'] == True else 'N'
            connection = self.connect()
            try:
                with connection.cursor() as cursor:
                   cursor.execute("SELECT `id` FROM `pool_worker` WHERE `username` = %(uname)s", kwargs) #cheking that worker is exec in pool_worker table
                   result = cursor.fetchone()
                   if result is None    :
			uid = self.get_uid(kwargs['uname'])
                        query = "INSERT INTO `pool_worker` (`account_id`, `username`, `password`) VALUES ({}, '{}', 'x');".format(uid, kwargs['uname']) #create worker if it not exec
                        cursor.execute(query)
			self.logger.info("worker {} created".format(kwargs['uname']))
            	   cursor.execute("""INSERT INTO `shares` (`time`, `rem_host`, `username`, `our_result`, `upstream_result`, `reason`, `solution`, `difficulty`)
                	VALUES  (FROM_UNIXTIME(%(time)s), %(host)s, %(uname)s, %(lres)s, 'N', %(reason)s, %(solution)s, %(difficulty)s)""", kwargs)
		   cursor.execute("UPDATE `pool_worker` SET `difficulty`=%(difficulty)s WHERE `username`=%(uname)s", kwargs) #update current diff for worker to present it in worker stats page
		connection.commit()
            except Exception as e:
                self.logger.error(e)
                return False
            return False


