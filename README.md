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
