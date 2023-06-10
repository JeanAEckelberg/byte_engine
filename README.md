# byte_engine
Revamped base game engine for use in NDACM Byte-le Royale games.
Changes made in 2023.

## Important Changes
* GameBoard Seed Parameter
  * There is a new parameter in the GameBoard class that allows 
  a specific seed to be set. This can be used to help with testing 
  during game development.
* Avatar Class
  * The avatar class now has new implementations for an inventory 
  system. Documentation is provided in the class file.
* Vector Class
  * The Vector class is used to simplify handling coordinates. 
  Some new implementations include ways to increase the values of an already existing Vector,
  combining two Vectors to create a new one, and returning the Vector's information as 
  a tuple.
* TODO
  * GameBoard, Type hinted, Basically everything that was changed needs to be written.
  * Explain importance of type hinting, starting with pseudocode and UMLs, etc. Discuss planning process.


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
