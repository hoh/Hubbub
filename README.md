Hubbub
======

Noise generator and traffic analysis plugin for Pidgin.

Hubbub consists of three parts : 
* `pidgin`: a DBus client that connects to Pidgin and monitors IM traffic
* `generator`: a generator that sends dummy messages via Pidgin through DBus
* `webui`: a web user interface showing stats about IM traffic

## Starting Hubbub

Open a terminal in the directory where you cloned the repository and load the `hubbub` virtualenv:

```bash
cd Path/Where/You/Will/Clone/Repositories/Hubbub
workon hubbub
```

### Create the SQLite database file

_Only run this command after the initial installation of after deleting the database file:_

```bash
python hubbub setup
```

### Pidgin plugin

Hubbub connects to Pidgin using DBus, so you can start it and stop it at anytime without restarting Pidgin. To work, Hubbub has to run on the desktop of the user that's using Pidgin.

To start the plugin, run `python hubbub pidgin`.

### Dummy traffic generator

To start the dummy traffic generator, run `python hubbub generator`.

### Web Interface

To start the web interface, run `python hubbub webui`. You can then open you webbrowser on http://localhost:8080/ .

### All together

You can run the Pidgin plugin, the dummy traffic generator and the Web UI at the same time with `python hubbub pidgin generator webui`.


## Installation

First, install the [Hubbub-Pidgin](https://github.com/hoh/Hubbub-Pidgin) plugin for Pidgin. This plugin will hide dummy messages so you don't get annoyed by them.

To so, download the binary file from [the releases](https://github.com/hoh/DummyMore/releases) that fits your architecture (Linux i686 or x86_64 available) and copy it in your `~/.purple/plugins` directory.

Do forget to enable the plugin in the Pidgin menu.

### On Ubuntu

Packages:

```bash
sudo apt-get install python3-dev python3-dbus libxml2-dev libxslt-dev virtualenvwrapper
```

Open a new terminal to enable _virtualenvwrapper_. If you don't, you will get the error `mkvirtualenv: command not found`.

Create a Python virtualenv:
```bash
mkvirtualenv --system-site-packages --python=/usr/bin/python3 hubbub
```

Optional: For the Web UI, install Python dependencies from within the virtualenv*:
```
pip install --upgrade tumulus
```

_You know that you are in the 'hubbub' virtualenv if your prompt starts with '(hubbub)'._

### All platforms

Clone the repository:

```bash
cd Path/Where/You/Will/Clone/Repositories/
git clone https://github.com/hoh/Hubbub.git
```

Install the libraries:
```
cd Hubbub
pip install -r requirements.txt
```
