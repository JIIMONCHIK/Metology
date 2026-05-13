from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import crud, schemas, dependencies
from app.database import get_db

router = APIRouter(prefix="/api/orders", tags=["orders"])


# Менеджер и админ могут просматривать заказы
@router.get("/", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(dependencies.role_required("manager")),  # manager или admin
):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


# Администратор может создавать заказ
@router.post(
    "/",
    response_model=schemas.Order,
    dependencies=[Depends(dependencies.role_required("admin"))],
)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Дополнительная проверка: существует ли товар с таким артикулом
    product = crud.get_product_by_article(db, order.article)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Проверка существования пункта выдачи
    pickup_point = crud.get_pickup_point(db, order.pickup_point_id)
    if not pickup_point:
        raise HTTPException(status_code=404, detail="Pickup point not found")
    return crud.create_order(db, order)


@router.put(
    "/{order_id}",
    response_model=schemas.Order,
    dependencies=[Depends(dependencies.role_required("admin"))],
)
def update_order(
    order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)
):
    existing = crud.get_order(db, order_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud.update_order(db, order_id, order)


@router.delete(
    "/{order_id}", dependencies=[Depends(dependencies.role_required("admin"))]
)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    if crud.delete_order(db, order_id):
        return {"ok": True}
    raise HTTPException(status_code=404, detail="Order not found")
