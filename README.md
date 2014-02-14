Hubbub
======

Noise generator and traffic analysis plugin for Pidgin.

Hubbub consists of two parts : 
* `pidgin`: a DBus client that connects to Pidgin and monitors IM traffic
* `webui`: a web user interface showing stats about IM traffic

## Starting Hubbub

Open a terminal in the directory where you cloned the repository and load the `hubbub` virtualenv:

```bash
cd Path/Where/You/Will/Clone/Repositories/Hubbub
workon hubbub
```

### Pidgin plugin

Hubbub connects to Pidgin using DBus, so you can start it and stop it at anytime without restarting Pidgin. To work, Hubbub has to run on the desktop of the user that's using Pidgin.

To start the plugin, run `python hubbub pidgin`.

### Web Interface

To start the web interface, run `python hubbub webui`. You can then open you webbrowser on http://localhost:8080/ .

### Both together

You can run both the Pidgin plugin and the Web UI at the same time with `python hubbub pidgin webui`.


## Installation

First, install the [DummyMore](https://github.com/hoh/DummyMore) plugin for Pidgin. This plugin will hide dummy messages so you don't get annoyed by them.

To so, download the binary file from [the releases](https://github.com/hoh/DummyMore/releases) that fits your architecture (Linux i686 or x86_64 available) and copy it in your `~/.purple/plugins` directory.


### On Ubuntu

Packages:

```bash
sudo apt-get install python3-dev python3-dbus libxml2-dev libxslt-dev virtualenvwrapper
```

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
