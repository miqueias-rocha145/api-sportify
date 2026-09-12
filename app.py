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

def buscar_artistas(nome_artista: str, headers: dict[str, str]) -> str:
    resposta = requests.get(
        "https://api.spotify.com/v1/search",
        headers=headers,
        params={
            "q": nome_artista,
            "limit": 1,
            "type": "artist"
        }
    )

    try:
        primeiro_artista = resposta.json()['artists']['items'][0]
    except IndexError as e:
        print(f"ocorreu um erro: {e}")
        primeiro_artista = None
    return primeiro_artista

def buscar_albums_artista(id_artista: str, headers: dict[str, str]):
    url = f"https://api.spotify.com/v1/artists/{id_artista}/albums"
    resposta = requests.get(
        url,
        headers=headers
    )

    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f"ocorreu um erro: {e}")
        print(f"Detalhes: {resposta.text}")
        resultado = None
    else:
        resultado = resposta.json()
    return resultado

token = token_acesso(
    sportify_client_id,
    sportify_client_secret
)

autenticacao={
    "Authorization": "Bearer " + token 
}

artista = buscar_artistas("Joji",headers=autenticacao)

id_artista = artista['id']
nome_artista = artista['name']

pprint(buscar_albums_artista(
    id_artista=id_artista,
    headers=autenticacao
))