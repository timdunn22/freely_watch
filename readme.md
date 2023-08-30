# About Freely Watch

This is an application that will enable people to search and watch any movie avaible online for free.

## Prerequisites

* Python 3.9 or higher
* Find needed python packages in ./requirements.txt of each project folder.

## Getting Started

Steps to build, load data from fixtures and run project:

1. `cd` to root of project
2. `docker-compose build`
4. `docker-compose up`

To test Elasticsearch in shell run these commands:
1. `docker-compose up`
2. `docker-compose exec django python manage.py shell`
