
import os
import requests
from fastapi import FastAPI, Request, HTTPException, Response
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

# Obtém as variáveis de ambiente
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
FORWARD_URL = os.getenv("FORWARD_URL")

@app.get("/webhook")
async def webhook_verification(request: Request):
    """
    Verifica a assinatura do webhook da Meta.
    """
    # Extrai os parâmetros da query
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    # Verifica se o modo e o token estão presentes e corretos
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print(f"Webhook verified successfully!")
        return Response(content=challenge, media_type="text/plain")
    else:
        print("Webhook verification failed.")
        raise HTTPException(status_code=403, detail="Verification token mismatch.")

@app.post("/webhook")
async def webhook_handler(request: Request):
    """
    Recebe os eventos do WhatsApp, imprime e encaminha para a URL local.
    """
    payload = await request.json()
    print("Payload recebido da Meta:")
    print(payload)

    print(f"URL completa recebida pela Meta: {request.url}")

    query_params = request.url

    print("Parâmetros da query:")
    print(query_params)

    if not FORWARD_URL:
        print("ERRO: A variável de ambiente FORWARD_URL não está definida.")
        return {"status": "error", "message": "Forward URL not configured"}

    try:
        # Encaminha o payload para a URL local
        headers = {'Content-Type': 'application/json'}
        res = requests.post(FORWARD_URL, json=payload, headers=headers, params=query_params)
        res.raise_for_status()  # Lança uma exceção para respostas de erro (4xx ou 5xx)
        
        print(f"Payload encaminhado para {FORWARD_URL} com sucesso.")
        print(f"Resposta do servidor local: {res.status_code}")
        return {"status": "success", "message": "Payload forwarded"}

    except requests.exceptions.RequestException as e:
        print(f"ERRO ao encaminhar o payload para {FORWARD_URL}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to forward payload: {e}")

@app.get("/")
def read_root():
    return {"message": "Servidor FastAPI para webhook do WhatsApp está rodando."}

