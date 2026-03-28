from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.utils import save_image
from app.dependencies import role_required
from app.crud import get_products, get_categories, get_manufacturers, get_units, get_product
from app.database import get_db
from sqlalchemy.orm import Session
from app import schemas
from typing import List


router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.post("/image", dependencies=[Depends(role_required("admin"))])
async def upload_image(file: UploadFile = File(...)):
    try:
        path = await save_image(file, resize=(300,200))
        return {"path": path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# app/api/products.py – дополнение к существующему коду

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Возвращает товар по его ID. Используется для предзаполнения формы редактирования.
    """
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/categories", response_model=List[str])
def get_categories_up(
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin"))
):
    """
    Возвращает список всех категорий товаров. Доступно только администратору.
    """
    return get_categories(db)


@router.get("/manufacturers", response_model=List[str])
def get_manufacturers_up(
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin"))
):
    """
    Возвращает список всех производителей. Доступно только администратору.
    """
    return get_manufacturers(db)


@router.get("/units", response_model=List[str])
def get_units_up(
    db: Session = Depends(get_db),
    current_user = Depends(role_required("admin"))
):
    """
    Возвращает список всех единиц измерения. Доступно только администратору.
    """
    return get_units(db)