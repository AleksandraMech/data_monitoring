import responses 
import re
from flask import url_for

from website.models import User
from playwright.sync_api import expect

#global test_home_page_loads

#test sie nie uda bo mam {% block title %}Home{% endblock %} {% block content %} zamiast  <title>Home</title>
def test_home(client):
    response = client.get("/login")
    print(response.data)
    assert b"<title>Login</title>" in response.data   #sprawdzam czy mam home w pasku karty # b to typ bite


## robic zalogowanie sie i dopiwro dodac reszte

#def test_signing_up(client, app): ##wszystkie testy musza sie zaczynac test
    #response = client.post("/sign_up", data={"email": "test@test.com", "first_name": "firstname", "password": "testpassword", "password": "testpassword"})
#
 #   with app.app_context():
  #      assert User.query.count() == 25
   #     assert User.query.first().email == "olamech2001@wp.pl" ## juz mam użytkownika nr 1 i jest to olamech2001

"""@responses.activate # it allow to mock some requests
def test_upload(client):
    responses.add(
        responses.GET,
        "https://api.agify.io",
        json={"age": 33, "count": 1049384, "name": "Anthony"},
       3 status=200
    )
    client.post("/register", data={"email": "olamech2001@wp.pl", "password": "123456789"}) ##jak chce testować coś na dalszych stronach, to najpierw musze sie zalogowac
    client.post("/login", data={"email": "olamech2001@wp.pl", "password": "123456789"})

    response = client.post("/upload", data={"file": "file"})

    assert b"You upload a file" in response.data """

#def test_take_screenshot(live_server, page):
 #   page.goto(url_for('auth.index', _external=True))
  #  page.screenshot(path="screenshots/home.png")

#..\..\..\AppData\Local\Programs\Python\Python311\Lib\multiprocessing\reduction.py:60: AttributeError
#def test_home_page_loads(live_server, page):
   # page.goto(url_for('home.index', _external=True))
    #expect(page).to_have_title("Home")

#w terminalu playwright codegen http://127.0.0.1:5000  
def test_sign_up_add_note(live_server, page):
    page.goto("http://127.0.0.1:5000/login?next=%2F")# bo to jest prawdziwy serwer a
    page.get_by_role("link", name="Sign Up").click()
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill("test@test.com")
    page.get_by_placeholder("Enter first name").click()
    page.get_by_placeholder("Enter first name").fill("Name")
    page.get_by_placeholder("Enter password").click()
    page.get_by_placeholder("Enter password").fill("password")
    page.get_by_placeholder("Confirm password").click()
    page.get_by_placeholder("Confirm password").fill("password")
    page.get_by_role("button", name="Submit").click()
    page.locator("#note").click()
    page.locator("#note").fill("Testowe dodanie notatki")
    page.get_by_role("button", name="Add Note").click() 

