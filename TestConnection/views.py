from django.shortcuts import render
from django.conf import settings


def main(request):
    storescore = settings.STORE_SCORE
    print(storescore.get_balance())
    balance_before = storescore.get_balance()
    tnx = storescore.add_match(11, 0, 1, 2, "jeremy", "johnny", "johnny")
    if tnx is None or tnx.status == 0:
        print("transaction failed")
        return render(request, "main.html")
    else:
        print(f"transaction succesfull cost:\n{storescore.get_transaction_cost(balance_before, storescore.get_balance())} eth\n{storescore.get_usd_transaction_cost(balance_before, storescore.get_balance())}$")
    print(storescore.get_match_by_id(11))
    print(storescore.get_balance())
    return render(request, "main.html")
