FROM node:15.7.0 as base

RUN npm install -g npm@latest

FROM base as with-requirements

# Installing the packages in another directory because mounting the directory 
# (overlays)[https://stackoverflow.com/questions/43287999/npm-install-doesnt-work-in-docker] node_modules directory.
RUN mkdir /build-dir
WORKDIR /build-dir
COPY package.json /build-dir
RUN npm install

ARG BASE_DIR
WORKDIR ${BASE_DIR}

EXPOSE 8000
CMD [ "npm", "start" ]

