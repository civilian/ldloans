#!/bin/bash

# Installing the packages in another directory and creating a symbolic link because mounting the directory 
# (overlays)[https://stackoverflow.com/questions/43287999/npm-install-doesnt-work-in-docker] node_modules directory.
ln -s /build-dir/node_modules /reactjs-jwt-authentication/node_modules

exec npm start