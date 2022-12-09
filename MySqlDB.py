import mysql.connector

from dbInterface import DBInterface
import time
from logger import logger


class MySqlDB(DBInterface):
    global cnx
    cnx = mysql.connector.connect(user='root', database='todoist', password='root')

    # Why would I make it static?
    def add(user_id, task) -> int:
        cursor = cnx.cursor()
        add_task_query = ("INSERT INTO tasks "
                        "(name, user_id, priority, created_at, updated_at) "
                        "VALUES (%s, %s, 0, now(), now())")
        data_task = (task, user_id)
        cursor.execute(add_task_query, data_task)
        task_id = cursor.lastrowid
        cnx.commit()
        return task_id

    def get_list(user_id) -> list:
        logger.info("Get tasks for user. user_id={}".format(user_id))

        cursor = cnx.cursor()
        query = ("SELECT task_id, name FROM tasks ORDER BY priority DESC, name ASC")
        cursor.execute(query)

        result = []
        for (task_id, name) in cursor:
            logger.info("Task '{}' '{}'".format(task_id, name))
            result.append(name)

        return result

    def set_priority(user_id, task_id, priority) -> None:
        logger.info("Update priority of task for user. user_id={}, task_id={}".format(user_id, task_id))

        cursor = cnx.cursor()
        query = ("UPDATE tasks SET priority = %s WHERE user_id = %s AND task_id = %s")
        cursor.execute(query, (priority, user_id, task_id))
        cnx.commit()
