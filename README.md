# Science Hack Day project
## 15.-16.10.2016
This is a two player game of boxing.

# Installation pre-requisites
Make sure you have git, python3 and python-virtualenv.
## Debian based and Ubuntu based
`sudo apt-get install git python3 python-virtualenv`
## Arch based
`sudo pacman -S git python3 python-virtualenv`
## Windows
Have fun. :)

# Installation
First clone the repository with
`git clone https://github.com/MKolman/SHD-2016.git`
Now enter the repository and create a python virtualenv
`virtualenv venv -p $(which python3)`


# Playing the game
Run `./run_dev` to run a flask development server on your local machine.
Connect 4 phones to your ip on port 5000, e.g. `192.168.1.23:5000`.

Select the player and hand position for each phone. On your computer select
`Watch game!` in order to see the game play.

The phones will indicate their position with colours. Red for attack position,
blue for neutral position and green for blocking position. In order to block
enemy hits both hands have to be in blocking position.
