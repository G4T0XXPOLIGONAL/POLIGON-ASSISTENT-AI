# 🤖 POLIGON ASSISTENT

Assistente de desktop por voz com automação local, modo privado e operação como agente em idle.

## Novidades desta versão

- **Agente autônomo em idle** com fila de tarefas local (`iniciar agente`, `parar agente`, `status agente`).
- **Agendamento de tarefas por voz** (`agendar relatorio`, `agendar navegador`).
- **Relatório periódico local** (`poligon_status.txt`) e log do agente (`poligon_agent.log`).
- **Modo privado padrão** (`POLIGON_SEM_API=1`) para não enviar tela/perguntas para API externa.

## Configuração

```bash
pip install -r requirements.txt
```

### Modo privado (recomendado)
```bash
export POLIGON_SEM_API=1
python poligon_assistent.py
```

### Modo online opcional
```bash
export POLIGON_SEM_API=0
export GROQ_API_KEY="sua_chave"
python poligon_assistent.py
```

## Variáveis de ambiente

- `POLIGON_SEM_API` (default `1`): ativa modo privado.
- `GROQ_API_KEY`: chave da API Groq quando quiser modo online.
- `POLIGON_IDLE_INTERVALO` (default `300`): intervalo (segundos) do ciclo de tarefas idle.

## Skill solicitada

A skill personalizada foi adicionada no arquivo `G4T0XX_MASTER_KERNEL_OVERRIDE.md`.
