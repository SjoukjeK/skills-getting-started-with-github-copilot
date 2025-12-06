import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Kies een bestaande activiteit en een uniek e-mailadres
    activity = "Chess Club"
    email = "testdeelnemer@mergington.edu"

    # Zorg dat de deelnemer niet in de lijst staat
    client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Aanmelden
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Dubbel aanmelden moet fout geven
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400

    # Uitschrijven
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert email in response.json()["message"]

    # Nogmaals uitschrijven moet fout geven
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 404
