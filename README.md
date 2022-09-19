# flight_club

[![Build Status](https://travis-ci.com/drc56/flight_club.svg?branch=master)](https://travis-ci.com/drc56/flight_club) [![Coverage Status](https://coveralls.io/repos/github/drc56/flight_club/badge.svg?branch=master&service=github)](https://coveralls.io/github/drc56/flight_club?branch=master)

# Running in container
## System dependencies
1. `docker`
2. `docker-compose`

## Running Locally
1. Run:
```
docker-compose up dev
```
2. In a browser navigate to:
```
0.0.0.0:5000
```
Congrats you are now running the flight club app


## Running Tests
1. Run:
```
docker-compose build test
docker-compose run test
```
2. Review results in `results.xml` file

## Running linting 
1. Run:
```
docker-compose build lint 
docker-compose run lint
```
2. Note, this will actually edit the files that violate the black formatting rules.  If 
you instead want to fail the build to see what files require linting run:
```
docker-compose run lint black /src/flight_club --check
```
