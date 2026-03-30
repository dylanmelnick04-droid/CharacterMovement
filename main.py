import pygame
import numpy as np
import stage_select.revolvingQueue_utils
from stage_select.pick_map_stage import PickMapStage
from gameplay.gameplay_stage import GamePlayStage

current_stage = PickMapStage()
running = True

while running:
    current_stage = current_stage.updateGameplay()