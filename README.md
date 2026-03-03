# Analisador de Currículos com IA

Esse projeto nasceu de uma ideia simples: automatizar a triagem de currículos usando IA. Você manda os PDFs, ele analisa cada um, compara com a vaga e devolve um ranking do mais ao menos compatível.

Por baixo do capô tem Python, Agno (framework pra agentes de IA), OpenAI GPT-4o e FastAPI. O agente lê o currículo, entende o que a empresa quer e dá uma nota de 0 a 10 pra cada candidato — com justificativa.

---

## O que ele faz

Você faz um POST na API mandando os PDFs dos candidatos. O sistema:

1. Extrai o texto de cada PDF
2. Compara com a descrição da vaga (arquivo `vaga.txt`)
3. Manda pro agente de IA analisar
4. Retorna um ranking JSON ordenado pela nota, com pontos fortes, pontos fracos e resumo de cada candidato

---

## Stack

- Python 3.14
- [Agno](https://docs.agno.com) — pra construir o agente
- OpenAI GPT-4o — o modelo que faz a análise
- FastAPI — a API que recebe os currículos
- pypdf — pra extrair texto dos PDFs
- Pydantic — pra garantir que o output do agente sempre vem estruturado

---

## Estrutura

```
analisadorCurriculo/
├── agent.py        # definição do agente e schema Pydantic
├── main.py         # API FastAPI com o endpoint /sendCV/
├── vaga.txt        # descrição da vaga que será usada na análise
├── .env            # suas chaves de API (não sobe pro git)
├── .env.example    # modelo do .env
├── requirements.txt
└── CV/             # pasta onde ficam os PDFs (opcional, veja abaixo)
```

---

## Como usar

Com o servidor rodando, abra outro terminal e manda os currículos via curl:

```bash
curl -X POST "http://127.0.0.1:8000/sendCV/" \
  -F "files=@curriculo.pdf"

curl -X POST "http://127.0.0.1:8000/sendCV/" \
  -F "files=@cv_joao.pdf" \
  -F "files=@cv_maria.pdf" \
  -F "files=@cv_pedro.pdf"
```

Ou acessa `http://127.0.0.1:8000/docs` pra usar a interface do Swagger.

---

## Exemplo do retorno

```json
[
  {
    "nome": "João Pedro Gregorini",
    "telefone": "(11) 99999-9999",
    "nota": 8.5,
    "resumo do curriculo": "Desenvolvedor backend com 3 anos de experiência em Python, Django e APIs REST. Inglês C2 e experiência com automação e IA.",
    "pontos fortes": "Experiência sólida com Python e frameworks web, inglês avançado e conhecimento em IA, que se alinham diretamente com os requisitos da vaga.",
    "pontos fracos": "Pouca experiência com cloud e arquitetura de microsserviços, mencionados como diferenciais na vaga."
  },
  {
    "nome": "Maria Silva",
    "telefone": "(21) 98888-8888",
    "nota": 6.2,
    "resumo do curriculo": "Analista de sistemas com foco em backend Java e experiência em bancos de dados relacionais.",
    "pontos fortes": "Boa base em desenvolvimento backend e banco de dados.",
    "pontos fracos": "Stack diferente da exigida na vaga e sem experiência com Python ou IA." 
  }
]
```