import os
from os.path import isfile

from dbInterface import DBInterface


class FileDb(DBInterface):
    def add(user_id, task) -> bool:
        p = os.path.join('data', str(user_id))
        with open(p, 'a') as f:
            f.writelines('\n')
            f.writelines(task)

        return True

    def get_list(user_id):
        tasks = list()
        p = os.path.join('data', str(user_id))
        if isfile(p):
            with open(p, 'r') as f:
                lines = (line.rstrip() for line in f)
                tasks.extend(line for line in lines if line)
        return tasks
