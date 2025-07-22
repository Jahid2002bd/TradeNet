# src/utils/pattern_memory.py

"""
pattern_memory.py

Stores and retrieves rare/anomalous patterns to avoid duplicate alerts.
Uses a JSON file to persist seen pattern signatures.
"""

import json
import os
import hashlib


class PatternMemory:
    """
    Manages a persistent store of pattern hashes.
    """

    def __init__(self, filepath: str = "pattern_memory.json"):
        self.filepath = filepath
        self._load_memory()

    def _load_memory(self) -> None:
        """Load existing memory from disk or initialize empty."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self.memory = set(json.load(f))
            except (json.JSONDecodeError, IOError):
                self.memory = set()
        else:
            self.memory = set()

    def _save_memory(self) -> None:
        """Persist current memory to disk."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(list(self.memory), f)
        except IOError:
            pass  # If saving fails, skip without blocking

    @staticmethod
    def _hash_pattern(pattern_features: list[float]) -> str:
        """
        Create a deterministic hash for a pattern feature list.
        """
        raw = ",".join(f"{x:.6f}" for x in pattern_features)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def is_new_pattern(self, pattern_features: list[float]) -> bool:
        """
        Check if a pattern is unseen. If new, store its hash.

        Returns:
            bool: True if pattern was not in memory (new), False otherwise.
        """
        h = self._hash_pattern(pattern_features)
        if h in self.memory:
            return False
        self.memory.add(h)
        self._save_memory()
        return True


if __name__ == "__main__":
    # Demo usage
    mem = PatternMemory()
    sample = [0.123456, 1.234567, -0.987654]
    if mem.is_new_pattern(sample):
        print("New rare pattern! Alert user.")
    else:
        print("Pattern already seen; no alert.")
