import datetime
import sqlite3
from sqlite3 import Error

database = 'example1.db'


def create_connection(db_file):
    """ creates database connection to the SQLite database db_file
    :param db_file: database file
    :return: connection object or None
    """
    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create table from create_table_sql statement
    :param conn: connection object
    :param create_table_sql: create table statement
    :return:
    """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_project(conn, project):
    """
    create a new project to insert into table
    :param conn:
    :param project:
    :return:
    """

    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    c = conn.cursor()
    c.execute(sql, project)
    conn.commit()

    return c.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    c = conn.cursor()
    c.execute(sql, task)
    conn.commit()

    return c.lastrowid


def create_table(database):

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                        ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create tables
    if conn := create_connection(db_file=database):
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        create_table(conn, sql_create_tasks_table)
    else:
        print(r'Error. Could not create database connection to {database}', database)


def update_task(conn, task):
    """
    update task status, end_date
    :param conn:
    :param task:
    :return:
    """
    sql = ''' UPDATE tasks
              SET status_id = ? ,
                  end_date = ? 
              WHERE id = ?'''
    c = conn.cursor()
    c.execute(sql, task)
    conn.commit()


def delete_project(conn, id):
    """
    Delete the project given by project id
    :param conn:
    :param id:
    :return:
    """
    sql = 'DELETE FROM projects WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def main():

    conn = create_connection(database)

    """ create tables """
    # with conn:
    #     project = ('New project', '2020-08-03', '2030-08-04')
    #     project_id = create_project(conn, project)
    #
    #     task_1 = ('Make example sqlite', 1, 1, project_id, '2020-08-03', '2020-08-04')
    #     task_2 = ('Make more example sqlite', 1, 1, project_id, '2020-08-03', '2020-08-04')
    #
    #     create_task(conn, task_1)
    #     create_task(conn, task_2)

    """ update task table """
    # with conn:
    #     task_update = (3, '2020-08-03', 2)
    #     update_task(conn, task_update)

    """ delete data """
    with conn:
        delete_project(conn, 1)


if __name__ == '__main__':
    main()
