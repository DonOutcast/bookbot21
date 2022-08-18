from src.databases.sql_database import DatabaseBot

user_db = DatabaseBot("test1.db") #test1.db
user_db.sql_create_users()
user_db.sql_create_booking()
user_db.sql_create_objects()
