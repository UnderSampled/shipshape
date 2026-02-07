"""Save/load game state to disk."""

import json
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import GameState

DEFAULT_SAVE_DIR = Path.home() / ".shipshape" / "saves"


def ensure_save_dir(save_dir: Path = DEFAULT_SAVE_DIR) -> Path:
    """Ensure the save directory exists."""
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def save_game(state: "GameState", slot: str = "autosave", save_dir: Path = DEFAULT_SAVE_DIR) -> Path:
    """
    Save game state to a JSON file.

    Returns the path to the saved file.
    """
    ensure_save_dir(save_dir)
    save_path = save_dir / f"{slot}.json"

    with state.lock():
        data = state.to_dict()

    with open(save_path, "w") as f:
        json.dump(data, f, indent=2)

    return save_path


def load_game(state: "GameState", slot: str = "autosave", save_dir: Path = DEFAULT_SAVE_DIR) -> bool:
    """
    Load game state from a JSON file.

    Returns True if successful, False if file not found.
    """
    save_path = save_dir / f"{slot}.json"

    if not save_path.exists():
        return False

    with open(save_path, "r") as f:
        data = json.load(f)

    # Import here to avoid circular imports
    from ..simulation.systems import ShipSystem
    from ..simulation.robots import Robot

    with state.lock():
        state.from_dict(data, ShipSystem, Robot)

    return True


def list_saves(save_dir: Path = DEFAULT_SAVE_DIR) -> list[str]:
    """List all available save slots."""
    ensure_save_dir(save_dir)
    return [p.stem for p in save_dir.glob("*.json")]


def delete_save(slot: str, save_dir: Path = DEFAULT_SAVE_DIR) -> bool:
    """Delete a save file."""
    save_path = save_dir / f"{slot}.json"
    if save_path.exists():
        save_path.unlink()
        return True
    return False
