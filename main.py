from pypdf import PdfReader
from agent import analisadorCurriculo
import os


def descricaoVaga():
    with open("vaga.txt", "r") as file:
        content = file.read()
    return content

def main():
    allCVs = []
    for curriculo in os.listdir("CV/"):
        if ".pdf" in curriculo:
            reader = PdfReader(os.path.join("CV", curriculo))
            text_from_all_pages = []
            for page in reader.pages:
                text_from_all_pages.append(page.extract_text())
            curriculoEmString = " ".join(text_from_all_pages)
            allCVs.append(curriculoEmString)
            curriculoEmString = ""
        else:
            continue

    analise = []
    vaga = descricaoVaga()

    for cv in allCVs:
        mensagem = f"Currículo: {cv}\n\nDescrição da vaga: {vaga}"
        msg = analisadorCurriculo.run(mensagem).content
        analise.append(msg)
    

    ranking = sorted(analise, key=lambda candidato: candidato.nota, reverse=True)  
    for candidato in ranking:
        print(f"Nome: {candidato.nome}")
        print(f"Contato: {candidato.telefone}")
        print(f"nota: {candidato.nota}")
        print(f"resumo: {candidato.resumoCurriculo}")
        print(f"pontos fortes: {candidato.pontos_fortes}")
        print(f"pontos fracos: {candidato.pontos_fracos}")

if __name__ == "__main__":
    main()

