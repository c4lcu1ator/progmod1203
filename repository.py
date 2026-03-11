import sqlite3
from typing import Optional

from models import Recipe, Difficulty


class RecipeRepository:
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection

    def get_by_id(self, recipe_id: int) -> Optional[Recipe]:
        cur = self._conn.cursor()
        cur.execute(
            """
            SELECT id, name, difficulty, category_id
            FROM recipes
            WHERE id = ?
            """,
            (recipe_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return Recipe(
            id=row[0],
            name=row[1],
            difficulty=Difficulty(row[2]),
            category_id=row[3],
        )

    def create(self, recipe: Recipe) -> int:
        cur = self._conn.cursor()
        cur.execute(
            """
            INSERT INTO recipes(name, difficulty, category_id)
            VALUES (?, ?, ?)
            """,
            (recipe.name, recipe.difficulty.value, recipe.category_id),
        )
        new_id = cur.lastrowid
        return new_id
