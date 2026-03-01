from pypdf import PdfReader
from agent import analisadorCurriculo

def descricaoVaga():
    with open("vaga.txt", "r") as file:
        content = file.read()
    return content

def main():
    reader = PdfReader("CV/curriculo.pdf")
    text_from_all_pages = []
    for page in reader.pages:
        text_from_all_pages.append(page.extract_text())
    curriculoEmString = " ".join(text_from_all_pages)
    vaga = descricaoVaga()
    mensagem = f"Currículo: {curriculoEmString}\n\nDescrição da vaga: {vaga}"
    analisadorCurriculo.print_response(mensagem)


if __name__ == "__main__":
    main()
