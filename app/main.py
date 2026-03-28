from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import auth, products, orders, pickup_points, upload
import os

app = FastAPI(title="Shoe Shop")

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(pickup_points.router)
app.include_router(upload.router)

# Простые HTML-страницы (рендеринг)
from fastapi import Request

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/products")
def products_page(request: Request):
    return templates.TemplateResponse("products.html", {"request": request})

@app.get("/orders")
def orders_page(request: Request):
    return templates.TemplateResponse("orders.html", {"request": request})

@app.get("/product_form")
def product_form_page(request: Request):
    return templates.TemplateResponse("product_form.html", {"request": request})

@app.get("/order_form")
def order_form_page(request: Request):
    return templates.TemplateResponse("order_form.html", {"request": request})