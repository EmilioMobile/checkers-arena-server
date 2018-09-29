"""
SEOUL AI SCORE BOARD
Emilio Coronado, emilio.mobile@gmail.com
seoulai.com
2018
"""

import threading
import time as t
import datetime
import random
from database.sqlite.connector import connect_to_database, disconnect_database
from database.sqlite.create_table import create_table
from flask_socketio import SocketIO, emit

class Scoreboard(threading.Thread):

    def __init__(self, name="", logger=None, server=None):

        # Set the general logger
        if logger is not None:
            self.log = logger
            self.log.info('--- Starting {} Checkers Competion Scoreboard ---'.format(name))

        # Create the sqllite DB, and stock tables

        self.database = "./data/seoul_ai_openAI_hackaton.db"

        sql_create_scores_table = """ CREATE TABLE IF NOT EXISTS scores (
                                            date_time text NOT NULL,
                                            agent_name text NOT NULL,
                                            score_value real NOT NULL
                                        ); """
        isolation_level = None # sqlite autocommit
        db_connection = connect_to_database(self.database, isolation_level, logger)

        if db_connection is not None:
            # create scores table
            create_table(db_connection, sql_create_scores_table)
        else:
            logger.info("Error! cannot create the database connection.")

        # Prepare a Websocket to stream the data
        if server is not None:
            self.socketio = SocketIO(server)
            @self.socketio.on('connect')
            def test_connect():
                print('SERVER: Websocket: Client connected')

            @self.socketio.on('disconnect')
            def test_disconnect():
                print('SERVER: Websocket: Client disconnected')

            @self.socketio.on('my_event')
            def handle_message(message):
                received_message = message['data']
                print("ticker received the message: {}".format(received_message))

            self.stream = True
        else:
            self.stream = False

        threading.Thread.__init__(self)

    def select_all_scores(self, conn):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM scores")

        rows = cur.fetchall()

        for row in rows:
            print(row)

    def store_score(self, time, agent_name, score):
        """
        Create a new score in storage
        :param time:
        :param ticker_name:
        :param ticker_price:
        :return:
        """
        # Connecting to DB
        isolation_level = None # sqlite autocommit
        db_connection = connect_to_database(self.database, isolation_level, self.log)

        if db_connection is not None:
            score = (time, agent_name, score)
            sql = ''' INSERT INTO scores (date_time, agent_name, score_value) VALUES(?,?,?) '''
            cur = db_connection.cursor()
            cur.execute(sql, score)
            # Now we can disconnect from DB
            disconnect_database(db_connection, self.log)
            # self.select_all_scores(db_connection)
            return cur.lastrowid
        else:
            self.log.info("Error! cannot create the database connection.")

        return None

if __name__ == '__main__':
    print("SEOULAI HACKATON SCOREBOARD")
    scoreboard = Scoreboard("SEOULAI")
    scoreboard.start()