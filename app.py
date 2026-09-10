import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import streamlit as st
import os
import base64
from pprint import pprint


load_dotenv()
sportify_client_id = os.environ["SPORTIFY_CLIENT_ID"]
sportify_client_secret = os.environ["SPORTIFY_CLIENT_SECRET"]

def token_acesso(client_id: str, client_secret: str) -> str:
    b_client_id = client_id.encode("utf-8")
    b_client_secret = client_secret.encode("utf-8")

    resposta = requests.post(
            "https://accounts.spotify.com/api/token",
                headers={
                    "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode("utf-8")
                },
                data={
                    "grant_type": "client_credentials"
                }
            )

    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"Ocorreu um erro: {e}")
        return None
    else:
        return resposta.json()["access_token"]

def buscar_artistas(token: str, nome_artista: str):
    resposta = requests.get(
        "https://api.spotify.com/v1/search",
        headers= {
            "Authorization": "Bearer " + token
        },
        params={
            "q": nome_artista,
            "limit": 1,
            "type": "artist"
        }
    )

    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"ocorreu um erro: {e}")
        resultado = None
    else:
        resultado = resposta.json()
    return resultado

token = token_acesso(
    sportify_client_id,
    sportify_client_secret
)

pprint(buscar_artistas(token,"Joji"))
