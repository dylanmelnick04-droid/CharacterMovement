import pygame
import map_select.revolvingQueue_utils
from map_select.pick_map_stage import PickMapStage
from gameplay.gameplay_stage import GamePlayStage

current_stage = PickMapStage(arena=True)
running = True

while running:
    current_stage = current_stage.updateGameplay()