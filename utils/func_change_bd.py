from loader import cursor, connect

def add_help_record(help_user_id,helper_id):
    sql_add_query = f"INSERT INTO help_user VALUES({helper_id}, {help_user_id})"
    cursor.execute(sql_add_query)
    connect.commit()

def delete_help_record(help_user_id):
    sql_delete_query = f"DELETE from help_user where id_user = {help_user_id}"
    cursor.execute(sql_delete_query)
    connect.commit()

def add_admin(id_user):
    sql_add_query = f"INSERT INTO admin VALUES({id_user})"
    cursor.execute(sql_add_query)
    connect.commit()

def delete_admin(user_id):
    sql_delete_query = f"DELETE from admin where id = {user_id}"
    cursor.execute(sql_delete_query)
    connect.commit()

def add_helper(id_user):
    sql_add_query = f"INSERT INTO helper VALUES({id_user})"
    cursor.execute(sql_add_query)
    connect.commit()

def delete_helper(user_id):
    sql_delete_query = f"DELETE from helper where id = {user_id}"
    cursor.execute(sql_delete_query)
    connect.commit()

def len_admin():
    list_admin = []
    result = cursor.execute("SELECT id FROM admin").fetchall()
    for i in range(len(result)):
        res = result[i]
        id = res[0]
        list_admin.append(id)
    return list_admin

def len_helper():
    list_helper = []
    result = cursor.execute("SELECT id FROM helper").fetchall()
    for i in range(len(result)):
        res = result[i]
        id = res[0]
        list_helper.append(id)
    return list_helper

def take_info(from_user_id):
    result = cursor.execute("SELECT user_id,user_name FROM users").fetchall()
    for i in range(len(result)):
        res = result[i]
        id,user_name = res
        if from_user_id == id:
            return user_name 

def ask_qui(id_user,text_message):
    pass