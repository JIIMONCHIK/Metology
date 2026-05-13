from sqlalchemy.orm import Session
from app import models, schemas


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def get_products(
    db: Session,
    skip=0,
    limit=100,
    search=None,
    sort_by_quantity=None,
    filter_supplier=None,
):
    query = db.query(models.Product)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.Product.name.ilike(search_term))
            | (models.Product.category.ilike(search_term))
            | (models.Product.description.ilike(search_term))
            | (models.Product.manufacturer.ilike(search_term))
            | (models.Product.supplier.ilike(search_term))
            | (models.Product.article.ilike(search_term))
        )
    if filter_supplier:
        query = query.filter(models.Product.supplier == filter_supplier)
    if sort_by_quantity == "asc":
        query = query.order_by(models.Product.quantity_in_stock.asc())
    elif sort_by_quantity == "desc":
        query = query.order_by(models.Product.quantity_in_stock.desc())
    return query.offset(skip).limit(limit).all()


def get_suppliers(db: Session):
    return [row[0] for row in db.query(models.Product.supplier).distinct().all()]


def get_categories(db: Session):
    return [row[0] for row in db.query(models.Product.category).distinct().all()]


def get_manufacturers(db: Session):
    return [row[0] for row in db.query(models.Product.manufacturer).distinct().all()]


def get_units(db: Session):
    return [row[0] for row in db.query(models.Product.unit).distinct().all()]


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    for var, value in vars(product).items():
        setattr(db_product, var, value) if value else None
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return False
    # проверка на наличие в заказах
    if db.query(models.Order).filter(models.Order.article == product.article).first():
        return False  # нельзя удалить
    db.delete(product)
    db.commit()
    return True


# аналогично для заказов
def get_orders(db: Session, skip=0, limit=100):
    return db.query(models.Order).offset(skip).limit(limit).all()


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    for var, value in vars(order).items():
        setattr(db_order, var, value) if value else None
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True


def get_pickup_points(db: Session):
    return db.query(models.PickupPoint).all()


def get_pickup_point(db: Session, point_id: int):
    return (
        db.query(models.PickupPoint).filter(models.PickupPoint.id == point_id).first()
    )


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()
