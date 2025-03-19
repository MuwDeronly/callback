import discord
from flask import Flask, request, redirect
import os
import json
from discord.ext import commands

app = Flask(__name__)

# ID du bot et du serveur Discord
BOT_TOKEN = "MTM0ODU5Njk4ODE3Nzk0NDYxNw.GzoDGy.D2Yf3z3WtSycFFLW52aFOP1K1wcGDzH040RLkY"
GUILD_ID = "1345009390302003272"

intents = discord.Intents.default()
intents.members = True  # Assurez-vous d'avoir accès aux membres du serveur

client = discord.Client(intents=intents)

# Initialisation du bot
bot = commands.Bot(command_prefix="!", intents=intents)

@app.route("/callback")
def callback():
    # Récupère le code de la requête
    code = request.args.get('code')

    if not code:
        return "Code missing, can't verify user."

    # Utiliser le code pour obtenir un access_token (ici on suppose l'utilisation d'un flow OAuth2)
    access_token = exchange_code_for_token(code)
    
    if not access_token:
        return "Failed to get access token."

    # Vérifie que l'utilisateur est légitime
    user = get_user_from_access_token(access_token)

    if user:
        # Une fois l'utilisateur validé, ajoute-le au serveur Discord
        add_user_to_guild(user)

    return "Verification successful. You may now join the server."

def exchange_code_for_token(code):
    # Échange le code contre un access token OAuth2
    url = "https://discord.com/api/v10/oauth2/token"
    data = {
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": "https://callback-4qhc.onrender.com/callback"
    }

    # Remplacer la méthode de requête par l'API de discord pour récupérer le token
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    
    return None

def get_user_from_access_token(access_token):
    # Utilise l'access token pour obtenir des informations sur l'utilisateur
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Renvoie les informations de l'utilisateur
    
    return None

def add_user_to_guild(user):
    # Ajoute l'utilisateur au serveur Discord via `guild.join`
    guild = discord.utils.get(client.guilds, id=int(GUILD_ID))
    
    if guild:
        # Récupère le membre via son ID (ici, tu pourrais vouloir inviter le membre)
        invite_link = f"https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&scope=bot&permissions=BOT_PERMISSIONS&guild_id={GUILD_ID}"
        print(f"Send this invite link to the user to join the server: {invite_link}")

# Démarrer l'app Flask
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
    app.run(host="0.0.0.0", port=8080)
