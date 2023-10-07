# Food_delivery_project
This project made with Django REST Framework on backend and will be added with React on frontend (future addition). 

User can register, create your account and choose user_type - Customer, Courier, Cook or Manager.
For booking purpose user can add your card with validate card number.

Manager can add new menu items, update and delete ones.

<i>Future plans:</i> <br />
I want to implement orders logic, user can order some food and couriers can deliver it to users.


## Table of Contents

- [About](#about)
- [Technologies](#technologies)
- [Getting Started](#getting-started)
- [Installing](#installing)
- [Usage](#usage)
- [Contributing](#contributing)

## About 

The main goal is to learn how to build RESTful API with DRF. 
Test all urls with services Postman and Insomnia, and also with TestCase.


## Technologies
Project is created with:
* Django: 4.2.4
* Вjango Rest Framework: 3.14.0
* Faker

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Clone project to your local machine  <br /> 
`git clone https://github.com/AlexMiller93/Food_delivery_project.git`

`cd Food_delivery_project`

<i>For Windows</i>

Creating virtual env <br />
`python3 -m venv venv`

Activating virtual env <br />
`.venv\Scripts\activate`

<i>For Linux/Mac</i>

Creating virtual env <br />
`python3 -m venv venv`

Activating virtual env <br />
`source venv/bin/activate`

### Installing

Install all needed packages <br />
`pip install -r requirements.txt`

## Usage

To synchronize the database sqlite3 <br />
`python manage.py migrate`

To run server <br />
`python manage.py runserver`

To test accounts app<br />
`python manage.py test accounts`

<i>Authentication staff</i>

Create superuser 
`python manage.py createsuperuser`

To register new user run <br />
`http://localhost:8000/users/register`

To login user run <br />
`http://localhost:8000/users/login`

<i>Admin urls</i>

Login as superuser and watch all users: <br />
`http://localhost:8000/users/admin`

To watch all accounts run: <br />
`http://localhost:8000/users/admin/accounts/`

To watch one account run using pk <br />
`http://localhost:8000/users/admin/accounts/<int:pk>`

To watch all user's cards <br />
`http://localhost:8000/users/admin/cards/`

<i>Menu urls</i>

To read all menu items and add new one run: <br />
`http://localhost:8000/menu`

To read menu item via pk run: <br />
`http://localhost:8000/menu/<int:pk>`

<i>Accounts urls</i>

To add new account run: <br />
`http://localhost:8000/users/accounts/add`

To watch user account run: <br />
`http://localhost:8000/users/accounts/<int:pk>`

<i>Cards urls</i>

To add new card run: <br />
`http://localhost:8000/users/cards`

To read, update and delete user card run: <br />
`http://localhost:8000/users/cards/<int:pk>`



### Contributing
