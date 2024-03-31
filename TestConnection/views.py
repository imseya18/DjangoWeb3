from django.shortcuts import render
from django.conf import settings
from .ConnectionToBC import *


def main(request):
    storescore = settings.STORE_SCORE
    print(storescore.get_balance())
    balance_before = storescore.get_balance()
    tnx = storescore.add_match(6, 0, 1, 2, "lolita", "johnny", "johnny")
    if tnx.status == 0:
        print("transaction failed")
    else:
        print(f"transaction succesfull cost:\n{storescore.get_transaction_cost(balance_before, storescore.get_balance())} eth\n{storescore.get_usd_transaction_cost(balance_before, storescore.get_balance())}$")
    print(storescore.get_match_by_id(6))
    print(storescore.get_balance())
    return render(request, "main.html")
