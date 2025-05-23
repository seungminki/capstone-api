import mysql.connector

from app.schemas import RequestData

from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


def insert_posts(req: RequestData):
    query = """
    INSERT INTO posts (post_id, board_id, content, user_id)
    VALUES (%(post_id)s, %(board_id)s, %(content)s, %(user_id)s)
    """
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


def insert_categories(req: RequestData, pred_category: str):
    query = """
    INSERT INTO categories (post_id, board_id, pred_category)
    VALUES (%(post_id)s, %(board_id)s, %(pred_category)s)
    """
    conn = get_connection()
    cursor = conn.cursor(prepared=True)

    data = {
        "post_id": req.post_id,
        "board_id": req.board_id,
        "pred_category": pred_category,
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


def insert_docs(req: RequestData, rows: list):
    query = """
    INSERT INTO docs (post_id, board_id, pred_id, pred_post_id, pred_board_id, cosine_distance)
    VALUES (%(post_id)s, %(board_id)s, %(pred_id)s, %(pred_post_id)s, %(pred_board_id)s, %(cosine_distance)s)
    """
    conn = get_connection()
    cursor = conn.cursor(prepared=True)

    try:
        rows = [
            {**row, "post_id": req.post_id, "board_id": req.board_id} for row in rows
        ]

        # bulk insert
        cursor.executemany(
            query,
            rows,
        )

        conn.commit()
        print("✅ Insert 성공")

    except Exception as e:
        conn.rollback()
        print("❌ 오류 발생, 롤백 수행:", e)

    finally:
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
        database=MYSQL_DATABASE,
    )
