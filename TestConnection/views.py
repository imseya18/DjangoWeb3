from django.shortcuts import render
from django.conf import settings
from .ConnectionToBC import *


def main(request):
    connnecttobc()
    return render(request, "main.html")
