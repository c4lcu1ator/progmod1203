import sqlite3

import pytest

from models import Recipe, Difficulty
from repository import RecipeRepository


def _insert_category(conn, name: str) -> int:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO categories(name) VALUES (?)",
        (name,),
    )
    return cur.lastrowid


def _insert_recipe(conn, name: str, difficulty: str, category_id: int | None) -> int:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO recipes(name, difficulty, category_id) VALUES (?, ?, ?)",
        (name, difficulty, category_id),
    )
    return cur.lastrowid


def test_get_by_id_success(db_connection):
    cat_id = _insert_category(db_connection, "Soups")
    recipe_id = _insert_recipe(db_connection, "Borscht", "medium", cat_id)

    repo = RecipeRepository(db_connection)

    result = repo.get_by_id(recipe_id)

    assert result is not None
    assert result.id == recipe_id
    assert result.name == "Borscht"
    assert result.difficulty == Difficulty.MEDIUM
    assert result.category_id == cat_id


def test_create_success(db_connection):
    cat_id = _insert_category(db_connection, "Desserts")
    repo = RecipeRepository(db_connection)

    recipe = Recipe(
        id=None,
        name="Cheesecake",
        difficulty=Difficulty.HARD,
        category_id=cat_id,
    )

    new_id = repo.create(recipe)
    stored = repo.get_by_id(new_id)

    assert stored is not None
    assert stored.name == "Cheesecake"
    assert stored.difficulty == Difficulty.HARD
    assert stored.category_id == cat_id


def test_create_invalid_enum(db_connection):
    cat_id = _insert_category(db_connection, "Main")
    repo = RecipeRepository(db_connection)

    bad_recipe = Recipe(
        id=None,
        name="Strange dish",
        difficulty="impossible",  # type: ignore
        category_id=cat_id,
    )

    with pytest.raises(sqlite3.IntegrityError):
        repo.create(bad_recipe)


def test_create_invalid_fk(db_connection):
    repo = RecipeRepository(db_connection)

    recipe = Recipe(
        id=None,
        name="Orphan dish",
        difficulty=Difficulty.EASY,
        category_id=999999,
    )

    with pytest.raises(sqlite3.IntegrityError):
        repo.create(recipe)


def test_get_by_id_not_found(db_connection):
    repo = RecipeRepository(db_connection)

    result = repo.get_by_id(999999)

    assert result is None
