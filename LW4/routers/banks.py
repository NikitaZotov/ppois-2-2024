from fastapi import APIRouter, HTTPException, Form
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from internal.services_provider import ServiceProvider


router = APIRouter(
    prefix="/banks",
    tags=["banks"],
    responses={404: {"description": "Not found"}},
)

templates = Jinja2Templates(directory="templates")
service_provider = ServiceProvider()
finances_service = service_provider.FinancesService


# Bank creation
@router.get('/create')
def post_bank(request: Request):
    return templates.TemplateResponse('create_bank.html', {"request": request})


@router.post('/create')
def post_bank(request: Request, name: str = Form(...)):
    try:
        if name == 'create':
            raise ValueError('Problems, huh?')

        finances_service.create_bank(name)
        finances_service.commit_changes()
        return RedirectResponse("/banks", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"create_bank threw {str(e)}")
        context = {"request": request, "redirect": "/banks", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.get("/{name}")
async def view_bank(request: Request, name: str):
    try:
        bank = finances_service.get_bank(name)
        bank.cards = finances_service.get_cards(name)
    except ValueError as e:
        context = {"request": request, "redirect": "/banks", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)

    context = {"request": request, "bank": bank}
    return templates.TemplateResponse("bank.html", context)


@router.get('/')
async def view_banks(request: Request):
    try:
        banks = finances_service.get_banks()
        return templates.TemplateResponse("banks.html", {"request": request, "banks": banks})
    except Exception as e:
        print(f"get_banks threw {str(e)}")
        context = {"request": request, "redirect": "/banks", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.delete('/{name}')
async def delete_bank(request: Request, name: str):
    try:
        finances_service.remove_bank(name)
        finances_service.commit_changes()
        return RedirectResponse("/banks", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        context = {"request": request, "redirect": "/banks", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


# REGION CARDS
@router.get('/{bank_name}/cards/create')
def post_card(request: Request, bank_name: str):
    return templates.TemplateResponse('create_card.html', {"request": request, "bank_name": bank_name})


@router.post('/{bank_name}/cards/')
def post_card(request: Request, bank_name: str, card_number: int = Form(...), card_pin: int = Form(...)):
    try:
        finances_service.create_card(bank_name, card_number, None, card_pin)
        finances_service.commit_changes()
        return RedirectResponse(f"/banks/{bank_name}", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"create_card threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/create", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.get("/{bank_name}/cards/{card_number}")
def view_card(request: Request, bank_name: str, card_number: int):
    try:
        card = finances_service.get_card(bank_name, card_number)
    except Exception as e:
        print(f"get_card threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)

    context = {"request": request,
               "bank_name": bank_name,
               "card": card}
    return templates.TemplateResponse("card.html", context)


@router.delete('/{bank_name}/cards/{card_number}')
def post_card(request: Request, bank_name: str, card_number: int):
    try:
        finances_service.remove_card(bank_name, card_number)
        finances_service.commit_changes()
        return RedirectResponse(f"/banks/{bank_name}", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/{card_number}", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.get('/{bank_name}/cards/{card_number}/change_pin')
def get_change_pin(request: Request, bank_name: str, card_number: int):
    return templates.TemplateResponse('card_operations/change_pin.html', {"request": request,
                                                                          "bank_name": bank_name,
                                                                          "card_number": card_number})


@router.post('/{bank_name}/cards/{card_number}/change_pin')
def post_change_pin(request: Request, bank_name: str, card_number: int, card_pin: int = Form(...)):
    try:
        finances_service.set_pin(bank_name, card_number, card_pin)
        finances_service.commit_changes()
        return RedirectResponse(f"/banks/{bank_name}/cards/{card_number}", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"set_pin threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/{card_number}/change_pin", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.get('/{bank_name}/cards/{card_number}/change_limit')
def get_change_limit(request: Request, bank_name: str, card_number: int):
    return templates.TemplateResponse('card_operations/change_limit.html', {"request": request,
                                                                            "bank_name": bank_name,
                                                                            "card_number": card_number})


@router.post('/{bank_name}/cards/{card_number}/change_limit')
def post_change_limit(request: Request, bank_name: str, card_number: int,
                      card_limit: int = Form(...),
                      card_pin: int = Form(...)):
    try:
        finances_service.set_limit(bank_name, card_number, card_limit, card_pin)
        finances_service.commit_changes()
        return RedirectResponse(f"/banks/{bank_name}/cards/{card_number}", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"set_limit threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/{card_number}/change_limit", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.get('/{bank_name}/cards/{card_number}/withdraw')
def get_withdraw(request: Request, bank_name: str, card_number: int):
    return templates.TemplateResponse('card_operations/withdraw.html', {"request": request,
                                                                        "bank_name": bank_name,
                                                                        "card_number": card_number})


@router.post('/{bank_name}/cards/{card_number}/withdraw')
def post_withdraw(request: Request, bank_name: str, card_number: int,
                  amount: int = Form(...),
                  card_pin: int = Form(...)):
    try:
        finances_service.withdraw(bank_name, card_number, amount, card_pin)
        finances_service.commit_changes()
        return RedirectResponse(f"/banks/{bank_name}/cards/{card_number}", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"withdraw threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/{card_number}/withdraw", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.get('/{bank_name}/cards/{card_number}/deposit')
def get_deposit(request: Request, bank_name: str, card_number: int):
    return templates.TemplateResponse('card_operations/deposit.html', {"request": request,
                                                                       "bank_name": bank_name,
                                                                       "card_number": card_number})


@router.post('/{bank_name}/cards/{card_number}/deposit')
def post_deposit(request: Request, bank_name: str, card_number: int,
                 amount: int = Form(...)):
    try:
        finances_service.deposit(bank_name, card_number, amount)
        finances_service.commit_changes()
        return RedirectResponse(f"/banks/{bank_name}/cards/{card_number}", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"deposit threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/{card_number}/deposit", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.post('/{bank_name}/cards/{card_number}/balance/')
def post_balance(request: Request, bank_name: str, card_number: int, card_pin: int | None = Form(...)):
    try:
        balance = finances_service.get_balance(bank_name, card_number, card_pin)
        return templates.TemplateResponse('card_operations/balance.html', {"request": request,
                                                                           "bank_name": bank_name,
                                                                           "card_number": card_number,
                                                                           "balance": balance})
    except Exception as e:
        print(f"get_balance threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/{card_number}/balance/pin", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.get('/{bank_name}/cards/{card_number}/balance/pin')
def get_balance(request: Request, bank_name: str, card_number: int):
    return templates.TemplateResponse('card_operations/input_pin.html', {"request": request,
                                                                         "bank_name": bank_name,
                                                                         "card_number": card_number,
                                                                         "operation": "check balance",
                                                                         "redirect": f"/banks/{bank_name}/cards/{card_number}/balance"})


@router.get('/{bank_name}/cards/{card_number}/toggle_block')
def get_toggle_block(request: Request, bank_name: str, card_number: int):
    try:
        finances_service.toggle_block(bank_name, card_number)
        finances_service.commit_changes()
        return RedirectResponse(f"/banks/{bank_name}/cards/{card_number}", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"toggle_block threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/{card_number}", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)


@router.get('/{bank_name}/cards/{card_number}/transfer')
def get_transfer(request: Request, bank_name: str, card_number: int):
    return templates.TemplateResponse('card_operations/transfer.html', {"request": request,
                                                                       "bank_name": bank_name,
                                                                       "card_number": card_number})


@router.post('/{bank_name}/cards/{card_number}/transfer')
def post_transfer(request: Request, bank_name: str, card_number: int,
                  card_pin: int = Form(...),
                  receiver_card_number: int = Form(...),
                  amount: int = Form(...)):
    try:
        finances_service.transfer(bank_name, card_number, receiver_card_number, card_pin, amount)
        finances_service.commit_changes()
        return RedirectResponse(f"/banks/{bank_name}/cards/{card_number}", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        print(f"transfer threw {str(e)}")
        context = {"request": request, "redirect": f"/banks/{bank_name}/cards/{card_number}/transfer", "details": str(e)}
        return templates.TemplateResponse("common/something_went_wrong.html", context)
