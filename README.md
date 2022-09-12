# pyignition-renpy

## What?

An attempt to provide more functionality for particle generation in `Ren'Py` by refactoring the `PyIgnition` library.

## Why?

While Ren'Py _does_ include a `sprite` and sprite generation funtionality, neither are well documented for common usage.

Additionally, to implement any type of particle physics requires writing all of the math code to make a particle animation usable. This creates a difficult challenge for those less math inclined (like myself).

PyIgnition appears to contain a lot of that "math" code already, and can hopefully be bootstrapped to work with Ren'Py sprite generation in some manner, even if just for the logic.

## How?

The PyIgnition library -- which was originally created for `pygame` -- is 99.9% pure Python. There are only a couple of interaction points with `pygame` directly, which look to be replacable with `renpy` functionality.

Granted, the PyIgnition code to intiate the particle generation is a bit verbose, but is much much less than rolling your own maths.

# Status

__IN PROGRESS | SEEKING CONTRIBUTORS__

This project is being posted in hopes that others with more knowledge of both Ren'Py and Python would like to jump in and see if they can make it tick.

The code has been gone over line for line and I have found a couple pain points that I am unable to solve currently due to my minimal knowledge of both Ren'Py and Python (which will hopefully change in the near future). I've also removed some functionality that is not relevant, or is unable to be supported in Ren'Py (as far as I understand).

In a couple of cases I had to update code for Python 3, so I am not completely positive that they still work the same, though the module does load without error now. Comments are active for the handful of places where these changes took place.

One of the main issues is how to "pump" the event loop, as well as some rendering calls. You can view these issues with more detail on the Github issue tracker.

If you are a coder who likes a challenge, then I welcome you. I feel that something like this would benefit all users of Ren'Py, so thank you in advance if you answer the call.

Of course this could just be a fools errand. :)

# Files

In the project the current refactor is in the directory `pyignition` and the original code (and some examples) in the directory `pyignition_original`.

The `scripts.rpy` is taken from a Ren'Py project and shows an example of initiating `pyignition` as per the documentation. This file should be considered "out of context" as you would need to move the file (and the `pyignition` directory) to a new Ren'Py `game` project directory to work on it fully. There is also a `particle.png` in the `images` directory which can be used for development.

__NOTE:__ _The `obstacles.py` is not being used at this time due to some `pygame` calls that don't seem to be able to be replaced. The file has been left "just in case" but is not the focus at this time.  All references have been stripped out in the refactored code._

# Resources

[PyIgnition](https://launchpad.net/pyignition)

[Ren'Py Sprites Docs](https://www.renpy.org/doc/html/sprites.html)

[Ren'Py Particle Source](https://github.com/renpy/renpy/blob/master/renpy/display/particle.py)
