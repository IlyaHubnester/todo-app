from fastapi import FastAPI

from todo import views as todo_views
from operations import views as operations_views

app = FastAPI(debug=True)

app.include_router(todo_views.router)
app.include_router(operations_views.router)