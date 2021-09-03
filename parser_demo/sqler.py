import psycopg2

con = psycopg2.connect(
    database="database1",
    user="database1_role",
    password="database1_password",
    host="172.19.0.2",
    port="5432"
)

# con = psycopg2.connect("host=database1 dbname=database1 user=database1_role password=database1_password")
cursor = con.cursor()


def sql_insert_dict(table, dictionary):
    placeholders = ', '.join(['%s'] * len(dictionary))
    columns = '\"' + '","'.join(dictionary.keys()) + '\"'
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
    cursor.execute(sql, list(dictionary.values()))


def sql_insert_many_dict(table, columns, dict_list):
    placeholders = ', '.join(['%s'] * len(columns))
    print(placeholders)
    columns = '\"' + '","'.join(columns) + '\"'
    values = []
    for x in dict_list:
        values.append(list(x.items())[0])
    print(values)
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns, placeholders)
    cursor.executemany(sql, values)


def tutor_copy():
    sql = """
    INSERT INTO timetable_tutor (long, short)
    SELECT DISTINCT tutor_full, tutor
    FROM timetable_timetable 
    WHERE tutor_full IS NOT NULL
    ORDER BY tutor_full
    """
    cursor.execute(sql)


def delete_all(table):
    sql = 'DELETE FROM %s' % table
    cursor.execute(sql)


def save_changes():
    con.commit()

