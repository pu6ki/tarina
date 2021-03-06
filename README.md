[![Heroku](http://heroku-badge.herokuapp.com/?app=tarina&style=flat&root=/static/images/default.jpg)](https://tarina.herokuapp.com/api/register)

![Logo](https://raw.githubusercontent.com/pu6ki/tarina/master/client/images/tarina_logo.jpg)


# tarina

**tarina** is a web application where you can post a story and wait to see how others will continue it, or you can contribute to the story of someone else.
This is the project of team PU6KI for the school hackathon HackTUES 3.


## Tech

The app is written in Python (Django) and JavaScript mainly. It uses a number of open-source projects to work properly:

* [Django](https://github.com/django/django) - A really nice high-level Python web framework
* [Django REST Framework](https://github.com/tomchristie/django-rest-framework) - Framework for building REST APIs in Django
* [django-cors-headers](https://github.com/ottoyiu/django-cors-headers) - Django app for handling the server headers required for Cross-Origin Resource Sharing (CORS)
* [drf-nested-routers](https://github.com/alanjds/drf-nested-routers) - Nested routing for DRF
* [django-vote](https://github.com/shanbay/django-vote) - Simple Django app to conduct vote for a model.
* [jQuery](https://github.com/jquery/jquery) - New Wave JavaScript
* [navigo](https://github.com/krasimir/navigo) - Minimalistic JavaScript router
* [live-server](https://github.com/tapio/live-server) - A small HTTP web server with live reload
* [handlebars](https://github.com/wycats/handlebars.js/) - Semantic templates for JavaScript
* [materialize-css](https://github.com/Dogfalo/materialize) - CSS Framework based on Material design.


## Getting started

How to copy this project to your local machine and run it:

1. Download a copy from GitHub:

    ```
    $ git clone https://github.com/pu6ki/tarina.git
    $ cd tarina/
    ```

2. Setup Django requirements:

    ```
    $ pip3 install -r requirements.txt
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    ```

3. Create a superuser:

    ```
    $ python3 manage.py createsuperuser
    ```

4. Run the tests:

    ```
    $ python3 manage.py test
    ```

5. Run the `live-server`:

    ```
    $ cd client/
    $ live-server
    ```


## API urls

* /api/register
* /api/login
* /api/profile/{user_id} - *Profile view.*
* /api/story - *List of all stories.*
* /api/story/personal - *Personal story list.*
* /api/story/trending - *Trending stories.*
* /api/story/{story_id} - *Story detail.*
* /api/story/{story_id}/storylines - *Story lines of a story.*
* /api/story/{story_id}/storylines/{storyline_id} - *See a certain story line.*
* /api/story/{story_id}/vote - *Vote for a story.*
* /api/story/{story_id}/unvote*
* /api/story/{story_id}/block/{user_id} - *Block user from posting story lines.*
* /api/story/{story_id}/unblock/{user_id}


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.