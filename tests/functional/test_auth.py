
import pytest

from flight_club import db
from flight_club.models.models import User

from flask import g, session

def test_register(test_client, app):
    # The registration page works
    response = test_client.get("/auth/register")
    assert(response.status_code == 200)

    # Test registration brings to login page
    response = test_client.post("/auth/register", data={"username":"test", "password":"test"})
    assert "auth/login" in response.headers["Location"]

    with app.app_context():
        assert db.session.query(User.query.filter_by(username="test").exists()).scalar()
    
def test_login(test_client, app):
    
    with app.app_context():
        assert db.session.query(User.query.filter_by(username="test").exists()).scalar()
    
    # Check the login page works
    response = test_client.get("/auth/login")
    assert(response.status_code == 200)

    # Test ability to login
    response = test_client.post("/auth/login", data={"username":"test", "password":"test"})
    
    # Assert there was a redirect to homepage
    assert(response.status_code == 302)
    assert(response.headers["Location"] == "http://localhost/")

    # Check the session context is good
    with test_client:
        test_client.get("/")
        assert(g.username == "test")

def test_logout(test_client, app):
    # Login
    response = test_client.post("/auth/login", data={"username":"test", "password":"test"})
    
    # Logout
    with test_client:
        response = test_client.get("/auth/logout")

        # Assert there was a redirect to homepage
        assert(response.status_code == 302)
        assert(response.headers["Location"] == "http://localhost/")

        assert("user_id" not in session)


