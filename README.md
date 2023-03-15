# Pyp-Boy

Pyp-boy is a Python Flask-based text role playing game inspired by the *Fallout* lore. At the beginning of this project, the idea was to make a quick and dirty attempt to create a pip-boy for the Pinephone, but the more the development advanced, the more I've shifted to this idea.

![pypboy](screenshot.png)

## Warning

This game is still buggy and unfinished. Also, the story is currently written in French.

## Install

### Using a container (Docker, Podman..)

Pull the image.

```bash
podman pull ghcr.io/wivik/pyp-boy:v0.4.2
```

Run the container, using a volume for the /pypboy/data directory inside the container (because it stores your save file).

```bash
podman run --rm -v <somepath>:/pypboy/data -p 5000:5000 ghcr.io/wivik/pyp-boy:v0.4.2
```

Open your browser to http://localhost:5000 and enjoy.

### Using source code

Clone the repository.

Install requirements :

```bash
pip install --user requirements.txt
```

Run flask

```bash
python -m flask run
```

Open your browser to http://localhost:5000

## How to play

The first thing the web application will do is downloading the game's database available in [GitHub's release](https://github.com/Wivik/pyp-boy/releases).  The database simply contains the story and it's branches. If the a new version is available, the game will prompt for an update. The databse is stored in `./data`. If the DB has been deleted by mistake, you may just need to for to the homepage http://localhost:5000 and it will download it again.

You'll prompted to create a save file. The game saves its data in `./data/save.db` using an sqlite3 database.

Following that, you'll be asked to create your character's name. Then, select the character and click on "Load".

The menus are : 

- DATA : The game's story to follow
- STAT : Not implemented
- INV : Not implemented
- MAP : The Map tab using OSM integration, currently broken since the changes made to integrate it in the story
- SYS : The save file management

During the story, you'll be prompted to choose some actions. They can trigger variations in the story, and even a game over. Once the character is dead, the story cannot be continued and a new character must be created or the save file deleted (no menu yet for this, you need to open the sqlite db).

Your character will earn EXP and increase its level. There is currently no incidence with that.

### Future things

- The last chapter is blank, it's currently experimenting using the OSM integration for interactive maps of the Pyp-boy.
- The story does not takes account in the character's gender yet, it would be nice to implement it later.
- A story recap based on the player's choices would be nice to read it in one shot.
- The INV tab should contains the acquired stuff during the story.

## Contribute

This project is mainly a playground for coding learning for a not-developer guy. But any contributions are welcome anyway. A multilingual support could be made later to translate the story.

## Attribution

Unless other statement, this project is licensed under MIT.

Maps based on [OpenStreetMap](https://www.openstreetmap.org/), using [Leaflet](https://leafletjs.com) and [Stamenmaps](http://maps.stamen.com/#watercolor/12/37.7706/-122.3782) render.

Icons are from [Remix Icon](https://remixicon.com).
