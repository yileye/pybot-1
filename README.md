# PyBot

PyBot is a work-in-progress socket messaging client that allows connecting to arbitrary hosts:ports and performing actions based on message content.

PyBot can be used to reverse engineer socket messaging protocols and was originally created as an IRC bot.

![PyBot UI](screenshot.png?raw=true "PyBot UI")

### Running

Clone this repository and :

`docker-compose up`


### Starting a basic IRC client

Navigate to http://localhost:8080 and start clicking around - see the screenshot above for defaults.

### JSON API

See the sample_api directory for a basic flask app that will read in the raw json from POST and return a `{'result':'Some text'}` that will be sent back over the wire.
