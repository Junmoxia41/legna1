import os
import sqlite3
from datetime import datetime

from models.memory import Memory
from models.observation import Observation


class Database:

    def __init__(self):

        self.database_folder = "database"

        self.database_name = "memory.db"

        self.database_path = os.path.join(
            self.database_folder,
            self.database_name
        )

        print("Database inicializada.")

    def initialize(self):

        if not os.path.exists(self.database_folder):

            os.makedirs(self.database_folder)

            print("Carpeta database creada.")

        else:

            print("Carpeta database encontrada.")

        if not os.path.exists(self.database_path):

            print("Base de datos no encontrada.")

            self.create_database()

        else:

            print("Base de datos encontrada.")

    def create_database(self):

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            self.create_memories_table(cursor)
            self.create_observations_table(cursor)
            self.create_conversations_table(cursor)
            self.create_metadata_table(cursor)

            self.initialize_metadata(cursor)

        print("Base de datos creada correctamente.")

    # =========================================================
    # TABLAS
    # =========================================================

    def create_memories_table(self, cursor):

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            memory_type TEXT NOT NULL,

            category TEXT,

            content TEXT NOT NULL

        )
        """)

    def create_observations_table(self, cursor):

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS observations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            detector TEXT NOT NULL,

            memory_type TEXT NOT NULL,

            category TEXT,

            canonical_key TEXT NOT NULL,

            content TEXT NOT NULL,

            importance INTEGER NOT NULL,

            confidence REAL NOT NULL,

            polarity TEXT,

            persistence INTEGER DEFAULT 0,

            timestamp TEXT NOT NULL

        )
        """)

    def create_conversations_table(self, cursor):

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            summary TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

    def create_metadata_table(self, cursor):

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (

            key TEXT PRIMARY KEY,

            value TEXT

        )
        """)
        
        # Tabla de Identidad Personal (Protegida)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_identity (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Tabla de Preferencias de UI y Sistema
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_preferences (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

    # =========================================================
    # IDENTITY
    # =========================================================

    def save_identity_data(self, key, value):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO user_identity (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            """, (key, value))

    def get_full_identity(self):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT key, value FROM user_identity")
            return dict(cursor.fetchall())

    # =========================================================
    # METADATA
    # =========================================================

    def initialize_metadata(self, cursor):

        cursor.execute("""
        INSERT OR IGNORE INTO metadata (key, value)

        VALUES (?, ?)
        """, ("schema_version", "1"))

    # =========================================================
    # MEMORIES
    # =========================================================

    def save_memory(self, memory):

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute("""
            INSERT INTO memories (

                memory_type,
                category,
                content

            )

            VALUES (?, ?, ?)
            """, (

                memory.memory_type,

                memory.category,

                memory.content

            ))

    def load_memories(self):

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute("""
            SELECT

                id,
                memory_type,
                category,
                content

            FROM memories
            """)

            rows = cursor.fetchall()

            memories = []

            for row in rows:

                memories.append(

                    Memory(

                        memory_type=row[1],

                        category=row[2],

                        content=row[3]

                    )

                )

            return memories

    # =========================================================
    # OBSERVATIONS
    # =========================================================

    def save_observation(self, observation):

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute("""

            INSERT INTO observations (

                detector,

                memory_type,

                category,

                canonical_key,

                content,

                importance,

                confidence,

                polarity,

                persistence,

                timestamp

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            """, (

                observation.detector,

                observation.memory_type,

                observation.category,

                observation.canonical_key,

                observation.content,

                observation.importance,

                observation.confidence,

                observation.polarity,

                observation.persistence,

                observation.timestamp.isoformat()

            ))

    def load_observations(self):

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute("""

            SELECT

                id,

                detector,

                memory_type,

                category,

                canonical_key,

                content,

                importance,

                confidence,

                polarity,

                persistence,

                timestamp

            FROM observations

            """)

            rows = cursor.fetchall()

            observations = []

            for row in rows:

                observations.append(

                    Observation(

                        observation_id=row[0],

                        detector=row[1],

                        memory_type=row[2],

                        category=row[3],

                        canonical_key=row[4],

                        content=row[5],

                        importance=row[6],

                        confidence=row[7],

                        polarity=row[8],

                        persistence=row[9],

                        timestamp=datetime.fromisoformat(row[10])

                    )

                )

            return observations

    def remove_observation(self, observation_id):

        with sqlite3.connect(self.database_path) as connection:

            cursor = connection.cursor()

            cursor.execute("""

            DELETE FROM observations

            WHERE id = ?

            """, (

                observation_id,

            ))

    def clear_expired_observations(self):

        pass