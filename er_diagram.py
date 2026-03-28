from sqlalchemy import create_engine
from sqlalchemy_schemadisplay import create_schema_graph
from app.models import Base

engine = create_engine('postgresql://user:pass@localhost/db')
graph = create_schema_graph(metadata=Base.metadata, show_datatypes=False, show_indexes=False)
graph.write_pdf('er_diagram.pdf')