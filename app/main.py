from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from .database import SessionLocal, engine, Base
from .models import Item
from .schemas import ItemCreate, ItemRead
from .crud import get_items, get_item, create_item, update_item, delete_item

app = FastAPI(
    title="FastAPI CRUD Example",
    description="A CRUD app with FastAPI, PostgreSQL, and Jinja2",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session

# API endpoints (OpenAPI auto-docs)
@app.get("/api/items/", response_model=list[ItemRead])
async def api_list_items(db: AsyncSession = Depends(get_db)):
    return await get_items(db)

@app.post("/api/items/", response_model=ItemRead)
async def api_create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = Item(**item.dict())
    return await create_item(db, db_item)

# HTML frontend using Jinja2
@app.get("/", response_class=HTMLResponse)
async def item_list(request: Request, db: AsyncSession = Depends(get_db)):
    items = await get_items(db)
    return templates.TemplateResponse("item_list.html", {"request": request, "items": items})

@app.get("/items/create", response_class=HTMLResponse)
async def item_create_form(request: Request):
    return templates.TemplateResponse("item_form.html", {"request": request})

@app.post("/items/create")
async def item_create(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    db_item = Item(name=name, description=description)
    await create_item(db, db_item)
    return RedirectResponse("/", status_code=303)

@app.get("/items/{item_id}", response_class=HTMLResponse)
async def item_detail(request: Request, item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("item_detail.html", {"request": request, "item": item})

@app.get("/items/{item_id}/edit", response_class=HTMLResponse)
async def item_edit_form(request: Request, item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("item_form.html", {"request": request, "item": item})

@app.post("/items/{item_id}/edit")
async def item_edit(
    request: Request,
    item_id: int,
    name: str = Form(...),
    description: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    item = await get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404)
    item_data = ItemCreate(name=name, description=description)
    await update_item(db, item, item_data)
    return RedirectResponse(f"/items/{item_id}", status_code=303)

@app.post("/items/{item_id}/delete")
async def item_delete(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404)
    await delete_item(db, item)
    return RedirectResponse("/", status_code=303)
