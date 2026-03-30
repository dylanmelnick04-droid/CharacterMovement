**Current Usage:**
* [main](main.py) runs the game. Projectiles can be thrown with `1` and `p` (except on map 2 *Bug*). Melee is `2` and `o`. Dash uses `shift` keys and can only be done in the air. Standard WASD and arrow keys for player movement.
  - *DEV USAGE*: `devtools` (either 'on' or 'off') in ENV controls hitboxes and screen color changes for projectile hits (and probably more later!). `arena` (bool) in ENV will encapsulate the map in an arena which cannot be fallen out of if True. `arena` should be determined by the player in the stage select.

* [revolvingQueue](stage_select/revolvingQueue.py) runs the stage select. Both `enter` keys select the stage. *Todo*: make arena determined in stage select. There will also be a winning screen, but for now we just have exit().

This project has taken aproximately `36` hours.
