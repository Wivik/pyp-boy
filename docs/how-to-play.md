# How to play

The first thing the web application will do is downloading the game's database available in [GitHub's release](https://github.com/Wivik/pyp-boy/releases).  The database simply contains the story and it's branches and various items definitions and story-related elements. If the a new version is available, the game will prompt for an update. The database is stored in `./data`. If the DB has been deleted by mistake, you may just need to  the homepage http://localhost:5000 and it will download it again.

## New game

You'll prompted to create a save file. The game saves its data in `./data/save.db` using an sqlite3 database.

Following that, you'll be asked to create your character's name. Then, select the character and click on "Load".

## Load game

At any time you may reload the saved progression. Each step in the story is saved, you don't have any risk of losing your progress in case of a game crash for any reason.

If the game's session is lost, you'll be asked to reload the saved data.

## Game interface

The menus are :

- DATA : This is where the game's story is played
	+ Journey : That's the current game's progression
	+ Log : The full story, so far in your progression
- STAT : Not implemented
- INV : The items you've collected through the story
	+ Weapon : the weapons you've collected during the exploration
	+ Apparel : the equipment you have
	+ Aid : some support items
	+ Misc : various kind of items, the Key items are expected to trigger side quests when the feature will be implemented
- MAP : The Map tab using OSM integration, currently broken since the changes made to integrate it in the story. This tab is currently useless and possibly broken.
- SYS : The save file management
	+ New : create a new game
	+ Load : load an existing save.

## Gameplay

During the story, you'll be prompted to choose some actions. They can trigger variations in the story, and even a game over. Once the character is dead, the story cannot be continued and a new character has to be created or the save file deleted (no menu yet for this, you need to open the sqlite db and delete the lines in table).

Your character will earn EXP and increase its level. There is currently no incidence with that.

The items has no incidence yet on the gameplay.

There is no fighting mechanics.

Side quests iniated by Key Items are intended to be implemented later.

For now, in case of a game over, the save file will be locked. A checkpoint reset mechanic should be implemented later.

