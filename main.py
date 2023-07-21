from fastapi import FastAPI
from menu import crud as menu_crud
from menu.schema import Menu as MenuSchema

app = FastAPI()


# Меню
@app.get("/api/v1/menus")
async def get_menus():
    menus = menu_crud.get_menus()
    return {"menus": [menus]}


@app.post("/api/v1/menus")
async def add_menu(menu: MenuSchema):
    result = menu_crud.add_menu_item(menu)
    return result


@app.patch("/api/v1/menus/{menu_id}")
async def edit_menu(menu_id: int, new_data: MenuSchema):
    result = menu_crud.edit_menu_item(menu_id, new_data)
    return {"menu": result}


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(menu_id: int):
    deleted_item = menu_crud.delete_menu_item(menu_id)
    return {"menu": deleted_item}
