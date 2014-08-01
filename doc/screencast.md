
## System Setup 

### Demo system 

Ubuntu 14.04 x86_64

Almost pure, with the following changes:
 * removed useless Unity dock icons
 * cached .deb dependencies (not installed)
 * installed updates as of 1 Aug 2014

### Install Hubbub 

Install the Hubbub package corresponding to your platform.



## Pidgin Setup 

 * Enable "Hubbub" in the "Tools/Plugins" menu.
 * Enable "Off-the-Record Messaging" in the "Tools/Plugins" menu.


### Pidgin Preferences 

 * Sounds: Disable Sound Events for "Message sent"
 * Conversations: Disable "Notify buddies that you are typing to them"


## Hubbub Setup 

### Initialize Hubbub 

_These steps are to be executed in a terminal at the moment._

 * Initialize the database: "python3 -m hubbub setup"
 * Import your contacts: "python3 -m hubbub contacts"

Pidgin CLI options (setup):
 * "setup": create the database used by Hubbub for traffic analysis and contacts management. Fails if the database already exists.
 * "contacts": import contacts information from Pidgin. Can be run anytime, exits when done.

### Start Hubbub 

 * Launch Hubbub from a terminal: "python3 -m hubbub pidgin generator webui"

Pidgin CLI options (run):
 * "pidgin": bind to Pidgin for traffic logging. Do not start more than one instance.
 * "generator": start the dummy traffic generator. Do not start more than one instance.
 * "webui": start the web-based User Interface; enable/disable dummy traffic to certain friends and visualize your traffic data.


