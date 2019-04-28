# project-hexagon

## System Requirements
- Ubuntu 16.04
- Python 2.7
- Networkx 2.3
- Visual Studio Code (optional)
  - pep8 as the linter

## Setup the environment
- Install git, pip, virtualenv
  - sudo apt update
  - sudo apt install git
  - sudo apt install python-pip
  - pip install virtualenv
- git clone https://github.com/taraprasad73/project-hexagon.git
- cd project-hexagon
- create a virtual environment
  - virtualenv -p /usr/bin/python2.7 hexagons
  - source hexagons/bin/activate
  - pip install -r requirements.txt

## Running the code
```
python hexagons.py 3 10

Use python heaxagons.py --help to see the argparse help.
```