
## Overview

This is a stripped down fork of [dm90/astrometry](https://hub.docker.com/r/dm90/astrometry/).
The image has astrometry.net and panoptes utils installed.

In order to run the docker container you will need to set two environment variables,

* ASTROMETRY_INDEX_DATA
* ASTROMETRY_INPUT_DATA

The first should point to a directory containing the relevant astronomety.net index files needed to process your images.
The second should point to a directory containing the data you want to process.

To launch the docker container simply run,

```
cd /path/to/astrometry
docker-compose up
```

Then attach to the container,

`docker attach astrometry_astrometry_1`

## Building
To build the docker image locally run the following command from the top level repository directory,

```
cd /path/to/astrometry
docker build -t astrometry -f Dockerfile .
```
