# Mini Arcade

Mini arcade is a project running old school games writen in python using pygame. There are 3 games currently in the arcade:

* Snake
* Pong
* Whackman (inspired by Pacman)


## Developers
* Brynjar Örn Grétarsson - *brynjarog17* - [github](https://github.com/brynjarorng)
* Daði Steinn Brynjarsson - *dadib17* - [github](https://github.com/dadisteinn)

## prerequisites
To be able to successfully launch this project you need to have installed **python 3.7.1**, link below. It is also very handy to have [git](https://git-scm.com/) installed to be able to follow the instructions below exactly.


## Built with
* [VS Code](https://code.visualstudio.com/Download) - Code editor
* [Python](https://www.python.org/downloads/) - Programming language
* [Pygame](https://www.pygame.org/wiki/GettingStarted) - Python library for games


## Installation
The first step is to make sure that python is installed on your system, **python 3.7.1** was used for this project. Follow the link above and choose the correct version for you OS. Make sure use python 3. The game has not been tested on python 2.

Next make sure you have the newest version of pip:
* `python3 -m pip install --upgrade pip`
or
* `python -m pip install --upgrade pip`

Next you need to install pygame, this can be done with the following command. Make sure to install the version we used for maximum stability **pygame 1.9.4**. The game will probably not run with other versions of pygame because of gfxdraw:
* `python3 -m pip install -U pygame==1.9.4 --user`
or
* `python -m pip install -U pygame==1.9.4 --user`

Further information about python or pygame can be found in the links above.

Next you need to clone the repo. Open a terminal and manouver into the appropriate directory and enter the following command:

* `git clone https://github.com/brynjarorng/Pythonic_Group_Project`

Now that everything is setup, using the terminal, navigate into *Pythonic_Group_Project* and run this command to play the game:
* `python3 ./menu.py`
or
* `python ./menu.py`


## Game assets

### Snake
Sound - Biting into apple
* **Title**: crunch.wav
* **Author**: Koops
* **Source**: (https://freesound.org/people/Koops/sounds/20279/)
* **License**: (https://creativecommons.org/licenses/by/3.0/)

### Pong
Sound - Ball collision
* **Title**: PongBlipF4.wav
* **Author**: NoiseCollector
* **Source**: (https://freesound.org/people/NoiseCollector/sounds/4359/)
* **License**: (https://creativecommons.org/licenses/by/3.0/)

### Whackman
Image - Player lives
* **Title**: heart.png
* **Author**: DontMind8
* **Source**: (https://opengameart.org/content/heart-pixel-art)
* **License**: "You can use the art commercially, You can modify or edit the art as you like"

Image - Player sprite
* **Title**: Animated Runner Character
* **Author**: irmirx
* **Source**: (https://opengameart.org/content/animated-runner-character?fbclid=IwAR3qteWqwyistdS2naXSn0ftotw_abGMhEjsGft2b9t--GaD1VlkXG7AoeQ)
* **License**: (https://creativecommons.org/licenses/by/3.0/)

Image - Ghost sprite
* **Title**: ghost[1-4].png
* **Author**: XenosNS
* **Source**: (https://opengameart.org/content/animated-blue-ghost)
* **License**: None

### Global
Font - Used for all games and menues
* **Title**: Minotaur.ttf
* **Author**: Walter Velez
* **Source**: (https://www.fontsquirrel.com/fonts/Minotaur)
* **License**: (https://www.fontsquirrel.com/license/Minotaur)
