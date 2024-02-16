from fastapi.testclient import TestClient
import main

client = TestClient( main.app )


def test_read_main_correct():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "--> mega super duper FastAPI sample contacts  <--"}


def test_read_main_incorrect():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() != {"message": "--> Hello World! <--"}
