# Oscar Chamat | ldloans project

This repository contains my Test Project, thank you for taking the time to read this documentation.
If you want me to implement some new feature, fix something or give any further detail don't hesitate on reaching me at chamatoscar@gmail.com.

## Easy testing

The easiest way to test is to connect to the server provided in the email and follow [easy-testing.md](easy-testing.md)

## Installation
Assuming you have the repository cloned already

### Requirements
This is what you need to install in your computer

* `Docker` https://docs.docker.com/install
  — Install Docker for different operating system. See documentation.
* `Docker Compose` https://docs.docker.com/compose/install/
  — Install Docker Compose for macOS, Windows, and Linux
* `cURL` https://develop.zendesk.com/hc/en-us/articles/360001068567-Installing-and-using-cURL#install
  — Install curl

### Putting enviroment file .env

Some configurations are dependant of the .env file. Then rename [.env.bk](.env.bk) to .env and if you want put the data of your bd.

### Testing the command

### Testing the api-rest
1) To run the rest service just do -> `docker-compose up`

#### Testing the api rest
* The database is added to the repository (db.sqlite3) for fast testing.

2) If you want to test in a more visual manner here is the url to the project in postman -> https://documenter.getpostman.com/view/7547562/TW6tMAnE
    - You can also see some examples of the urls.

## Implementation
I implemented the test project as a Django application and using Django Rest Framework for the API Rest.

### Implemented Features
* Docker machine with a up to date installation.
* Docker compose to make easier the user of Docker.
* Design of the Database for eficiency and simple access to data.
* Used ViewSets (Equivalent to Class Based Views) for the API View.
* An instalation in AWS is created, configuring the ports, the RDS (database), billing alarms, proper users for the database for easy testing.
* Details; documentation, private variables and methods, custom error messages and providing tool to reduce the complexity of testing.

## Design

### Entity Relationship diagram
* There has been 2 versions of the ER Diagram, thanks to the depper understanding of the problem
* To modify; https://drive.google.com/file/d/1yZk9WSLOnIvv9rz-lJvltbGkvMn_fL-7/view?usp=sharing

#### V1

![ER V1](./diagrams/mopokemonER-v1.png)

#### V2

![ER V2](./diagrams/mopokemonER-v2.png)

## Extra notes
* Different notes of design provided in the file [minor-notes.md](minor-notes.md)

## Closing
Thanks for reading this far, I wish you a good day and I'm very looking forward to an interview with you.