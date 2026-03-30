**Current Usage:**
* [main](main.py) runs the game. Projectiles can be thrown with `1` and `p` (except on map 2 *Bug*). Melee is `2` and `o`. Dash uses `shift` keys and can only be done in the air. Standard WASD and arrow keys for player movement.
  - *DEV USAGE*: `devtools` (either 'on' or 'off') in ENV controls hitboxes and screen color changes for projectile hits (and probably more later!). `arena` (bool) in ENV will encapsulate the map in an arena which cannot be fallen out of if True. `arena` should be determined in the loading screen (options are something like 1v1, arena, free for all, options, etc).

* [revolvingQueue](stage_select/revolvingQueue.py) runs the stage select. Both `enter` keys select the stage.

**Stage Changing**:
`current_stage` determines which stage is running. Between stages 1-4, `current_stage` should be updated via a return in the class stage (see [gameplay_stage](gameplay/gameplay_stage.py) and [pick_map_stage](stage_select/pick_map_stage.py) for examples).

This project has taken aproximately `36` hours.
