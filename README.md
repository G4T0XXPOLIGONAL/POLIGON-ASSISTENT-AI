# 🤖 POLIGON ASSISTENT

O **POLIGON ASSISTENT** é um assistente virtual de desktop avançado que combina reconhecimento de voz, síntese de fala neural e **visão computacional** através da inteligência artificial. Ele não apenas ouve você, mas também "enxerga" o que está acontecendo na sua tela para oferecer ajuda contextual em tempo real.

---

## 🧠 Como o Projeto Funciona?

O Poligon opera em um ciclo contínuo de **Escuta, Visão e Ação**. Diferente de assistentes comuns, ele utiliza o contexto visual do seu computador para tomar decisões.

1.  **Escuta Ativa:** Utiliza a biblioteca `SpeechRecognition` para monitorar o microfone em busca da *wake-word* "Poligon".
2.  **Processamento Visual:** Ao receber um comando, o assistente captura um print da sua tela com `Pillow`, permitindo que a IA veja o que você está fazendo.
3.  **Inteligência Artificial:** O texto e a imagem são enviados para o modelo **Llama 4** da Groq, processando a resposta com velocidade ultra-rápida.
4.  **Resposta e Execução:** O assistente responde via voz neural (`edge-tts`) e executa comandos no Windows (como abrir apps ou minimizar janelas) usando `pyautogui`.

---

## ✨ Funcionalidades Principais

* **👁️ Visão de Tela:** Analisa o conteúdo da sua tela para tirar dúvidas ou ajudar em tarefas.
* **🎙️ Comando de Voz:** Interação natural ativada por voz.
* **🗣️ Voz Neural:** Fala humana e clara em português (AntonioNeural).
* **🚀 Automação de Atalhos:** Inicia Spotify, Steam, Discord, VRChat e outros instantaneamente.
* **🎮 Modo Jogatina:** Prepara o PC para jogar (abre jogos, Discord e ajusta o som) com um comando.
* **🕒 Utilidades Rápidas:** Informa a hora, abre sites e gerencia janelas do Windows.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **Groq API** (Llama-4-Scout) - Cérebro da IA.
* **SpeechRecognition** - Reconhecimento de fala.
* **Edge-TTS** - Síntese de voz de alta qualidade.
* **PyAutoGUI & Pillow** - Automação e captura de tela.
* **Pygame** - Reprodução de áudio.

---

## 🚀 Como Instalar e Rodar

### 1. Prepare o ambiente
Certifique-se de ter o Python instalado. Clone este repositório ou baixe o arquivo `.py`.

### 2. Instale as dependências
No terminal do VS Code, execute:
```bash
pip install -r requirements.txt
(Ou instale manualmente: pip install groq speechrecognition pygame edge-tts pyautogui Pillow)

3. Configure sua API Key
No arquivo poligon_assistent.py, localize e edite a linha:

Python
API_KEY_GROQ = "SUA_CHAVE_AQUI"
Nota: Obtenha sua chave gratuitamente em Groq Cloud.

4. Inicie o Assistente
Bash
python poligon_assistent.py
⌨️ Comandos de Exemplo
"Poligon, que horas são?"

"Poligon, abrir o YouTube"

"Poligon, ativar modo jogatina"

"Poligon, o que estou vendo na minha tela agora?"