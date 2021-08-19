<p align="center">
  <h3 align="center">Comparte Ride API</h3>

  <p align="center">
    API for Comparte Ride
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
Comparte Ride, an application that allows you to connect with users who have cars and who can help you move to different places in the city.

The circles where the trip is shared are private and can be accessed only with an invitation


### Built With

*	Python 3
*	Django
*	Django REST framework
*	JWT
*	Unit test
*	Docker
*	Celery

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites for Local Development
* Python Programming Language
* Django Framework
* Django Rest Framework

### Installation 

1. Clone the repo
   ```sh
   git clone https://github.com/murtagh95/ComparteRide
   ```
2. Change directory to ComparteRide
   ```sh
   cd ComparteRide
   ```
3. Install python module dependencies
   ```sh
   pip install -r \requirements\local.txt
   ```
4. Run migrations and api server
   ```sh
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
   ```

### Using Docker Compose
1. Clone the repo
   ```sh
   git clone https://github.com/murtagh95/ComparteRide
   ```
2. Change directory to ComparteRide
   ```sh
   cd ComparteRide
   ```
3. Build containers with docker-compose
   ```sh
   docker-compose -f local.yml build
   ```
4. Start containers
   ```sh
   docker-compose -f local.yml up -d
   ```

<!-- USAGE EXAMPLES -->
## Usage

* Open http://127.0.0.1:8000/users/signup/ and register your user.
    
    You can see the email that will be sent to the confirmation client by the server logs. In it you will find the token to verify the account
    
* paste the verification token and send it to http://127.0.0.1:8000/users/verify/ 

* You can log in with the following url http://127.0.0.1:8000/users/login/.

    Copy the token that returns to be able to use the other endpoints of the application

* In the post endpoint you can change the request to GET and get all the records from the table
  
* In the code you can test the different TEST that I have created by running the command "python manage.py test"

* You can download the collection with the EndPoints in the following button.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/e4498bf067a08df8a92c?action=collection%2Fimport#?env%5BComarte%20Ride%5D=W3sia2V5IjoiYWNjZXNzX3Rva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6InVzZXJuYW1lIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6Imhvc3QiLCJ2YWx1ZSI6ImxvY2FsaG9zdDo4MDAwIiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJJRF9UT0tFTiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZX1d)

    ---------------------------------------------------o---------------------------------------------------
## Note
* The port set is 0.0.0.0:8000 but the port that must be used in the browser is 127.0.0.1:8000,
  in postman the requests are well configured and you should not modify them


<!-- CONTACT -->
## Contact

Nicolas Catalano - nec.catalano@gmail.com