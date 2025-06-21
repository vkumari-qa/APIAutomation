import allure

@allure.epic("Sanity Suite")
@allure.feature("Health Check")
@allure.story("Basic status test")
@allure.title("Check /health endpoint")
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json().get("status") == "up"
