import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return None


def execute_sql(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except Error as e:
        print(e)


def add_book(conn, book):
    sql = '''INSERT INTO books(title, author, published_year)
             VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, book)
    conn.commit()
    return cur.lastrowid


def add_review(conn, review):
    sql = '''INSERT INTO reviews(book_id, reviewer, rating, comment)
             VALUES(?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, review)
    conn.commit()

    return cur.lastrowid


def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    return rows


def select_where(conn, table, **query):
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table: table name
    :param query: dict of attributes and values
    :return:
    """
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows


def delete_where(conn, table, **kwargs):
    qs = [f"{k}=?" for k in kwargs]
    values = tuple(kwargs.values())
    q = " AND ".join(qs)
    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")


def delete_all(conn, table):
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {table}')
    conn.commit()
    print("Deleted")


if __name__ == "__main__":
    create_books_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        published_year INTEGER
    );
    """

    create_reviews_sql = """
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY,
        book_id INTEGER NOT NULL,
        reviewer TEXT NOT NULL,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        comment TEXT,
        FOREIGN KEY (book_id) REFERENCES books(id)
    );
    """

    db_file = "library.db"

    conn = create_connection(db_file)
    if conn:
        execute_sql(conn, create_books_sql)
        execute_sql(conn, create_reviews_sql)

        book = ("Władca Pierścieni", "J.R.R. Tolkien", 1954)
        book_id = add_book(conn, book)

        review = (book_id, "Ania", 5, "Arcydzieło literatury fantasy!")
        review_id = add_review(conn, review)

        print(select_all(conn, "books"))
        print(select_all(conn, "reviews"))

        # delete_where(conn, "reviews", id=1)
        # delete_all(conn, "reviews")

        conn.close()
