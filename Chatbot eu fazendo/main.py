from fastapi import FastAPI, Request
from evolution import send_whatsapp_message
from Agente import agente, rag  # tudo vem de um lugar só

app = FastAPI()

@app.on_event("startup")
async def load_rag_data():
    print("🔄 Carregando base de conhecimento...")
    await rag.add_content_async(path="process_pdf")  # ✅ versão assíncrona
    print("✅ Base carregada!")

@app.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    chat_id = data.get('data', {}).get('key', {}).get('remoteJid')
    message = data.get('data', {}).get('message', {}).get('conversation')

    if chat_id and message and '@g.us' not in chat_id:
        response_agente = agente.run(message, session_id=chat_id)
        send_whatsapp_message(number=chat_id, text=str(response_agente.content))

    return {'status': 'ok'}
