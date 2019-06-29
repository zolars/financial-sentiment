import pymysql


class MySQL:
    def __init__(self):
        # Connect to MySQL
        self._conn = pymysql.connect(
            host='localhost',  # mysql server address
            port=3306,  # port num
            user='root',  # username
            passwd='root',  # password
            db='finance',
            charset='utf8',
        )
        self._cur = self._conn.cursor()

    def __del__(self):
        self._conn.close()

    def insert(self, sql, data):
        effect_rows = self._cur.execute(sql, data)
        self._conn.commit()
        return effect_rows
