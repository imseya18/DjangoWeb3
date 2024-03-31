"""
Django settings for Testweb3 project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
import json
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

INFURA_PK = config('INFURA_PK')
INFURA_API_KEY = config('INFURA_API_KEY')
META_PK = config('META_PK')
ETH_ADDRESS = config('MY_ADDRESS')
CONTRACT_ADDRESS = config('CONTRACT_ADDRESS')
INFURA_URL = f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"
ABI = json.loads('[{"inputs": [{"internalType": "address","name": "owner","type": "address"}],"name": "OwnableInvalidOwner","type": "error"},{"inputs": [{"internalType": "address","name": "account","type": "address"}],"name": "OwnableUnauthorizedAccount","type": "error"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "previousOwner","type": "address"},{"indexed": true,"internalType": "address","name": "newOwner","type": "address"}],"name": "OwnershipTransferred","type": "event"},{"inputs": [{"internalType": "uint256","name": "_r_matchId","type": "uint256"},{"internalType": "uint256","name": "_tournamentId","type": "uint256"},{"internalType": "uint8","name": "_player1Score","type": "uint8"},{"internalType": "uint8","name": "_player2Score","type": "uint8"},{"internalType": "string","name": "_player1Id","type": "string"},{"internalType": "string","name": "_player2Id","type": "string"},{"internalType": "string","name": "_winner","type": "string"}],"name": "addMatch","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256[]","name": "_r_matchId","type": "uint256[]"},{"internalType": "uint256","name": "_tournamentId","type": "uint256"},{"internalType": "uint8[]","name": "_player1Score","type": "uint8[]"},{"internalType": "uint8[]","name": "_player2Score","type": "uint8[]"},{"internalType": "string[]","name": "_player1Id","type": "string[]"},{"internalType": "string[]","name": "_player2Id","type": "string[]"},{"internalType": "string[]","name": "_winner","type": "string[]"}],"name": "addTournament","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "renounceOwnership","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "newOwner","type": "address"}],"name": "transferOwnership","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256","name": "_r_matchId","type": "uint256"}],"name": "getMatchById","outputs": [{"components": [{"internalType": "uint256","name": "matchId","type": "uint256"},{"internalType": "uint8","name": "player1Score","type": "uint8"},{"internalType": "uint8","name": "player2Score","type": "uint8"},{"internalType": "string","name": "player1Id","type": "string"},{"internalType": "string","name": "player2Id","type": "string"},{"internalType": "string","name": "winner","type": "string"}],"internalType": "struct storeScore.Match","name": "","type": "tuple"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "string","name": "_playerName","type": "string"}],"name": "getPlayerMatchs","outputs": [{"components": [{"internalType": "uint256","name": "matchId","type": "uint256"},{"internalType": "uint8","name": "player1Score","type": "uint8"},{"internalType": "uint8","name": "player2Score","type": "uint8"},{"internalType": "string","name": "player1Id","type": "string"},{"internalType": "string","name": "player2Id","type": "string"},{"internalType": "string","name": "winner","type": "string"}],"internalType": "struct storeScore.Match[]","name": "","type": "tuple[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "_tournamentId","type": "uint256"}],"name": "getTournament","outputs": [{"components": [{"internalType": "uint256","name": "matchId","type": "uint256"},{"internalType": "uint8","name": "player1Score","type": "uint8"},{"internalType": "uint8","name": "player2Score","type": "uint8"},{"internalType": "string","name": "player1Id","type": "string"},{"internalType": "string","name": "player2Id","type": "string"},{"internalType": "string","name": "winner","type": "string"}],"internalType": "struct storeScore.Match[]","name": "","type": "tuple[]"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "owner","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"}]')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b&)ba%5_kohu%k^v^z&#l4$(ae9^__wnh3iinsu#h_#p)qra3y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TestConnection',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Testweb3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Testweb3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
