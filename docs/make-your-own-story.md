# Make your own story

## Introduction

This application is basically reading a SQLite3 database containing the story with the paths and the items for the inventories (and possibly new features added on the run). If you want to write your own story and use it in the game, you just have to create the game database using the [../sql/](sql) instructions to fill it.

A chapter in the database can has several steps. Choosing an option will select the next chapter + step in the database.

Example : 

- Chapter 1 Step 3 : you have two options :
	+ Option 1 will redirect to Chapter 1 step 4
	+ Option 2 will redirect to Chapter 1 step 5

Here is the way I use to generate the content :

```md
## 1-1 The waking up

You wake up with a start after having the contents of a ice water bucket thrown in your face. (....)

---

Choice : 

- You give the guy what he wants
	+ 1-5
- You try to stand up to the interrogation and refuse to give information
	+ 1-3
- You say nothing and look around for an escape plan
	+ 1-2

---

### 1-2 You say nothing and look around for an escape plan

You observe the place you are in. (...)

---

Choice :

- You try to lie about the location of the camp	
	+ 1-5
- You refuse to answer
	+ 1-3

---
```

Then, I insert these content into a static database file and use it to produce the CSV file.

## Database structure

The game databse contains the following tables :

- aid : the aid items definition
- apparel : the equipment items definition
- misc : the misc items definition
- story : the game's story
- weapon : the weapons definition

### items tables

`aid`, `apparel`, `misc`, and `weapon` are basically the same tables.

- `id` : auto incremented row ID
- `name` : Item's display name
- `descr` : Item's description
- `img` : file for the item's picture, located in `static/(aid|apparel|misc|weapon)`

### story table

Columns : 

- `id` : an auto incremented row identifier
- `chapter` : the chapter number
- `step` : the step in the chapter
	+ Chapter and step are a primary key
- `text` : the step's content
- `next_chapter` : the chapter associated to the next step
- `choice_(1|2|3)` : the step's number where the player is redirected to in the story
	+ The game's currently supports 3 choices per step
	+ If the row in `NULL` (*NOT* empty, `NULL` !), the choice will be ignored
- `img` : the background image displayed in the story
- `end` : values are `0` or `1`. Default is `0`, set `1` is this choice results a game over
- `choice_(1|2|3)_descr` : the text displayed for the choice option
- `exp` : the amout of Experience the character earns by completing this step
- `loot` : the items the character obtain when completing this step
	+ Content is expected to be : `<type>:<id>` where type is the item type and id it's id in the items' database. Separated by semicolons `;` if several loots are available.
	+ Example : `weapon:1` refers to the `weapon` table, id `1`
	+ `weapon:1;misc:2` will add the weapon id 1 and misc item id 2 to the character's inventory

To end the story, just keep `next_chapter`, `choice_(1|2|3)` and the choices description `NULL`. This chapter and stepp will be the last one displayed and no further progression will be possible.

### Images processing

The template's CSS will apply the greenish render. However, the pixelated effect has been applied using GIMP's Blur => Pixelate filter.

The images are sized for a 480px width.

Sometimes if the image is too dark, you may have to increase its base brightness since the CSS filter will reduce it.