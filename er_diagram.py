import os
from sqlalchemy import create_engine
from sqlalchemy_schemadisplay import create_schema_graph
from app.models import Base

# Берём строку подключения из переменной окружения, иначе используем значение по умолчанию
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db/shoe_shop")
engine = create_engine(DATABASE_URL)

graph = create_schema_graph(
    metadata=Base.metadata,
    show_datatypes=False,  # не показывать типы данных
    show_indexes=False,  # не показывать индексы
    rankdir="LR",  # направление слева направо
)
graph.write_pdf("er_diagram.pdf")
print("ER diagram generated: er_diagram.pdf")
