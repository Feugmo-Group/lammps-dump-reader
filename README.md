# unDumper
**unDumper** is a fast and memory-efficient LAMMPS dump file reader with great developer experience.
Completely unbiased and applicable to all projects

## Features

- Generator objects to load one frame of a dump file at a time
- Capable of loading entire dumps into memory
- Supports classic, YAML and grid type dumps
- Utilizes a dictionary data structure for seamless integration with other plotting software in Python
- Completely general, with data structure generated based on your dump file

## Installation

**unDumper** is available on PyPI. Install it via pip

```bash
pip install undumper
```

## Usage

There are many ways to use **unDumper**, and here we'll cover a few examples to illustrate its versatility in your project

In all cases you start by importing the package which can be done using the following

```python
from undumper import undumper
```

From here, several functions are available. For most cases, you'll use either 'read_dump()' or 'read_whole_dump()'

```python

undumper.read_dump('dump.lammpstrj', 'classic')
undumper.read_dump('dump.grid')
undumper.read_dump('dump.yaml')
```

When using read_dump, you may or may not specify the file type. In general, leaving the second argument blank is preferred

read_dump generates a generator object which can be used in a loop as follows

```python

data = undumper.read_dump(file) #where file can be a classic, grid or yaml lammps dump file 

for snapshot in data:
    timesteps.append(snapshot["TIMESTEP"])
    positions.append([])

    for atom in snapshot["ATOMS"]:
        if atom["element"] == "Li":
            positions[-1].append([atom["xu"], atom["yu"], atom["zu"]])
```

At this point it is important to understand the structure of the dictionary that **unDumper** outputs, this applies to both the generator which returns the dictionary on each yield, and the 'read_whole_dump()' which returns a list of the following dictionaries

```python
unDumped = {'TIMESTEP':0, 'NUMBER OF ATOMS':1600, 'BOX BOUNDS':{x: [0,0], y: [0,0]. z: [0,0]}, 'ATOMS':{id: 1, 'Element': "Li", "xu": 1, "yu": 2, "zu": 3}}
```
If your dump file has more parameters for specifying an atom they will be added in a similar manor, a good idea is to print and look at what your dictionary looks like before you start working with it

All the remaining functions are generally not recomended to be used and are listed here

- 'read_classic()' 
- 'read_yaml()'
- 'read_grid()'

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This work was conducted by the Intellimatter Group under Dr. Conrard Giresse Tetsassi Feugmo at the University of Waterloo.

Special thanks to Xander Gouws for supervising this project and originating the idea behind it.

## Contact

For any questions or feedback, feel free to contact me at mu2farooqi@uwaterloo.ca

Let us know is there are any features you would like to see or if you find this project useful







