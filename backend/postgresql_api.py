import datetime

from flask import jsonify
import psycopg2

# PostgreSQL
DB_IP       = "10.228.5.96"
DB_NAME     = "postgres"
DB_ID       = "postgres"
DB_PW       = "postgres"
DB_PORT     = "5432"
DB_CONFIG   = f"""
    host        = {DB_IP}
    dbname      = {DB_NAME}
    user        = {DB_ID}
    password    = {DB_PW}
    port        = {DB_PORT}
"""

# PostgreSQL Grammar
GET_TABLES = """
    SELECT
        table_schema || '.' || table_name
    FROM
        information_schema.tables
    WHERE
        table_type = 'BASE TABLE'
    AND
        table_schema NOT IN ('pg_catalog', 'information_schema');
"""
GET_TABLE_DESCRIPTION = """
    SELECT
        column_name, data_type, character_maximum_length, column_default, is_nullable
    FROM
        INFORMATION_SCHEMA.COLUMNS
    WHERE
        table_name = '{table_name}';
"""
CREATE_TABLE = """
    CREATE TABLE {table_name}
    (
        {fields}
    );
"""
DROP_TABLE = """
    DROP TABLE IF EXISTS {table_name};
"""
INSERT_DATA = """
    INSERT INTO
        {table_name} {table_columns}
    VALUES
        {table_data};
"""
#TODO#
GET_DATA = """
    SELECT
        *
    FROM
        {table_name}
"""
DROP_DATA = """
    DELETE FROM
        {table_name}
    WHERE
        USER_ID = {index};
"""

TABLE_CONFIG = {
    "test_table"    : {
        "table_format" : """
            USER_ID     SERIAL          PRIMARY KEY,
            USERNAME    VARCHAR(50)     UNIQUE  NOT NULL,
            PASSWORD    VARCHAR(50)             NOT NULL,
            EMAIL       VARCHAR(355)    UNIQUE  NOT NULL,
            CREATED_ON  TIMESTAMP               NOT NULL,
            LAST_LOGIN  TIMESTAMP
        """,
        "table_columns" : """
            (USERNAME, PASSWORD, EMAIL, CREATED_ON, LAST_LOGIN)
        """,
        "table_data"    : """
            ('{username}', '{password}', '{email}', '{created_on}', '{last_login}')
        """
    },
}

def get_connection() -> object:
    return psycopg2.connect(DB_CONFIG)

def get_tables() -> tuple:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(GET_TABLES)
        table_list = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return {"table_list" : table_list}, 200
    except Exception as e:
        return {"error" : str(e)}, 500

def get_table_description(
    table_name  : str,
) -> tuple:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(GET_TABLE_DESCRIPTION.format(
            table_name  = table_name,
        ))
        table_description = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return {"table_description" : table_description}, 200
    except Exception as e:
        return {"error" : str(e)}, 500

def create_table(
    table_name      : str,
    table_format    : str,
) -> str:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(CREATE_TABLE.format(
            table_name  = table_name,
            fields      = table_format,
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {"status" : "Table created"}, 200
    except Exception as e:
        return {"error" : str(e)}, 500

def drop_table(
    table_name  : str,
) -> str:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(DROP_TABLE.format(
            table_name  = table_name,
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {"status" : "Table dropped"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

def insert_data(
    table_name      : str,
    table_columns   : str,
    table_data      : list,
) -> tuple:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(INSERT_DATA.format(
            table_name      = table_name,
            table_columns   = table_columns,
            table_data      = table_data,
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {"status" : "Data inserted"}, 200
    except Exception as e:
        return {"error" : str(e)}, 500

def get_data(
    table_name  : str,
    num_rows    : int   = 0,
    fields      : list  = None,
) -> tuple:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(GET_DATA.format(
            table_name  = table_name,
        ))
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return {"rows" : rows}, 200
    except Exception as e:
        return {"error" : str(e)}, 500

def drop_data(
    table_name  : str,
    index       : int,
) -> tuple:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(DROP_DATA.format(
            table_name  = table_name,
            index       = index,
        ))
        conn.commit()
        cur.close()
        conn.close()
        return {"status" : "Data deleted"}, 200
    except Exception as e:
        return {"error" : str(e)}, 500

if (__name__ == "__main__"):
    table_name = "test_table"

    print(create_table(
        table_name      = table_name,
        table_format    = TABLE_CONFIG["test_table"]["table_format"],
    ))
    print(get_tables())
    print(get_table_description(
        table_name  = table_name,
    ))
    print(insert_data(
        table_name      = table_name,
        table_columns   = TABLE_CONFIG["test_table"]["table_columns"],
        table_data      = TABLE_CONFIG["test_table"]["table_data"].format(
            username    = "id",
            password    = "pw",
            email       = "email@email.com",
            created_on  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            last_login  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ),
    ))
    print(insert_data(
        table_name      = table_name,
        table_columns   = TABLE_CONFIG["test_table"]["table_columns"],
        table_data      = TABLE_CONFIG["test_table"]["table_data"].format(
            username    = "id1",
            password    = "pw2",
            email       = "asd@asd.com",
            created_on  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            last_login  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ),
    ))
    print(get_data(
        table_name  = table_name,
    ))
    print(drop_data(
        table_name  = table_name,
        index       = 1,
    ))
    print(get_data(
        table_name  = table_name,
    ))
    print(drop_table(
        table_name  = table_name,
    ))
    print(get_tables())