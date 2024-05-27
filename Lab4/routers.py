# -*- coding: utf-8 -*-
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from Model.barbershop import Barbershop
from Model import barbershop
from Model.ClientDataValidator import ClientDataValidator

from typing import Optional, List

templates = Jinja2Templates(directory="templates")

router = APIRouter()

barbershop = Barbershop(500)

validator = ClientDataValidator()


def load_barbershop_state():
    barbershop.load_state()


names = ["add_registration", "delete_clients", "performing", "execution", "purchase"]


@router.get("/", response_class=HTMLResponse)
async def show_main(request: Request, message: str = None):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "budget": barbershop.budget,
        "barbers_count": barbershop.barbers_count,
        "clients": barbershop.clients,
        "message": message
    })


@router.get("/execution/", response_class=HTMLResponse)
async def execution(request: Request):
    message = barbershop.perform_all_registered_services()
    barbershop.save_state()
    return templates.TemplateResponse("execution.html", {
        "request": request,
        "message": message
    })


@router.get("/purchase/", response_class=HTMLResponse)
async def execution(request: Request):
    try:
        message = barbershop.purchase()
        barbershop.save_state()
        return await show_main(request=request, message=message)
    except Exception as e:
        context = {"request": request, "error_message": str(e)}
        return templates.TemplateResponse("error.html", context)


@router.get("/add_registration/", response_class=HTMLResponse)
async def add_registration(request: Request):
    message = barbershop.barbers_not_empty_str()
    if message is not None:
        return await show_main(request=request, message=message)
    return templates.TemplateResponse("add_registration.html", {"request": request})


@router.post("/add_registration/")
def submit_registration(request: Request, name: Optional[str] = Form(None), day: str = Form(...),
                        time: int = Form(...),
                        service_type: str = Form(...), hair_length: str = Form(...), hair_type: str = Form(...)):
    try:
        validation = validator.validate_name(name)
        if validation is not True:
            return templates.TemplateResponse("add_registration.html",
                                              {
                                                  "request": request,
                                                  "error_message": validation,
                                                  "name": name,
                                                  "day": day,
                                                  "time": time,
                                                  "service_type": service_type,
                                                  "hair_length": hair_length,
                                                  "hair_type": hair_type
                                              },
                                              status_code=422)
        message = barbershop.add_registration(name, day, time, service_type, hair_length, hair_type)
        context = {"request": request, "message": message}
        barbershop.save_state()
        return templates.TemplateResponse("add_registration.html", context)
    except Exception as e:
        context = {"request": request, "error_message": str(e)}
        return templates.TemplateResponse("add_registration.html", context)
    except ValueError as e:
        context = {"request": request, "error_message": str(e)}
        return templates.TemplateResponse("error.html", context)


@router.delete("/delete_clients/")
async def delete_selected(request: Request, selected_rows: List[int] = Form(...)):
    message = barbershop.delete_registration_list(selected_rows)
    barbershop.save_state()
    return await show_main(request=request, message=message)


@router.get("/{name:path}")
async def read_item(name: str, request: Request):
    if name not in names:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": "Страница не найдена"},
                                          status_code=404)
