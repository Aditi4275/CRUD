from sqlalchemy.future import select
from .models import Item

async def get_items(db):
    result = await db.execute(select(Item))
    return result.scalars().all()

async def get_item(db, item_id: int):
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()

async def create_item(db, item):
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def update_item(db, item, data):
    item.name = data.name
    item.description = data.description
    await db.commit()
    await db.refresh(item)
    return item

async def delete_item(db, item):
    await db.delete(item)
    await db.commit()
