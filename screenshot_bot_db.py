import sqlite3
from typing import Dict, Optional


class ScreenshotDatabase:
    def __init__(self, db_name: str = 'bot_config.db'):
        self.db_name = db_name
        self.init_database()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self) -> None:
        conn = self._get_conn()
        try:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS server_configs (
                    guild_id BIGINT PRIMARY KEY,
                    channel BIGINT,
                    threshold INTEGER DEFAULT 5,
                    emoji TEXT DEFAULT '⭐',
                    color TEXT DEFAULT '7276AD',
                    timezone TEXT DEFAULT 'Europe/Moscow'
                )
            ''')
            conn.commit()
        finally:
            conn.close()
        print(f"База данных {self.db_name} инициализирована")

    def get_server_config(self, guild_id: int) -> Optional[Dict]:
        conn = self._get_conn()
        try:
            row = conn.execute(
                'SELECT * FROM server_configs WHERE guild_id = ?', (guild_id,)
            ).fetchone()
            if row:
                return dict(row)
            return None
        finally:
            conn.close()

    def set_server_config(self, guild_id: int, **kwargs) -> None:
        conn = self._get_conn()
        try:
            existing = conn.execute(
                'SELECT 1 FROM server_configs WHERE guild_id = ?', (guild_id,)
            ).fetchone()

            if existing:
                fields = []
                values = []
                for key, value in kwargs.items():
                    if value is not None:
                        fields.append(f"{key} = ?")
                        values.append(value)
                if fields:
                    values.append(guild_id)
                    conn.execute(
                        f'UPDATE server_configs SET {", ".join(fields)} WHERE guild_id = ?',
                        values
                    )
            else:
                keys = ['guild_id']
                vals = [guild_id]
                for key, value in kwargs.items():
                    if value is not None:
                        keys.append(key)
                        vals.append(value)
                placeholders = ', '.join('?' for _ in keys)
                conn.execute(
                    f'INSERT INTO server_configs ({", ".join(keys)}) VALUES ({placeholders})',
                    vals
                )
            conn.commit()
        finally:
            conn.close()

    def get_config(self, guild_id: int) -> Dict:
        config = self.get_server_config(guild_id)
        if not config:
            return {
                'channel': None,
                'threshold': 5,
                'emoji': '⭐',
                'color': '7276AD',
                'timezone': 'Europe/Moscow'
            }
        return config

    def delete_server_config(self, guild_id: int) -> bool:
        conn = self._get_conn()
        try:
            cursor = conn.execute('DELETE FROM server_configs WHERE guild_id = ?', (guild_id,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
        finally:
            conn.close()

    def get_all_configs(self) -> Dict[int, Dict]:
        conn = self._get_conn()
        try:
            rows = conn.execute('SELECT * FROM server_configs').fetchall()
            return {row['guild_id']: dict(row) for row in rows}
        finally:
            conn.close()


db = ScreenshotDatabase()
