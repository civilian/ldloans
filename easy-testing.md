## Requirements

* `Postman` https://www.postman.com/downloads/
    — Install Postman for different operating system.

## Testing the Api Rest
* Go to the project https://documenter.getpostman.com/view/7547562/TW6wKUbd and get it to run in postman
* In the folder aws are all the calls that you can to the developed api.

### Api Rest running the tests
* If you connect to the server with the command and the key provided in the mail, you can also review the 
tests. First go to the ldloans directory (`cd ~/ldloans`) and then you can run the tests with with:
  `docker-compose run rest-service python manage.py test`

## Testing the frontend
* Go to the url http://ec2-34-233-128-227.compute-1.amazonaws.com
* With the credentials

| User          | Password    |
|---------------|-------------|
| user@user.com | password    |

* Go to the page create-loan-application and see what happens if you ask for a project with requested_amount > 50000, requested_amount == 50000 and requested_amount < 50000
* Also if you ask for the same loan in less than an hour the api rest service will tell you that you need to wait an hour.
* The frontend can also report you when the server is failing or when there are different problems with the backend.
* There is also included the ability to sign new users and to see their data.