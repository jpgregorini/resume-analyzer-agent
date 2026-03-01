from agno.models.openai import OpenAIChat
from agno.agent import Agent
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
load_dotenv()

class Analisador(BaseModel):
    resumoCurriculo : str = Field(description="Resumo do curriculo em 100 ou menos palavras")
    pontos_fortes : str = Field(description="Pontos fortes do currículo")
    pontos_fracos : str = Field(description="Pontos fracos do currículo")
    nota : float = Field(description="Nota de 0 a 10.")

model = OpenAIChat(id="gpt-4o", name= "analisador", api_key=os.getenv("OPENAI_API_KEY"))

analisadorCurriculo = Agent(
    model=model,
    instructions="""
    Você é um analisador de Currículo, seu trabalho é analisar os currículos e comparar
    com a vaga que estão aplicando. Você deve elencar pontos fortes e fracos do currìculo,
    sendo imparcial e verdadeiro. Ao final da sua análise, dê uma nota de 0 a 10, sendo 10 
    perfeito para o trabalho e 0 sendo o oposto do que a empresa busca.
""",
response_model=Analisador
)
