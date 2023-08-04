from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

menu_id = 2
submenu_id = 2
dish_id = 1


def test_add_submenu():
    new_submenu = {"title": "My submenu 1", "description": "My submenu description 1"}
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=new_submenu)
    assert response.status_code == 201
    assert response.json() == {
        "id": "2", "title": "My submenu 1",
        "description": "My submenu description 1"
    }


def test_add_dish():
    new_dish = {"title": "My dish 1",
                "description": "My dish description 1",
                "price": "12.50"}
    response = client.post(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", json=new_dish)
    assert response.status_code == 201
    assert response.json() == {
        "id": "1", "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.5"
    }


def test_get_dishes():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1, "title": "My dish 1",
            "description": "My dish description 1",
            "price": 12.5,
            'submenu_id': 2
        }
    ]

    def test_get_dish():
        response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
        assert response.status_code == 200
        assert response.json() == {
            "id": "1", "title": "My dish 1",
            "description": "My dish description 1",
            "price": "12.5",
        }

    def test_edit_dish():
        new_data = {"title": "My updated dish 1",
                    "description": "My updated dish description 1",
                    "price": "14.5"}
        response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", json=new_data)
        assert response.status_code == 200
        assert response.json() == {
            "id": "1", "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": "14.5"
        }

    def test_delete_dish():
        response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
        assert response.status_code == 200
        assert response.json() == {"status": True, "message": "The menu has been deleted"}
