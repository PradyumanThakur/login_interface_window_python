#!/usr/bin/env python


import sqlite3
login_db = sqlite3.connect('user_credential.db')

c = login_db.cursor()


c.execute("""
	CREATE TABLE `signup_credential` (
  `user_id` int AUTO_INCREMENT,
  `first_name` varchar(20),
  `last_name` varchar(20),
  `email_address` varchar(40),
  `sex` varchar(10),
  `birth_date` date,
  `age` int,
  `phone_num` varchar(15),
  `password` varchar(40),
  PRIMARY KEY (`user_id`)
)""")





