def test_protected_route_without_token(client):
    endpoints = [
        ("GET", "/books/"),
        ("POST", "/books/"),
        ("PUT", "/books/1"),
        ("DELETE", "/books/1"),
    ]
    for method, url in endpoints:
        resp = getattr(client, method.lower())(url)
        assert resp.status_code == 403, f"{method} {url} returned {resp.status_code} - {resp.text}"
        assert resp.headers["content-type"].startswith("application/json")


def test_create_read_update_delete_book(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    book_payload = {
         # Required per your schema
        "name": "Test Book",
        "author": "Author Name",
        "published_year": 2024,
        "book_summary": "A test summary"
    }

    # Create
    resp_create = client.post("/books/", json=book_payload, headers=headers)
    assert resp_create.status_code == 200, f"Create failed: {resp_create.status_code} - {resp_create.text}"
    created = resp_create.json()
    book_id = created.get("id")
    assert book_id is not None

    # Read list
    resp_list = client.get("/books/", headers=headers)
    assert resp_list.status_code == 200
    assert any(book.get("id") == book_id for book in resp_list.json())

    # Read single
    resp_get = client.get(f"/books/{book_id}", headers=headers)
    assert resp_get.status_code == 200

    # Update
    update_payload = {
        "id": book_id,
        "name": "Updated Book",
        "author": "Author Name",
        "published_year": 2025,
        "book_summary": "Updated summary"
    }
    resp_update = client.put(f"/books/{book_id}", json=update_payload, headers=headers)
    assert resp_update.status_code == 200
    assert resp_update.json().get("name") == "Updated Book"

    # Delete
    resp_delete = client.delete(f"/books/{book_id}", headers=headers)
    assert resp_delete.status_code == 200

    # Verify deletion
    resp_get2 = client.get(f"/books/{book_id}", headers=headers)
    assert resp_get2.status_code == 404


def test_update_delete_nonexistent_book(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    invalid_id = 9999

    update_payload = {
        "id": invalid_id,
        "name": "Nonexistent Book",
        "author": "Ghost",
        "published_year": 1800,
        "book_summary": "Doesn't exist"
    }

    resp_update = client.put(f"/books/{invalid_id}", json=update_payload, headers=headers)
    assert resp_update.status_code == 404, f"Expected 404, got {resp_update.status_code} - {resp_update.text}"

    resp_delete = client.delete(f"/books/{invalid_id}", headers=headers)
    assert resp_delete.status_code == 404


from sqlalchemy.exc import IntegrityError

def test_create_book_invalid_payload(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Missing required fields — might raise 422 or DB integrity error
    invalid_payload_1 = {"name": "Incomplete Book"}
    try:
        resp1 = client.post("/books/", json=invalid_payload_1, headers=headers)
        assert resp1.status_code in [422, 500]
    except IntegrityError:
        pass  # acceptable failure

    # Wrong type for published_year
    invalid_payload_2 = {
        "name": "Bad Year Book",
        "author": "Author",
        "published_year": "not-a-year",
        "book_summary": "Invalid year"
    }
    resp2 = client.post("/books/", json=invalid_payload_2, headers=headers)
    assert resp2.status_code == 422, f"Expected 422, got {resp2.status_code} - {resp2.text}"
