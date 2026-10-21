# Entry point for the browser build: pygbag needs main.py at the top level.
# The game loads assets with paths relative to src/, so run from there.
import asyncio
import os
import sys

import pygame  # noqa: F401 -- pygbag scans this file's imports to decide what to load

os.chdir("src")
sys.path.insert(0, os.getcwd())

from game import Game

asyncio.run(Game().run())
