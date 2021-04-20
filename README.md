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

### "Painter" Demo

The Painter demo was mostly used to figure out how to work with a cursor over
a video buffer.

The initial attempts basically saved the area of the cursor off-screen, and
when the cursor moved, it would redraw that area, before capturing a new area.

As the other demos progressed, Painter was check to ensure the basic functions
still worked:

* Pressing the left mouse button would 'draw' a circle on the active area.
* Pressing the right mouse button would 'draw' an "erased" circle on the same.

When the cursor was updated to use a separate layer (CameraOverlay), Painter
was tested first, and oh did that separate layer make it so much easier!

The "Painter" demo can be run by the following command, at the root directory
of the repository:

    python painter.py

### Emitter Demo

The purpose of the Emitter demo is to spam a bunch of Rays into the scene, to
find out the limitations of the current code. While about 1024 seem to be good,
there are massive slow downs, as the count ratches up from there.

I've had about 25600 without any major issue (albeit extremely slow - think
seconds per slide in a presentation, haha!), possibly more. The code
evolved over time, so I might be off by now; however, there are a few values
at the top of the demo, so feel free to play with them to really push the rays!

The "Emitter" demo can be run by the following command, at the root directory
of the repository:

    python emitter.py

### Bouncer Demo

This demonstration was created to test using a different way to track the life
of a Ray. Specifically, the number of bounces a Ray has experienced. The demo
doesn't have any additional objects in the scene, but soon (tm).

The "Bouncer" demo can be run by the following command, at the root directory
of the repository:

    python bouncer.py

### Sorter Demo

This demonstration was created in response to a Discord guild member reacting
to an image posted in the guild. The individual stated that the image of the
Emitter demo reminded them of an algorithm visualization video on YouTube, and
then linked it. After review, I thought it possible to do with what enlightened
had available at the time, and made it so; I then decided to keep it as a demo.

Currently, it visualizes [what I think is] the "bubble sort" sorting algorithm,
however, I've not verified the algorithm to be exactly the bubble sort method.

In the future, I'm thinking that the mouse wheel events could be used to cycle
between different sorting visualizations, but it'd be nice to be able to see
which sorting algorithm is currently being demonstrated. That might be one way
to interact with a camera overlay from the environment.

The "Sorter" demo can be run by the following command, at the root directory
of the repository:

    python sorter.py

