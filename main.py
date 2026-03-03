from pypdf import PdfReader
from agent import analisadorCurriculo
import uvicorn
from typing import List, Annotated
from fastapi import FastAPI, File, UploadFile
from io import BytesIO

app = FastAPI(
    title="API DO JP",
    description="Testando essa coisa",
    version="0.1.0",
    contact={
        "name" : "Joao",
        "email" : "joao@example.com"
    })

def descricao_vaga():
    with open("vaga.txt", "r") as file:
        content = file.read()
    return content

def processar_pdfs(lista : list):
    allCVs = []
    for curriculo in lista:
        reader = PdfReader(curriculo)
        text_from_all_pages = []
        for page in reader.pages:
            text_from_all_pages.append(page.extract_text())
        curriculoEmString = " ".join(text_from_all_pages)
        allCVs.append(curriculoEmString)
    return allCVs

@app.post("/sendCV/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    pdfs = []
    for file in files:
        arquivos_bytes = await file.read()
        pdf_em_memoria = BytesIO(arquivos_bytes)
        pdfs.append(pdf_em_memoria)
    pdfs_processados = processar_pdfs(pdfs)
    analise = []
    vaga = descricao_vaga()

    for cv in pdfs_processados:
        mensagem = f"Currículo: {cv}\n\nDescrição da vaga: {vaga}"
        msg = analisadorCurriculo.run(mensagem).content
        analise.append(msg)
    
    ranking = sorted(analise, key=lambda candidato: candidato.nota, reverse=True)  
    return  [{"nome": candidato.nome,
            "telefone": candidato.telefone,
            "nota": candidato.nota,
            "resumo do curriculo": candidato.resumoCurriculo,
            "pontos fortes": candidato.pontos_fortes,
            "pontos fracos": candidato.pontos_fracos} for candidato in ranking]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)