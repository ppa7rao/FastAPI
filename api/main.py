import uvicorn
from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None  # = None makes brand opticional


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {}


@app.get('/')
def home():
    return {'Data': 'Testing'}


@app.get('/items')
def get_items():
    return JSONResponse(content=inventory,
                        status_code=200)


@app.get('/item_id/{item_id}')
def get_item_by_id(item_id: int = Path(...,
                                       description='item ID you want to see')):
    return inventory.get(item_id)
    raise HTTPException(status_code=404, detail='Item not found.')


@app.get('/item_name/{name}')
def get_item_by_name(name: str = Path(...,
                                      title='Name',
                                      description='Item Name')):

    matching_items = []
    for item_id, item_info in inventory.items():
        if item_info['name'] == name:
            matching_items.append({'item_id': item_id,
                                   'item_info': item_info})

    if not matching_items:
        raise HTTPException(status_code=404,
                            detail='Item not found.')

    return matching_items


@app.post('/item/{item_id}')
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=403,
                            detail='Item already exists')

    inventory[item_id] = {
        'name': item.name,
        'price': item.price,
        'brand': item.brand
    }
    return inventory[item_id]


@app.put('/update_item/{item_id}')
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404,
                            detail='Item not found.')

    if item.name is not None:
        inventory[item_id]['name'] = item.name
    if item.price is not None:
        inventory[item_id]['price'] = item.price
    if item.brand is not None:
        inventory[item_id]['brand'] = item.brand

    return inventory[item_id]


@app.delete('/delete_item/{item_id}')
def delete_item(item_id: int = Path(...,
                                    gt=0,
                                    description='ID must be greater than zero')
                ):
    if item_id not in inventory:
        raise HTTPException(status_code=404,
                            detail='ID does not exists')
    del inventory[item_id]
    return {'Item successfully deleted!'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
