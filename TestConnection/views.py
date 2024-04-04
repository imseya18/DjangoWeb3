from django.shortcuts import render
from django.conf import settings
from .models import Match, Tournament
from .StoreInDB import delete_match_from_db
#def main(request):
#    storescore = settings.STORE_SCORE
#    print(storescore.get_balance())
#    balance_before = storescore.get_balance()
#    tnx = storescore.add_match(11, 0, 1, 2, "jeremy", "johnny", "johnny")
#    if tnx is None or tnx.status == 0:
#        print("transaction failed")
#        return render(request, "main.html")
#    else:
#        print(f"transaction succesfull cost:\n{storescore.get_transaction_cost(balance_before, storescore.get_balance())} eth\n{storescore.get_usd_transaction_cost(balance_before, storescore.get_balance())}$")
#    print(storescore.get_match_by_id(11))
#    print(storescore.get_balance())
#    return render(request, "main.html")


def match_add(request):
    storescore = settings.STORE_SCORE
    if Match.objects.exists():
        print(f" il y a {Match.objects.count()} match dans la db")
        for match in Match.objects.all():
            tnx = storescore.add_match(match.match_id, 0, match.player1_score, match.player2_score, match.player1_id,
                                 match.player2_id, match.winner_id)
            if tnx is not None:
                print("la TX est reussi je delete")
                delete_match_from_db(match.match_id)
    storescore.add_match(17, 0, 1, 2, "jeremy", "johnny", "johnny")
    return render(request, "main.html")


def match_get(request):
    storescore = settings.STORE_SCORE
    match = storescore.get_match_by_id(17)
    print(match)
    return render(request, "main.html")
