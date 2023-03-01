import sqlite3

with sqlite3.connect('pars.db', timeout=15000) as data:
            curs = data.cursor()
            curs.execute("""CREATE TABLE IF NOT EXISTS data_1c (
            id TEXT NOT NULL PRIMARY KEY,
            full_name TEXT,
            short_name TEXT,
            minsupplierprice INTEGER,
            maxsupplierprice INTEGER,
            retailprice INTEGER,
            quantity INTEGER,
            model TEXT,
            groupid1,
		        groupid2,
        		groupid3,
        		groupid4,
        		groupid5,
        		groupid16
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS users (
            id TEXT NOT NULL PRIMARY KEY,
            first_name TEXT,
            username TEXT,
            access BOOL DEFAULT False
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS comparison (
            id TEXT NOT NULL PRIMARY KEY,
            name_1c TEXT,
            name_store2 TEXT,
            name_store1 TEXT,
            name_store6 TEXT,
            name_store4 TEXT,
            name_store5 TEXT,
            name_store3 TEXT
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store2 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store3 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store6 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store1 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store5 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS store4 (
            name TEXT NOT NULL PRIMARY KEY,
            name_for_search TEXT,
            price INTEGER,
            url TEXT
            )""")
            curs.execute("""CREATE TABLE IF NOT EXISTS parsing_time (
            day DATETIME NOT NULL PRIMARY KEY,
            store2 BOOL DEFAULT False,
            store3 BOOL DEFAULT False,
            store6 BOOL DEFAULT False,
            store1 BOOL DEFAULT False,
            store5 BOOL DEFAULT False,
            store4 BOOL DEFAULT False
            )""")
            