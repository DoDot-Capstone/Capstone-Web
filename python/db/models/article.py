from datetime import datetime
from python.db.database import get_connection
from python.db.models.user import User
import logging
import traceback

"""
    python.user.user 의 User모델에서 get_user_info() 함수 개선 필요
    Error: Not all parameters were used in the SQL statement
    prepared Statement를 사용하면 해결되는것으로 예측
    cursor생성시 prepared = True 옵션을 부여
"""

class Article:
    def __init__(self, post_id: int, title: str, content: str, user_id: int, created_at: datetime = datetime.now(), updated_at: datetime = datetime.now()):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = created_at.strftime("%Y.%m.%d")
        self.updated_at = updated_at.strftime("%Y.%m.%d")

    @property
    def convert_json(result):
        return {
            "post_id": result.post_id,
            "title": result.title,
            "content": result.content,
            "username": User.load_username_from_user_id(result.user_id),
            "created_at": result.created_at,
            "updated_at": result.updated_at
        }

    @staticmethod
    def get_all_article(page: int = 1, count: int = 15):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                SELECT * FROM posts
                ORDER BY created_at DESC
                LIMIT {count} OFFSET {(page - 1) * count}
            """)

            results = cursor.fetchall()
            return list(map(lambda x: {
                "post_id": x[0],
                "title": x[1],
                "username": User.load_username_from_user_id(x[3]),
                "created_at": x[4].strftime("%Y년 %m월 %d일")
            }, results))
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def search_article(search_value: str, page: int = 1, count: int = 15):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                SELECT * FROM posts
                WHERE title LIKE '%{search_value}%'
                ORDER BY created_at DESC
                LIMIT {count} OFFSET {(page - 1) * count}
            """)

            results = cursor.fetchall()
            return list(map(lambda x: {
                "post_id": x[0],
                "title": x[1],
                "username": User.load_username_from_user_id(x[3]),
                "created_at": x[4]
            }, results))
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_max_page(search_value: str | None = None, count: int = 15):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            sql = "SELECT COUNT(*) FROM posts"
            if search_value:
                sql += " WHERE title LIKE '%{search_value}%'"
            cursor.execute(sql + ";")

            cnt = cursor.fetchone()
            return (cnt[0] // count) + 1
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def load_article_with_post_id(post_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                SELECT * FROM posts WHERE post_id={post_id};
            """)

            results = cursor.fetchall()
            if len(results) == 0:
                return None
            else:
                return Article(*results[0]).convert_json
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)
            
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_article(title: str, content: str, user_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO posts(title, content, user_id) VALUES ('{title}', '{content}', {user_id});
            """)
            results = cursor.fetchall()
            return 200 if len(results) == 0 else 401

        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            return 500
        
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    @staticmethod
    def delete_article(post_id: int, user_id: int):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(f"""
            SELECT * FROM posts WHERE post_id = {post_id};
            """)
            results = cursor.fetchone()
            if len(results) == 0:
                status = 401

            elif results[3] != int(user_id):
                status = 401

            else:
                cursor.execute(f"""
                    DELETE FROM posts WHERE post_id = {post_id};
                """)
                results = cursor.fetchone()
                if results is None:
                    status = 200
                else:
                    status = 401

            return status

        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            return 500

        finally:
            conn.commit()
            cursor.close()
            conn.close()