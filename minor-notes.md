## To implement
- Protect the api with nginx.

## Comment structure
- Comments that are obvious after the first read of the code should not be kept in the code augmenting the cognitive load and the time spent reading the code of the developers.
    They can be kept in this file.

## Investigating the frontend docker image
- The creation of the image is a little troublesome, the package versions are not runnable in the ubuntu default configuration, so to save time (and see the limitations and habilities of buildpack-deps:stretch that is a debian) I use the node:15.7.0 base image.

- npm install gives a lot of problems seen that; 
    - you can't install them globally by design 
    - when you mount the directory in which the source code is sopposed to go node_modules is deleted.
    - Different ways to install are investigated and tested;
        - linking them and copying them in a [command](https://stackoverflow.com/questions/38425996/docker-compose-volume-on-node-modules-but-is-empty), 
        - using NODE_PATH, all of them don't work, 
        - the only solution is a custom [command.sh](./reactjs-jwt-authentication/command.sh) that makes sure that the local directory has a simbolic link to an external installation of node_modules.

## Investigating the docker image

- https://pythonspeed.com/articles/base-image-python-docker-images/
- It's investigated to take advantange of a previous investigation that has been done for the previous job. Where i updated all the versions (from the SO base image to all the versions in requirements.txt).
- I realize that the python images come from debian but again I choose Ubuntu because the community is bigger and the errors are fixed faster because of that. More importantly i have previously solved various bugs in the ubuntu machine which will help alocating resources(time) in the problem at hand.
- The building of the image may be slower but this in a real world example will be optimized by creating a base image with everything we need and uploading that to a registry of our own.
- The version of the base image is 18.04 and not 20.04 to take advantange of the longer release/debugging time passed in the community.

## Building rest-service image / [Dockerfile](./flask-jwt-auth/Dockerfile)
- To fix Python.h includes and compilations when including packages that need to be compiled.
        `RUN apt-get -y install python3.8-dev`

- Python 3.8 is currently being improved (https://devguide.python.org/#status-of-python-branches) and have a longer possible life (https://endoflife.date/python) whitout being too new.
    `RUN apt-get -y install python3.8`

- The BASE_DIR is configured from the docker-compose to make the image creation more flexible.
    `ARG BASE_DIR`

-  The directory of the project it's defined as the default directory of vagrant; from the source (/) so;
        `(ENV BASE_DIR=/ldloans)`
    - Even if the Operating System changes the structure of the project is kept.
    - Also is not directed to home(~) to make paths shorter and not dependant on a particular user

## Using the image / docker-compose

- The code is shared, not copied, to the container to:
    - speed the build of the image for development(now the code is small and is not a problem look at assumptions)
    - Being able to use the IDE of your choice in the host Operating System.

## Choosed names
- ldloans is choosed as a project name to slighly protect the anonimity of the project and that it's not easily copied.

## Documentation
- The style is choosen from pep 257 https://www.python.org/dev/peps/pep-0257#multi-line-docstrings

## Design decisions
- It is decided to use https://realpython.com/token-based-authentication-with-flask/#route-setup code because it's a great base to implement the requirements. The license is MIT therefore the code can be modified with no problems. The versions of the libraries are updated.
    - The code in the blog post helps with a structure that has been thought out by a flask code expert.
    - When updating the versions some changes have to be made.
    - The blog post gives a great way to understand and even implement different basic parts of flask such as blueprints or testing those.

- By testing and improving the code of flask-jwt-auth i see that unittest package fails in a really porly documented manner, i always have to go to the method to realize what happent that's why i prefer pytest.

- The same aproach to start from a aplication with some code is done for the client side of the application.

## Debug

### Debug commands of the manage.py
You need to run Visual Studio Code with the remote extension (https://code.visualstudio.com/docs/remote/remote-overview) in the ldloans_rest-service container, in the /ldloans directory. Make sure you have put your breakpoints (https://code.visualstudio.com/docs/editor/debugging). Then run inside the container the command:

    `$ python -m debugpy --wait-for-client --listen 0.0.0.0:5678 ./manage.py`
And start the debugger from the menu that Visual Studio Code provides.

### Debug a single test
Is basically the same as " Debug commands of the manage.py" with the remote visual studio code but run the individual test

    `$ python -m debugpy --wait-for-client --listen 0.0.0.0:5678  project/tests/test_user_model.py`

## Kown errors

### Windows
- If the container frontend does not want to build go the file explorer in the directory of the project reactjs-jwt-authentication and delete the file node_modules

### Linux
- ERROR: for rest-service  Cannot start service rest-service: OCI runtime create failed: container_linux.go:370: starting container process caused: exec: "/command.sh": permission denied: unknown