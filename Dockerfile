FROM centos:7

# ----------------------------------------------
#               BASE INSTALLATION
# ----------------------------------------------
COPY ./base /install/base
WORKDIR /install/base
RUN ["./install_dependencies.sh"]

# ----------------------------------------------
#            ASTROMETRY INSTALLATION
# ----------------------------------------------
COPY ./astrometry /install/astrometry
WORKDIR /
RUN ["/install/astrometry/compile_astrometry.sh"]
ENV PATH="/usr/local/astrometry/bin:${PATH}"
ENV PYTHONPATH="/astrometry.net"

# ----------------------------------------------
#           POCS UTILS INSTALLATION
# ----------------------------------------------
RUN python3 -m pip install panoptes-utils

# ----------------------------------------------
#                   CLEAN UP
# ----------------------------------------------
WORKDIR /
RUN ["rm","-rf","install/"]

# ----------------------------------------------
#                RUNTIME STUFF
# ----------------------------------------------
# add any example index files:
COPY ./index/*.fits /usr/local/astrometry/data/
# add utility script for downloading index files to astrometry/bin, which is part of the path:
COPY ./index/download_index_files.sh /usr/local/astrometry/bin/

# ----------------------------------------------
#                  ENTRYPOINT
# ----------------------------------------------
WORKDIR /
CMD ["/bin/bash"]
