# byte_engine
Revamped base game engine for use in NDACM Byte-le Royale games.
Changes made in 2023.

## Important Changes

* Overall Change
  * Every file is now type hinted to facilitate the coding process. For future development,
  type hint any changes made for the same reason.
  

* Item Changes
  * The item class has extra parameters. You can now define an item's durability, its value
  for different uses (e.g., sell pricing), and a stack size system. Refer to the class for 
  a more detailed explanation.


* GameBoard Class
  * GameBoard Seed Parameter
    * There is a new parameter in the GameBoard class that allows 
    a specific seed to be set. This can be used to help with testing during game development.
  * Map Size Parameter
    * This is a Vector object that is not used as a coordinate, but the dimensions of the 
    entire game map. Vectors are explained later.
  * Locations Parameter
    * This parameter allows for user-defined specifications of where to put certain GameObjects 
    on the game map. It is an extensive system used to do this, so refer to the file for 
    further documentation.
  * Walled Parameter
    * This is a boolean that determines whether to place Wall objects on the border of the game 
    map.


* Occupiable Class
  * A new class was implemented called Occupiable. This class inherits from GameObject and 
  allows for other GameObjects to "stack" on top of one another. As long as an object inherits 
  this class, it can allow for many objects to be located on the same Tile.

 
* Tile Class
  * The Tile class inherits from Occupiable, allowing for other GameObjects to stack on top of
  it. A Tile can be used to represent the floor or any other basic object in the game.


* Wall Class
  * The Wall class is a GameObject that represent an impassable object. Use this object to help 
  define the borders of the game map.


* Stations
  * Station Class
    * The Station represents a basic Station. They can contain items and be interacted with.
  * Occupiable Station
    * Occupiable Stations represent basic Station objects that can be occupied by another 
    GameObject.
  * Example Classes
    * The occupiable_station_example, station_example, and station_receiver_example classes 
    are provided to show how their respective files can be used. These can be deleted or used
    as templates on how to expand on their functionality. 


* Action Class
  * This is a class to represent the actions a player takes each turn in object form. This is 
  not implemented in this version of the engine since enums are primarily used.


* Avatar Class
  * The avatar class now has new implementations for an inventory 
  system. Documentation is provided in the class file.


* Enums File
  * This file has every significant object being represented as an enum. There are also enums
  that help with the avatar's inventory system. Refer to the file for a note on this.


* Player Class
  * The player class now receives a list of ActionType enums to allow for multiple actions 
  to happen in one turn. The enum representation can be replaced with the Action object 
  if needed.


* Controllers
  * Interact Controller Class
    * This class controls how players interact with the environment and other GameObjects.
  * Inventory Controller Class
    * This class controls how players select a certain item in their inventory to then 
    become their held item.
  * Master Controller
    * This controller is used to manage what happens in each turn and update the 
    overarching information of the game's state.


* Generate Game File
  * This file has a single method that's used to generate the game map. The 
  generation is slow, so call the method when needed. Change the initialized 
  GameBoard object's parameters as necessary for the project.
  
 
* Vector Class
  * The Vector class is used to simplify handling coordinates. 
  Some new implementations include ways to increase the values of an already existing Vector,
  adding two Vectors to create a new one, and returning the Vector's information as 
  a tuple.


* Congif File
  * The most notable change in this file is MAX_NUMBER_OF_ACTIONS_PER_TURN. It is used for 
  allowing multiple actions to be taken in one turn. Adjust as necessary.


## Development Notes

* Type Hinting
  * Type hinting is very useful in Python because it prevents any confusion on
  what type an object is supposed to be, what value a method returns, etc. Make 
  sure to type hint any and everything to eliminate any confusion.
* Planning
  * When planning, it's suggested to write out pseudocode, create UMLs, and any 
  other documentation that will help with the process. It is easy to forget what 
  is discussed between meetings without a plan. 
  * Write everything that should be implemented, 
  what files need to be created, their purpose in the project, and more. UML diagrams 
  help see how classes will interact and inherit from each other. 
  * Lastly, documentation is a great method to stay organized too. Having someone to 
  write what is discussed in meetings can be useful; you won't easily lose track of 
  what's discussed.



## How to run

```bash
.\build.bat - will build your code (compile, pretty much)

python .\launcher.pyz g - will generate a map 

python .\launcher.pyz r - will run the game
```

## Required Python Version

- Requires Python 3.11 due to type of Self

## Test Suite Commands:

```bash
python -m game.test_suite.runner
```

## Manual

[Usage Manual](https://docs.google.com/document/d/1MGxvq5V9yGJbsbcBgDM26LugPbtQGlyNiaUOmjn85sc/edit?usp=sharing)

Referenced Examples - https://github.com/topoftheyear/Byte-le-Game-Examples

## Previous Byte-le Competitions

2018 - Dungeon Delvers - https://github.com/jghibiki/Byte-le-Royale-2018

2019 - Space Denizen - https://github.com/topoftheyear/Byte-le-Royale-2019

2020 - Disaster Dispatcher - https://github.com/PixPanz/byte_le_royale_2020

2021 - Traveling Trailsmen - https://github.com/PixPanz/byte_le_royale_2021

2022 - FarTech - https://github.com/HagenSR/byte_le_royale_2022

2023 - Undercooked - https://github.com/amanda-f-ndsu/byte_le_royale_2023
