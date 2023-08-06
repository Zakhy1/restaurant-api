from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

menu_id = 2
submenu_id = 2
dish_id = 1


def test_add_submenu():
    new_submenu = {'title': 'My submenu 1', 'description': 'My submenu description 1'}
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json=new_submenu)
    assert response.status_code == 201
    assert response.json() == {
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'id': '2',
        'dishes_count': 0
    }


def test_add_dish():
    new_dish = {'title': 'My dish 1',
                'description': 'My dish description 1',
                'price': '12.50'}
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=new_dish)
    assert response.status_code == 201
    assert response.json() == {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50',
        'id': '1'
    }


def test_get_dishes():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200
    assert response.json() == [
        {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50',
            'id': '1'
        }
    ]


def test_get_dish():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json() == {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50',
        'id': '1'
    }


def test_edit_dish():
    new_data = {'title': 'My updated dish 1',
                'description': 'My updated dish description 1',
                'price': '14.5'}
    response = client.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=new_data)
    assert response.status_code == 200
    assert response.json() == {
        'title': 'My updated dish 1',
        'description': 'My updated dish description 1',
        'price': '14.50',
        'id': '1'
    }


def test_delete_dish():
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The dish has been deleted'
    }
