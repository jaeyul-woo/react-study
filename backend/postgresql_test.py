import psycopg2

POSTGRESQL_IP   = "10.228.5.96"
POSTGRESQL_DB   = "postgres"
POSTGRESQL_ID   = "postgres"
POSTGRESQL_PW   = "postgres"
POSTGRESQL_PORT = "5432"

connection  = psycopg2.connect(f"""
    host={POSTGRESQL_IP}
    dbname={POSTGRESQL_DB}
    user={POSTGRESQL_ID}
    password={POSTGRESQL_PW}
    port={POSTGRESQL_PORT}
    """)
cursor      = connection.cursor()

def send_query(
    connection  : object,
    cursor      : object,
    query       : str,
    ret         : bool = True,
):
    cursor.execute(query)
    if (ret):
        return cursor.fetchall()
    else:
        connection.commit()

GET_ALL_DATABASES   = """
    SELECT datname FROM pg_database;
"""
GET_ALL_TABLES      = """
    SELECT * FROM pg_catalog.pg_tables
    WHERE schemaname != 'pg_catalog'
        AND schemaname != 'information_schema';
"""
CREATE_TABLE        = """
    CREATE TABLE {table_name}
    (
        {fields}
    );
"""
DROP_TABLE          = """
    DROP TABLE IF EXISTS {table_name}
"""

print()
print("#==== Show databases ====#")
print(send_query(connection, cursor, GET_ALL_DATABASES))
print()
print("#==== Show tables ====#")
print(send_query(connection, cursor, GET_ALL_TABLES))
print()

print("#==== Drop table ====#")
send_query(connection, cursor, DROP_TABLE.format(
    table_name  = "test_table",
), False)
print()

print("#==== Create table ====#")
fields = list()
fields.append("USER_ID SERIAL PRIMARY KEY")
fields.append("USERNAME VARCHAR(50) UNIQUE NOT NULL")
fields.append("PASSWORD VARCHAR(50) NOT NULL")
fields.append("EMAIL VARCHAR(355) UNIQUE NOT NULL")
fields.append("CREATED_ON TIMESTAMP NOT NULL")
fields.append("LAST_LOGIN TIMESTAMP")

send_query(connection, cursor, CREATE_TABLE.format(
    table_name  = "test_table",
    fields      = ",\n".join(fields),
), False)
print(send_query(connection, cursor, GET_ALL_TABLES))
print()
