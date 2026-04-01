**Current Usage:**
* [main](main.py) runs the game. Projectiles can be thrown with `1` and `p`. Melee is `2` and `o`. Dash uses `shift` keys and can only be done in the air. Standard WASD and arrow keys for player movement.
  - *DEV USAGE*: `devtools` (either 'on' or 'off') in ENV controls hitboxes and screen color changes for projectile hits (and probably more later!). `arena` (bool) in ENV will encapsulate the map in an arena which cannot be fallen out of if True. `arena` should be determined in the loading screen (options are something like 1v1, arena, endless (infinite lives), options, etc). This has yet to be implemented. Current character select options are: `fireball`, `throwing_knife`, `thor`, `name_of_the_wind` (big Pat Rothfuss fan - read his stuff). Those options should be passed into [GamePlayStage](gameplay/gameplay_stage.py) via `player1_character` and `player2_character`. `MAP` `arena` and `lives` are already functional. While in development, switching between stages can be done with either `enter` key.

* [revolvingQueue](stage_select/revolvingQueue.py) runs the stage select. Both `enter` keys select the stage.

**Stage Changing**:
`current_stage` determines which stage is running. Between stages 1-4, `current_stage` is updated via a return in the class stage (see [gameplay_stage](gameplay/gameplay_stage.py) and [pick_map_stage](map_select/pick_map_stage.py) for examples).

*TODO*:
- start page
- character select page
- fourth character animation

This project has taken aproximately `39` hours.
