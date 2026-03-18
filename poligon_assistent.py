import os
import asyncio
import datetime
import webbrowser
import time
import base64
from io import BytesIO
import speech_recognition as sr
import pygame
import edge_tts
import pyautogui
from PIL import ImageGrab
from groq import Groq

# =========================
# CONFIGURAÇÕES E MEMÓRIA
# =========================

# INSIRA SUA CHAVE DA GROQ AQUI DENTRO DAS ASPAS!
API_KEY_GROQ = "COLE_SUA_API_KEY_AQUI" 
client = Groq(api_key=API_KEY_GROQ)

historico = []

# Dicionário de atalhos rápidos
ATALHOS_DIRETOS = {
    "spotify": "start spotify:",
    "steam": "start steam://",
    "vrchat": "start steam://rungameid/438100", 
    "discord": "Update.exe --processStart Discord.exe", 
    "brave": "start brave",
    "osu": "start osu!"
}

# =========================
# SISTEMA DE VOZ
# =========================

def falar(texto):
    print(f"\nPoligon: {texto}")
    texto_limpo = texto.replace("*", "").replace("#", "")
    arquivo = "voz.mp3"

    asyncio.run(
        edge_tts.Communicate(
            texto_limpo,
            "pt-BR-AntonioNeural",
            rate="+20%"
        ).save(arquivo)
    )

    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()

    if os.path.exists(arquivo):
        try: os.remove(arquivo)
        except: pass

# =========================
# CAPTURA DE TELA
# =========================

def capturar_tela():
    try:
        img = ImageGrab.grab()
        largura, altura = img.size
        img_otimizada = img.resize((largura // 2, altura // 2))
        return img_otimizada
    except Exception as e:
        print(f"Erro ao capturar tela: {e}")
        return None

# =========================
# CÉREBRO DE IA
# =========================

def perguntar_ia(pergunta, imagem_tela):
    global historico
    try:
        print("[Poligon está analisando a tela e pensando...]")
        
        buffered = BytesIO()
        imagem_tela.save(buffered, format="JPEG")
        imagem_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        memoria = "\n".join(historico[-4:]) 
        prompt = f"""Você é Poligon, uma IA assistente de desktop avançada. Seu criador é o Mestre.
        Responda de forma natural, inteligente e DIRETA (curto). 
        Sempre que o usuário fizer uma pergunta, analise a imagem anexada da tela dele detalhadamente para ajudá-lo.
        
        Histórico recente:
        {memoria}
        
        Mestre pergunta: {pergunta}"""

        mensagens = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{imagem_base64}"
                        }
                    }
                ]
            }
        ]

        resposta = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct", 
            messages=mensagens
        )
        
        texto = resposta.choices[0].message.content
        
        historico.append(f"Mestre: {pergunta}")
        historico.append(f"Poligon: {texto}")
        
        return texto

    except Exception as e:
        print(f"Erro na IA: {e}")
        return "Tive uma falha na rede central de visão, mestre."

# =========================
# COMANDOS LOCAIS E APPS
# =========================

def executar_comando(comando):
    comando_lower = comando.lower()

    if "hora" in comando_lower:
        agora = datetime.datetime.now().strftime("%H e %M")
        falar(f"Agora são {agora}.")
        return True

    if "abrir youtube" in comando_lower:
        webbrowser.open("https://youtube.com")
        falar("Iniciando os servidores do YouTube.")
        return True

    if "abrir google" in comando_lower:
        webbrowser.open("https://google.com")
        falar("Google a postos.")
        return True
        
    if any(cmd in comando_lower for cmd in ["minimizar tudo", "área de trabalho", "esconder janelas"]):
        falar("Limpando sua área de trabalho, mestre.")
        pyautogui.hotkey('win', 'd')
        return True

    if any(cmd in comando_lower for cmd in ["modo jogatina", "modo jogo", "preparar para jogar"]):
        falar("Iniciando Modo Jogatina. Preparando o campo de batalha.")
        os.system(ATALHOS_DIRETOS["steam"])
        time.sleep(1) 
        os.system(ATALHOS_DIRETOS["discord"])
        pyautogui.press('volumemute')
        falar("Sistemas de comunicação e jogos online. Divirta-se, mestre.")
        return True

    if "abrir" in comando_lower or "iniciar" in comando_lower:
        app_alvo = comando_lower.replace("abrir", "").replace("iniciar", "").replace("o", "").replace("a", "").strip()
        
        if not app_alvo:
            return False

        falar(f"Iniciando {app_alvo}.")
        
        for chave, executavel in ATALHOS_DIRETOS.items():
            if chave in app_alvo:
                os.system(executavel)
                return True
        
        pyautogui.press('win')
        time.sleep(0.5) 
        pyautogui.write(app_alvo)
        time.sleep(0.6) 
        pyautogui.press('enter')
        return True

    return False

# =========================
# MOTOR PRINCIPAL
# =========================

def iniciar():
    recognizer = sr.Recognizer()
    falar("Sistemas online. Motor visual ativado. Diga Poligon para me chamar.")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                print("\n[Aguardando wake word 'Poligon'...]")
                audio = recognizer.listen(source)
                texto = recognizer.recognize_google(audio, language="pt-BR").lower()

                if any(gatilho in texto for gatilho in ["poligon", "polígono", "polly"]):
                    falar("Ao seu dispor.")

                    em_conversa = True
                    while em_conversa:
                        print("\n[Escutando seu comando...]")
                        try:
                            recognizer.pause_threshold = 1.0
                            audio_comando = recognizer.listen(source, timeout=7, phrase_time_limit=15)
                            comando = recognizer.recognize_google(audio_comando, language="pt-BR")

                            print(f"Você: {comando}")

                            if any(palavra in comando.lower() for palavra in ["desligar", "encerrar", "dormir"]):
                                falar("Sistemas em repouso. Até logo, mestre.")
                                os._exit(0)

                            if executar_comando(comando):
                                continue 

                            tela = capturar_tela()
                            if tela:
                                resposta = perguntar_ia(comando, tela)
                                falar(resposta)
                            else:
                                falar("Meus sensores visuais falharam ao capturar a tela.")

                        except sr.WaitTimeoutError:
                            print("[Poligon voltou a dormir.]")
                            em_conversa = False 
                        except sr.UnknownValueError:
                            em_conversa = False 

            except Exception as e:
                pass 

if __name__ == "__main__":
    iniciar()