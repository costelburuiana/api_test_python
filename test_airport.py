import allure
import requests
import os
from dotenv import load_dotenv

load_dotenv()
ENDPOINT = "https://airportgap.com/api"


headers = {}

@allure.title("Test generate token with invalid credentials")
@allure.description("Test generate token with invalid credentials")
def test_generate_token_invalid_credentials():
    
    email = "example@email.com"
    password = "Password123"
    response = requests.post(
        ENDPOINT + "/tokens", data={"email": email, "password": password}
    )
    assert response.status_code == 401

@allure.title("Test generate token with correct credentials")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Test generate token")
def test_generate_token():
    EMAIL = os.environ.get("EMAIL")
    PASSWORD = os.environ.get("PASSWORD")

    response = requests.post(
        ENDPOINT + "/tokens", data={"email": EMAIL, "password": PASSWORD}
    )
    assert response.status_code == 200

    bearer_token = response.json()["token"]
    assert bearer_token is not None
    global headers
    headers = {"Authorization": f"Bearer {bearer_token}"}

@allure.title("Test fetching all airports")
@allure.description("Test fetching all airports from API")
def test_fetch_all_airports():
    response = requests.get(ENDPOINT + "/airports")
    assert response.status_code == 1200
    assert len(response.json()) > 0

@allure.title("Test getting 'OTP' airport by ID")
@allure.description("Test fetching the airport by string ID (OTP)")
def test_gets_the_airport_by_ID():
    response = requests.get(ENDPOINT + "/airports/OTP")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == "OTP"

@allure.title("Test distance between two airports")
@allure.description("Test distance between two airports")
def test_distance_between_two_airports():
    from_airport = "OTP"
    to_airport = "BBU"

    response = requests.post(
        ENDPOINT + "/airports/distance", data={"from": from_airport, "to": to_airport}
    )
    assert response.status_code == 200

    data = response.json()
    distance_data = data["data"]
    assert distance_data

    distance = distance_data["attributes"]["kilometers"]
    assert distance > 0


@allure.title("Test adding an airport to favourites")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Test adding an airport to favourites")
def test_add_and_delete_airport_to_favourites():
    try:
        response = requests.post(
            ENDPOINT + "/favorites",
            data={"airport_id": "OTP", "note": "Biggest airport in Romania"},
            headers=headers,
        )
        assert response.status_code == 201
    except:
        # Airport already in favourites
        assert response.status_code == 500

    id = response.json()["data"]["id"]
    response = requests.get(
        ENDPOINT + f"/favorites/{id}", data={f"id": "{id}"}, headers=headers
    )
    assert response.status_code == 200

    response = requests.delete(
        ENDPOINT + f"/favorites/{id}", data={f"id": "{id}"}, headers=headers
    )
    assert response.status_code == 204

@allure.title("Test fetching all airports")
@allure.description("Test fetching all airports")
def test_returns_all_favourite_airports():
    response = requests.get(ENDPOINT + "/favorites", headers=headers)
    assert response.status_code == 200

@allure.title("Test delete all favourites airports")
@allure.description("Test delete all favourites airports")
def test_detele_all_favourite_airports():
    response = requests.delete(ENDPOINT + "/favorites/clear_all", headers=headers)
    assert response.status_code == 204
