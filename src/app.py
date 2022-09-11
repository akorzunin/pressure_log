import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from jinja2 import Environment, FileSystemLoader

from src.dashapp import create_dash_app

env = Environment(loader=FileSystemLoader("./src/templates"))
template = env.get_template("dashboard.html")

app = FastAPI()


@app.get("/")
def read_main():
    ...


@app.get("/status")
def get_status():
    return {"status": "ok"}


dash_app = create_dash_app(
    # dashboard template content
    html_layout=template.render(
        content="_",
        # **defaults,
    ),
    prefix="/dash/",
)

app.mount("/dash", WSGIMiddleware(dash_app.server))
