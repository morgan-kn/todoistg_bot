from dbInterface import DBInterface


class MemoryDB(DBInterface):
    global tasks
    tasks = dict()

    # Why would I make it static?
    def add(user_id, task) -> bool:
        v = tasks.get(user_id, list())
        v.append(task)
        tasks[user_id] = v

        return True

    def get_list(user_id) -> list:
        if tasks.get(user_id, 0) != 0:
            return tasks.get(user_id)
        return list()
