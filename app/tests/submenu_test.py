from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

menu_id = 2
submenu_id = 1


def test_add_menu():
    new_menu = {"title": "My menu 1", "description": "My menu description 1"}
    response = client.post("/api/v1/menus", json=new_menu)
    assert response.status_code == 201
    assert response.json() == {
        "id": "2", "title": "My menu 1",
        "description": "My menu description 1"
    }


def test_add_submenu():
    new_submenu = {"title": "My submenu 1", "description": "My submenu description 1"}
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=new_submenu)
    assert response.status_code == 201
    assert response.json() == {
        "id": "1", "title": "My submenu 1",
        "description": "My submenu description 1"
    }


def test_get_submenus():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1, "title": "My submenu 1",
            "description": "My submenu description 1",
            "menu_id": 2
        }
    ]


def test_get_submenu():

    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": "1", "title": "My submenu 1",
        "description": "My submenu description 1",
        "dishes_count": 0
    }


def test_edit_submenu():
    new_data = {"title": "My updated submenu 1", "description": "My updated submenu description 1"}
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json=new_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": "1", "title": "My updated submenu 1", "description": "My updated submenu description 1",
    }


def test_delete_submenu():
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "The menu has been deleted"}
