import os
import asyncio
import datetime
import webbrowser
import time
import base64
import threading
from io import BytesIO
from queue import Queue, Empty
from pathlib import Path
import speech_recognition as sr
import pygame
import edge_tts
import pyautogui
from PIL import ImageGrab
from groq import Groq

API_KEY_GROQ = os.getenv("GROQ_API_KEY", "")
MODO_PRIVADO_SEM_API = os.getenv("POLIGON_SEM_API", "1").strip().lower() in {"1", "true", "yes", "on"}
IDLE_INTERVALO = int(os.getenv("POLIGON_IDLE_INTERVALO", "300"))

client = Groq(api_key=API_KEY_GROQ) if API_KEY_GROQ and not MODO_PRIVADO_SEM_API else None
historico = []

ATALHOS_DIRETOS = {
    "spotify": "start spotify:",
    "steam": "start steam://",
    "vrchat": "start steam://rungameid/438100",
    "discord": "Update.exe --processStart Discord.exe",
    "brave": "start brave",
    "osu": "start osu!",
}


class AgenteIdle:
    def __init__(self, intervalo=300):
        self.intervalo = max(60, intervalo)
        self.fila_tarefas = Queue()
        self.ativo = False
        self.thread = None
        self.log_path = Path("poligon_agent.log")

    def registrar(self, msg):
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(f"[{stamp}] {msg}\n")

    def adicionar_tarefa(self, tarefa):
        self.fila_tarefas.put(tarefa)
        self.registrar(f"Tarefa adicionada: {tarefa}")

    def status(self):
        return f"Agente {'ativo' if self.ativo else 'inativo'} | fila: {self.fila_tarefas.qsize()} | intervalo: {self.intervalo}s"

    def _rodar(self):
        self.registrar("Agente idle iniciado")
        while self.ativo:
            try:
                tarefa = self.fila_tarefas.get_nowait()
                self.executar_tarefa(tarefa)
            except Empty:
                self.executar_rotina_idle()
            time.sleep(self.intervalo)
        self.registrar("Agente idle parado")

    def iniciar(self):
        if self.ativo:
            return
        self.ativo = True
        self.thread = threading.Thread(target=self._rodar, daemon=True)
        self.thread.start()

    def parar(self):
        self.ativo = False

    def executar_tarefa(self, tarefa):
        if tarefa == "abrir_navegador":
            webbrowser.open("https://google.com")
            self.registrar("Executado: abrir_navegador")
        elif tarefa == "relatorio_sistema":
            self.gerar_relatorio_sistema()
            self.registrar("Executado: relatorio_sistema")
        else:
            self.registrar(f"Tarefa desconhecida ignorada: {tarefa}")

    def executar_rotina_idle(self):
        self.gerar_relatorio_sistema()
        self.registrar("Rotina idle: relatório de sistema atualizado")

    def gerar_relatorio_sistema(self):
        agora = datetime.datetime.now().isoformat(timespec="seconds")
        relatorio = Path("poligon_status.txt")
        conteudo = [
            f"timestamp={agora}",
            f"modo_privado={MODO_PRIVADO_SEM_API}",
            f"cwd={Path.cwd()}",
            f"historico_memoria={len(historico)}",
        ]
        relatorio.write_text("\n".join(conteudo), encoding="utf-8")


agente_idle = AgenteIdle(intervalo=IDLE_INTERVALO)


def falar(texto):
    print(f"\nPoligon: {texto}")
    texto_limpo = texto.replace("*", "").replace("#", "")
    arquivo = "voz.mp3"
    asyncio.run(edge_tts.Communicate(texto_limpo, "pt-BR-AntonioNeural", rate="+20%").save(arquivo))
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    if os.path.exists(arquivo):
        try:
            os.remove(arquivo)
        except OSError:
            pass


def capturar_tela():
    if MODO_PRIVADO_SEM_API:
        return None
    try:
        img = ImageGrab.grab()
        largura, altura = img.size
        return img.resize((largura // 2, altura // 2))
    except Exception as e:
        print(f"Erro ao capturar tela: {e}")
        return None


def responder_offline(pergunta):
    pergunta_l = pergunta.lower()
    if "hora" in pergunta_l:
        agora = datetime.datetime.now().strftime("%H:%M")
        return f"Agora são {agora}."
    if "status" in pergunta_l and "agente" in pergunta_l:
        return agente_idle.status()
    return "Modo privado ativo. Posso executar comandos locais e tarefas de agente idle sem enviar seus dados para API."


def perguntar_ia(pergunta, imagem_tela):
    if MODO_PRIVADO_SEM_API or client is None:
        resposta = responder_offline(pergunta)
        historico.extend([f"Mestre: {pergunta}", f"Poligon: {resposta}"])
        return resposta
    try:
        buffered = BytesIO()
        imagem_tela.save(buffered, format="JPEG")
        imagem_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        memoria = "\n".join(historico[-4:])
        prompt = f"Você é Poligon. Responda de forma direta.\nHistórico:\n{memoria}\nPergunta: {pergunta}"
        mensagens = [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{imagem_base64}"}}]}]
        resposta = client.chat.completions.create(model="meta-llama/llama-4-scout-17b-16e-instruct", messages=mensagens)
        texto = resposta.choices[0].message.content
        historico.extend([f"Mestre: {pergunta}", f"Poligon: {texto}"])
        return texto
    except Exception:
        return "Falha de conexão com serviço externo de IA."


def executar_comando(comando):
    c = comando.lower()
    if "hora" in c:
        falar(f"Agora são {datetime.datetime.now().strftime('%H e %M')}.")
        return True
    if "abrir youtube" in c:
        webbrowser.open("https://youtube.com")
        falar("Iniciando YouTube.")
        return True
    if "iniciar agente" in c:
        agente_idle.iniciar()
        falar("Agente autônomo iniciado em modo idle.")
        return True
    if "parar agente" in c:
        agente_idle.parar()
        falar("Agente autônomo pausado.")
        return True
    if "status agente" in c:
        falar(agente_idle.status())
        return True
    if "agendar relatorio" in c:
        agente_idle.adicionar_tarefa("relatorio_sistema")
        falar("Tarefa de relatório adicionada à fila do agente.")
        return True
    if "agendar navegador" in c:
        agente_idle.adicionar_tarefa("abrir_navegador")
        falar("Tarefa para abrir navegador adicionada.")
        return True

    if "abrir" in c or "iniciar" in c:
        app_alvo = c.replace("abrir", "").replace("iniciar", "").replace("o", "").replace("a", "").strip()
        if not app_alvo:
            return False
        for chave, executavel in ATALHOS_DIRETOS.items():
            if chave in app_alvo:
                os.system(executavel)
                falar(f"Iniciando {chave}.")
                return True
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write(app_alvo)
        time.sleep(0.6)
        pyautogui.press("enter")
        falar(f"Iniciando {app_alvo}.")
        return True
    return False


def iniciar():
    recognizer = sr.Recognizer()
    falar("Sistemas online. Modo privado ativo por padrão. Diga Poligon para me chamar.")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while True:
            try:
                audio = recognizer.listen(source)
                texto = recognizer.recognize_google(audio, language="pt-BR").lower()
                if any(g in texto for g in ["poligon", "polígono", "polly"]):
                    falar("Ao seu dispor.")
                    audio_comando = recognizer.listen(source, timeout=7, phrase_time_limit=15)
                    comando = recognizer.recognize_google(audio_comando, language="pt-BR")
                    if not executar_comando(comando):
                        resposta = perguntar_ia(comando, capturar_tela())
                        falar(resposta)
            except Exception:
                continue


if __name__ == "__main__":
    iniciar()
