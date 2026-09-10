from dotenv import load_dotenv
import streamlit as st
import os


load_dotenv()
sportify_client_id = os.environ["SPORTIFY_CLIENT_ID"]
sportify_client_secret = os.environ["SPORTIFY_CLIENT_SECRET"]
    