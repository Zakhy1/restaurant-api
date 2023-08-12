from httpx import AsyncClient

menu_id = 2
submenu_id = 1


async def test_add_menu(ac: AsyncClient):
    new_menu = {'title': 'My menu 1', 'description': 'My menu description 1'}
    response = await ac.post('/api/v1/menus', json=new_menu)
    assert response.status_code == 201
    assert response.json() == {
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'id': '2',
        'submenus_count': 0,
        'dishes_count': 0
    }


async def test_add_submenu(ac: AsyncClient):
    new_submenu = {'title': 'My submenu 1', 'description': 'My submenu description 1'}
    response = await ac.post(f'/api/v1/menus/{menu_id}/submenus', json=new_submenu)
    assert response.status_code == 201
    assert response.json() == {
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'id': '1',
        'dishes_count': 0
    }


async def test_get_submenus(ac: AsyncClient):
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200
    assert response.json() == [
        {
            'title': 'My submenu 1',
            'description': 'My submenu description 1',
            'id': '1',
            'dishes_count': 0
        }
    ]


async def test_get_submenu(ac: AsyncClient):
    response = await ac.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json() == {
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'id': '1',
        'dishes_count': 0
    }


async def test_edit_submenu(ac: AsyncClient):
    new_data = {'title': 'My updated submenu 1', 'description': 'My updated submenu description 1'}
    response = await ac.patch(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}', json=new_data)
    assert response.status_code == 200
    assert response.json() == {
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1',
        'id': '1',
        'dishes_count': 0
    }


async def test_delete_submenu(ac: AsyncClient):
    response = await ac.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The submenu has been deleted'
    }
