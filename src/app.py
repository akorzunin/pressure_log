import pprint
from fastapi import FastAPI, status, Request
from fastapi.responses import (
    RedirectResponse,
    HTMLResponse,
    FileResponse,
)
from fastapi.templating import Jinja2Templates
from fastapi.middleware.wsgi import WSGIMiddleware
from jinja2 import Environment, FileSystemLoader

from src.dashapp import create_dash_app
from src import crud
from src.db_conn import users
from src.localization.ru import ru_language
from src.localization.en import en_language

env = Environment(loader=FileSystemLoader("./src/templates"))
dash_template = env.get_template("dashboard.html")
templates = Jinja2Templates(
    directory="src/templates",
)

app = FastAPI()


@app.get("/")
def read_main():
    return RedirectResponse("/dash")


@app.get(
    "/data",
    response_class=HTMLResponse,
    status_code=status.HTTP_300_MULTIPLE_CHOICES,
)
def data_page(request: Request):
    current_user = 1
    raw_data = crud.get_user(users, current_user)
    format_data = pprint.pformat(raw_data)
    return templates.TemplateResponse(
        "data.html",
        {
            "request": request,
            "content": format_data.replace("\n", "<br>").replace(" ", " "),
        },
    )


@app.get("/pressure_log_json")
def export_json():
    current_user = 1
    return crud.get_user(users, current_user)


@app.get(
    "/export_txt/{lang}",
    response_class=FileResponse,
)
def export_txt_ru(lang: str):
    if lang == "pressure_log_en":
        local_lang = en_language
    elif lang == "pressure_log_ru":
        local_lang = ru_language
    else:
        raise NotImplementedError(f"No localization for {lang}")
    current_user = 1
    json_data = crud.get_user(users, current_user)
    data = json_data["items"]
    with open("temp.txt", "w", encoding="utf-8") as file:
        for item in data:
            file.write(f"{local_lang['day']}: {item['day_id']}\n")
            morning = item.get("morning")
            evening = item.get("evening")
            if shard := morning:
                file.write(
                    f"{local_lang['morning']}: {shard['up']}/{shard['down']} p: {shard['pulse']}\n"
                )
            if shard := evening:
                file.write(
                    f"{local_lang['evening']}: {shard['up']}/{shard['down']} p: {shard['pulse']}\n"
                )
    return FileResponse(
        "temp.txt",
    )


@app.get("/status")
def get_status():
    return {"status": "ok"}


dash_app = create_dash_app(
    # dashboard template content
    html_layout=dash_template.render(
        content="_",
        # **defaults,
    ),
    prefix="/dash/",
)

app.mount("/dash", WSGIMiddleware(dash_app.server))
