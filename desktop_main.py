import asyncio
import os
import sys
from pathlib import Path


def bundle_root():
    """Return the project root when developing, or PyInstaller's bundle root."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


ROOT = bundle_root()
SRC = ROOT / "src"

# The existing game uses asset paths relative to src/, so preserve that layout
# in the desktop bundle instead of rewriting every asset reference.
os.chdir(SRC)
sys.path.insert(0, str(SRC))

from game import Game


if __name__ == "__main__":
    asyncio.run(Game().run())
