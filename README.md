 🤖 Agente Analisador de Currículos

Um agente de IA construído com **Python + Agno** que analisa currículos em PDF e os compara com descrições de vagas, retornando um relatório estruturado com pontos fortes, pontos fracos e uma nota de compatibilidade.

---

## 📌 O que o projeto faz

O agente recebe um currículo em PDF e uma descrição de vaga em texto, processa as duas informações e devolve um JSON validado com:

- **Resumo do currículo** — visão geral do candidato em até 100 palavras
- **Pontos fortes** — onde o candidato se destaca para a vaga
- **Pontos fracos** — lacunas e gaps em relação ao que a empresa busca
- **Nota** — score de 0 a 10 indicando a compatibilidade com a vaga

---

## 🧱 Stack utilizada

- [Python 3.11+](https://www.python.org/)
- [Agno](https://docs.agno.com) — framework para construção de agentes de IA
- [OpenAI GPT-4o](https://platform.openai.com/) — modelo de linguagem
- [pypdf](https://pypdf.readthedocs.io/) — leitura e extração de texto de PDFs
- [Pydantic](https://docs.pydantic.dev/) — validação e estruturação do output

---

## 📁 Estrutura do projeto

```
resume-analyzer-agent/
├── agent.py          # Definição do agente e schema de output (Pydantic)
├── main.py           # Ponto de entrada: lê o PDF, a vaga e chama o agente
├── .env.example      # Modelo de variáveis de ambiente
├── requirements.txt  # Dependências do projeto
└── sample/
    ├── curriculo.pdf # Currículo de exemplo para teste
    └── vaga.txt      # Descrição de vaga de exemplo
```

---

## ⚙️ Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/resume-analyzer-agent.git
cd resume-analyzer-agent
```

**2. Crie e ative um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Abra o arquivo .env e adicione sua chave da OpenAI
```

**5. Adicione o currículo e a vaga**

Coloque o arquivo `curriculo.pdf` dentro da pasta `CV/` e edite o arquivo `vaga.txt` com a descrição da vaga desejada. Ou use os arquivos de exemplo da pasta `sample/`.

**6. Execute o agente**
```bash
python main.py
```

---

## 📤 Exemplo de output

```json
{
  "resumoCurriculo": "Desenvolvedor backend com 3 anos de experiência em Python e Django, atuando em projetos de e-commerce e APIs REST. Possui conhecimento em Docker e PostgreSQL.",
  "pontos_fortes": "Experiência sólida com Python e frameworks web, familiaridade com containerização e banco de dados relacional, o que atende diretamente aos requisitos técnicos da vaga.",
  "pontos_fracos": "Ausência de experiência com cloud (AWS/GCP) e com arquiteturas de microsserviços, ambos mencionados como diferenciais na descrição da vaga.",
  "nota": 7.4
}
```

---

## 🔐 Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> ⚠️ Nunca suba o arquivo `.env` para o repositório. Ele já está no `.gitignore`.

---

## 🗺️ Arquitetura

```
main.py
  │
  ├── Lê curriculo.pdf com pypdf → extrai texto de todas as páginas
  ├── Lê vaga.txt → carrega descrição da vaga
  ├── Monta mensagem combinando currículo + vaga
  └── Chama analisadorCurriculo.print_response(mensagem)
            │
            └── agent.py
                  ├── GPT-4o processa a mensagem
                  └── Pydantic valida o output → retorna JSON estruturado
```

---

## 📄 Licença

MIT License — sinta-se livre para usar, modificar e distribuir.