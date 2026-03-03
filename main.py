from pypdf import PdfReader
from agent import analisadorCurriculo
import uvicorn
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from io import BytesIO
import os

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="API DO JP",
    description="Testando essa coisa",
    version="0.1.0",
    contact={
        "name" : "Joao",
        "email" : "joao@example.com"
    })

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def descricao_vaga():
    if not os.path.exists("vaga.txt"):
        raise HTTPException(500, "Arquivo vaga.txt não encontrado")
    with open("vaga.txt", "r", encoding="utf-8") as file:
        return file.read()

def processar_pdfs(lista: list):
    allCVs = []
    for i, curriculo in enumerate(lista):
        try:
            reader = PdfReader(curriculo)
            pages = [page.extract_text() or "" for page in reader.pages]
            allCVs.append(" ".join(pages))
        except Exception as e:
            print(f"Erro ao ler PDF {i}: {e}")
            allCVs.append("")  # mantém a posição na lista
    return allCVs

@app.post("/sendCV/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(400, "Nenhum arquivo enviado")

    pdfs = []
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(400, f"'{file.filename}' nao e um PDF valido")
        arquivos_bytes = await file.read()
        pdfs.append(BytesIO(arquivos_bytes))

    pdfs_processados = processar_pdfs(pdfs)
    analise = []
    vaga = descricao_vaga()

    for i, cv in enumerate(pdfs_processados):
        mensagem = f"Currículo: {cv}\n\nDescrição da vaga: {vaga}"
        try:
            msg = analisadorCurriculo.run(mensagem).content
            analise.append(msg)
        except Exception as e:
            print(f"Erro ao processar currículo {i}: {e}")

    ranking = sorted(analise, key=lambda c: c.nota, reverse=True)
    return [{"nome": c.nome, "telefone": c.telefone, "nota": c.nota,
             "resumo do curriculo": c.resumoCurriculo,
             "pontos fortes": c.pontos_fortes,
             "pontos fracos": c.pontos_fracos} for c in ranking]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)