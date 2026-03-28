from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app import crud, schemas, dependencies
from app.database import get_db

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=List[schemas.Product])
def read_products(
    search: Optional[str] = None,
    sort_by_quantity: Optional[str] = Query(None, regex="^(asc|desc)$"),
    filter_supplier: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(dependencies.get_current_user_optional)
):
    # Для гостя или клиента – игнорируем фильтры/сортировку/поиск
    if current_user is None or current_user.role == "client":
        products = crud.get_products(db, limit=1000)  # без параметров
    else:
        products = crud.get_products(db, search=search, sort_by_quantity=sort_by_quantity, filter_supplier=filter_supplier)
    return products

@router.get("/suppliers", response_model=List[str])
def get_suppliers(db: Session = Depends(get_db), current_user = Depends(dependencies.role_required("manager"))):
    return crud.get_suppliers(db)

@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db), current_user = Depends(dependencies.role_required("admin"))):
    return crud.get_categories(db)

@router.get("/manufacturers", response_model=List[str])
def get_manufacturers(db: Session = Depends(get_db), current_user = Depends(dependencies.role_required("admin"))):
    return crud.get_manufacturers(db)

@router.get("/units", response_model=List[str])
def get_units(db: Session = Depends(get_db), current_user = Depends(dependencies.role_required("admin"))):
    return crud.get_units(db)

@router.post("/", response_model=schemas.Product, dependencies=[Depends(dependencies.role_required("admin"))])
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.put("/{product_id}", response_model=schemas.Product, dependencies=[Depends(dependencies.role_required("admin"))])
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, product)

@router.delete("/{product_id}", dependencies=[Depends(dependencies.role_required("admin"))])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if crud.delete_product(db, product_id):
        return {"ok": True}
    raise HTTPException(status_code=400, detail="Cannot delete product: it is referenced in orders")

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """
    Возвращает товар по его ID. Используется для предзаполнения формы редактирования.
    """
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product