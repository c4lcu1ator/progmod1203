from dataclasses import dataclass
from enum import Enum


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class Category:
    id: int | None
    name: str


@dataclass
class Recipe:
    id: int | None
    name: str
    difficulty: Difficulty
    category_id: int | None
