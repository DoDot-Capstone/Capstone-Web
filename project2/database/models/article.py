from datetime import datetime
from database.mysql import get_connection
from database.models.user import User
import logging
import traceback

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
            "user_id": User.load_username_from_user_id(result.user_id),
            "created_at": result.created_at,
            "updated_at": result.updated_at
        }

    @staticmethod
    def load_all_article():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM posts;
            """)

            results = cursor.fetchall()
            return list(map(lambda x: Article(*x).convert_json, results))
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def load_article_with_post_id(post_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT * FROM posts WHERE post_id={post_id};
            """)

            results = cursor.fetchall()
            print(results[0])
            return Article(*results[0]).convert_json
        
        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert_article(title: str, content: str, user_id: int):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO posts(title, content, user_id) VALUES ('{title}', '{content}', {user_id});
            """)
            results = cursor.fetchall()
            conn.commit()
            return len(results) is not None

        except Exception as e:
            logging.error(f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}")
            exit(1)

        finally:
            cursor.close()
            conn.close()