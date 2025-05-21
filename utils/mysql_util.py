import mysql.connector

from app.schemas import RequestData

from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD


def insert_post(req: RequestData):
    query = create_insert_query()
    conn = get_connection()
    cursor = conn.cursor(prepared=True)

    data = {
        "post_id": req.post_id,
        "board_id": req.board_id,
        "content": req.content,
        "user_id": req.user_id,
    }

    try:
        cursor.execute(query, data)
        conn.commit()
        print("✅ 게시글 삽입 성공")
    except mysql.connector.Error as e:
        conn.rollback()
        print(f"❌ 삽입 실패: {e}")
    finally:
        cursor.close()
        conn.close()


def create_insert_query():
    return """
    INSERT INTO posts (post_id, board_id, content, user_id)
    VALUES (%(post_id)s, %(board_id)s, %(content)s, %(user_id)s)
    """


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database="smki_capstone_db",
    )
