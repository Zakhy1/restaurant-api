from httpx import AsyncClient

menu_id = 1


async def test_add_menu(ac: AsyncClient):
    new_menu = {'title': 'My menu 1', 'description': 'My menu description 1'}
    response = await ac.post('/api/v1/menus', json=new_menu)
    assert response.status_code == 201
    assert response.json() == {
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'id': '1',
        'submenus_count': 0,
        'dishes_count': 0
    }


# async def test_get_menus(ac: AsyncClient):
#     response = await ac.get('/api/v1/menus/')
#     assert response.status_code == 200
#     assert response.json() == [
#         {
#             'title': 'My menu 1',
#             'description': 'My menu description 1',
#             'id': '1',
#             'submenus_count': 0,
#             'dishes_count': 0
#         }
#     ]


async def test_get_menu(ac: AsyncClient):
    response = await ac.get('/api/v1/menus/1')
    assert response.status_code == 200
    assert response.json() == {
        'title': 'My menu 1',
        'description': 'My menu description 1',
        'id': '1',
        'submenus_count': 0,
        'dishes_count': 0
    }


async def test_edit_menu(ac: AsyncClient):
    new_data = {'title': 'My updated menu 1', 'description': 'My updated menu description 1'}
    response = await ac.patch(f'/api/v1/menus/{menu_id}', json=new_data)
    assert response.status_code == 200
    assert response.json() == {
        'title': 'My updated menu 1',
        'description': 'My updated menu description 1',
        'id': '1',
        'submenus_count': 0,
        'dishes_count': 0
    }


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json() == {
        'status': True,
        'message': 'The menu has been deleted'
    }
