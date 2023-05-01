import pytest
import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_handler_with_welcome(client):
    r = client.get("/")

    assert r.json["description"] == "Welcome. Service is alive"
    assert r.json["code"] == 200


def test_handler_with_wrong_command(client):
    r = client.post("/run_command", json={"command": "dbt run || cat /etc/passwd"})

    assert r.json["description"] == "Multiple commands not allowed"
    assert r.json["code"] == 400

    r = client.post("/run_command", json={"command": "dbts test"})

    assert r.json["description"] == "Not a DBT command"
    assert r.json["code"] == 400

    r = client.post("/run_command", json={"command": "cat /etc/passwd"})

    assert r.json["description"] == "Not a DBT command"
    assert r.json["code"] == 400

