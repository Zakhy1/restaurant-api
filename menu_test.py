from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_menu():
    new_menu = {"title": "My menu 1", "description": "My menu description 1"}
    response = client.post("/api/v1/menus", json=new_menu)
    assert response.status_code == 201
    assert response.json() == {
        "id": "1", "title": "My menu 1",
        "description": "My menu description 1"
    }


def test_get_menus():
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1, "title": "My menu 1",
            "description": "My menu description 1",
        }
    ]


def test_get_menu():
    response = client.get("/api/v1/menus/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1", "title": "My menu 1",
        "description": "My menu description 1",
        "submenus_count": 0, "dishes_count": 0
    }


def test_edit_menu():
    menu_id = 1
    new_data = {"title": "My updated menu 1", "description": "My updated menu description 1"}
    response = client.patch(f"/api/v1/menus/{menu_id}", json=new_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": "1", "title": "My updated menu 1",
        "description": "My updated menu description 1",
    }


def test_delete_menu():
    menu_id = 1
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "The menu has been deleted"}
