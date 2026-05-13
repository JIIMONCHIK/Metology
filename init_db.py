import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.models import User, Product, PickupPoint, Order
from app.auth import get_password_hash


def init_db():
    # Создаём таблицы (если не существуют)
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    with Session(engine) as session:
        # Проверяем, есть ли уже данные (чтобы не импортировать повторно)
        if session.query(User).first() is not None:
            print("Database already contains data. Skipping import.")
            return

        print("Importing users...")
        users_df = pd.read_excel("data/user_import.xlsx")
        for _, row in users_df.iterrows():
            role_raw = row["Роль сотрудника"]
            if role_raw == "Администратор":
                role = "admin"
            elif role_raw == "Менеджер":
                role = "manager"
            elif role_raw == "Авторизированный клиент":
                role = "client"
            else:
                role = role_raw  # на случай других вариантов

            user = User(
                login=row["Логин"],
                password_hash=get_password_hash(row["Пароль"]),
                full_name=row["ФИО"],
                role=role,
            )
            session.add(user)
        session.commit()
        print(f"Imported {len(users_df)} users.")

        print("Importing pickup points...")
        pickup_df = pd.read_excel("data/Пункты выдачи_import.xlsx")
        # Предполагаем, что в файле один столбец с адресами (без заголовка)
        # В Excel может быть заголовок, поэтому берем первую колонку по индексу
        addresses = pickup_df.iloc[:, 0].tolist()
        for idx, addr in enumerate(addresses, start=1):
            pp = PickupPoint(id=idx, address=addr)
            session.add(pp)
        session.commit()
        print(f"Imported {len(addresses)} pickup points.")

        print("Importing products...")
        products_df = pd.read_excel("data/Tovar.xlsx")
        for _, row in products_df.iterrows():
            # Определяем путь к фото
            img_file = row["Фото"] if pd.notna(row["Фото"]) else ""
            if img_file and os.path.exists(f"app/static/images/{img_file}"):
                img_path = f"/static/images/{img_file}"
            else:
                img_path = "/static/images/picture.png"

            product = Product(
                article=row["Артикул"],
                name=row["Наименование товара"],
                unit=row["Единица измерения"],
                price=row["Цена"],
                supplier=row["Поставщик"],
                manufacturer=row["Производитель"],
                category=row["Категория товара"],
                discount_percent=row["Действующая скидка"],
                quantity_in_stock=row["Кол-во на складе"],
                description=(
                    row["Описание товара"] if pd.notna(row["Описание товара"]) else ""
                ),
                image_path=img_path,
            )
            session.add(product)
        session.commit()
        print(f"Imported {len(products_df)} products.")

        print("Importing orders...")
        orders_df = pd.read_excel("data/Заказ_import.xlsx")
        orders_created = 0

        for idx, row in orders_df.iterrows():
            # Разбираем поле "Артикул заказа": оно содержит пары "артикул, количество"
            article_field = row["Артикул заказа"]
            if pd.isna(article_field):
                print(f"Warning: empty article field in row {idx}, skipping")
                continue
            parts = [p.strip() for p in str(article_field).split(",")]
            # Если количество частей нечётное, данные повреждены
            if len(parts) % 2 != 0:
                print(
                    f"Warning: malformed article field '{article_field}' in row {idx}, skipping"
                )
                continue
            items = [(parts[i], int(parts[i + 1])) for i in range(0, len(parts), 2)]

            pickup_index = row["Адрес пункта выдачи"]
            try:
                pickup_id = int(pickup_index)
            except (ValueError, TypeError):
                print(
                    f"Warning: invalid pickup point index '{pickup_index}' in row {idx}, skipping"
                )
                continue

            # Проверка существования пункта выдачи
            if (
                not session.query(PickupPoint)
                .filter(PickupPoint.id == pickup_id)
                .first()
            ):
                print(f"Warning: pickup point {pickup_id} not found, skipping order")
                continue

            # Обработка дат с возможными ошибками
            order_date = pd.to_datetime(row["Дата заказа"], errors="coerce")
            if pd.isna(order_date):
                print(
                    f"Warning: invalid order date '{row['Дата заказа']}' in row {idx}, skipping order"
                )
                continue

            issue_date = None
            if pd.notna(row["Дата доставки"]):
                issue_date = pd.to_datetime(row["Дата доставки"], errors="coerce")
                if pd.isna(issue_date):
                    print(
                        f"Warning: invalid issue date '{row['Дата доставки']}' in row {idx}, will set to None"
                    )

            # Создаём отдельный заказ для каждого артикула
            for article, qty in items:
                order = Order(
                    article=article,
                    status=row["Статус заказа"],
                    pickup_point_id=pickup_id,
                    order_date=order_date.date(),
                    issue_date=(
                        issue_date.date()
                        if issue_date and not pd.isna(issue_date)
                        else None
                    ),
                    user_id=None,
                )
                session.add(order)
                orders_created += 1

        session.commit()
        print(
            f"Imported {orders_created} orders (from {len(orders_df)} original rows)."
        )

        print("Database initialization completed successfully.")


if __name__ == "__main__":
    init_db()
