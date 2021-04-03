# enlightened

A collection of PyGame demos for toying around with ray-based stuff.

## Virtual Environment

I use Python virtual environments when writing and testing code, as visible
with the `.dev/` entry in the [.gitignore](.gitignore) file.

Therefore, I suggest recreating a virtual environment, in the same folder as
the cloned repository:

    python -m venv .dev

Note: You might prefer a different one, and if you don't intend to contribute,
feel free to use whatever folder name you'd like. If you do intend to throw a
bit of code towards the project, please remember to include that directory in
the [.gitignore](.gitignore) file.

### Environment Activation

Once the `venv` module prepares a virtual environment folder, you'll need to
activate it:

    source .dev/bin/activate

(or whatever folder name you are using).

## Installing Requirements

The `venv` module will install `pip`, a tool very useful for installing and
maintaining requirements, or dependencies, of projects. Of course, you can add
requirements individually, or via a specially-crafted file. This file, also
included, is the [requirements.txt](requirements.txt) file, which `pip` can
automatically generate (recommended):

    pip freeze > requirements.txt

`pip` is also able to read what it generates and install them, so when you have
activated your virtual environment, you can just invoke the following command:

    pip install -r requirements.txt


## Demonstrations

This project comes witth a number of demonstration programs, akin or similar to
the tech demonstration idea. A demonstration should highlight a particular goal
in mind, which should be accomplishable, and maintainable, for as long as it is
feasible to do so.

### Original Invocation

The `launcher.py` class imported the targeted demo to be run, and thusly could
be invoked to run that demo by simply calling the following command in the root
directory of the repository:

    python launcher.py

This method is still supported, and will be so, as the following methods are a
little too.. tedious to continually type. I could theoretically figure it out,
but that would likely require having an `enlightened` subdirectory.. and I'm a
bit wary of that.

### Individual Invocation

As I have yet to still grasp how to perform relative imports, it is not as
simple as double-clicking an individual demonstration's Python program file.
Instead, these demonstrations can be invoked directly, by utilizing the `-m`
parameter|command-line-switch of `python`:

    python -m demos.[$demoNameSansExtension]

It's nice to see an example as well, so to run the Painter demonstration, one
would execute:

    python -m demos.painter

Remember: Do not include the file extension for this method of invocation!

## "Painter" Demo

The Painter demo was mostly used to figure out how to work with a cursor over
a video buffer.

The initial attempts basically saved the area of the cursor off-screen, and
when the cursor moved, it would redraw that area, before capturing a new area.

As the other demos progressed, Painter was check to ensure the basic functions
still worked:

* Pressing the left mouse button would 'draw' a circle on the active area.
* Pressing the rightt mouse button would 'draw' an "erased" circle on the same.

When the cursor was updated to use a separate layer (CameraOverlay), Painter
was tested first, and oh did that separate layer make it so much easier!

In addition to the line in `launcher.py`, the "Painter" demo can be run by the
following command, at the root directory of the repository:

    python -m demos.painter

## Emitter Demo

The purpose of the Emitter demo is to spam a bunch of Rays into the scene, to
find out the limitations of the current code. While about 1024 seem to be good,
there are massive slow downs, as the count ratches up from there.

I've had about 25600 without any major issue (albeit extremely slow - think
seconds per slide in a presentation, haha!), possibly more. The code
evolved over time, so I might be off by now; however, there are a few values
at the top of the demo, so feel free to play with them to really push the rays!

In addition to the line in `launcher.py`, the "Emitter" demo can be run by the
following command, at the root directory of the repository:

    python -m demos.emitter

## Bouncer Demo

This demonstration was created to test using a different way to track the life
of a Ray. Specifically, the number of bounces a Ray has experienced. The demo
doesn't have any additional objects in the scene, but soon (tm).

In addition to the line in `launcher.py`, the "Bouncer" demo can be run by the
following command, at the root directory of the repository:

    python -m demos.bouncer

