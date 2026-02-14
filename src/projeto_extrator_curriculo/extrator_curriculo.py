import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard
from typing import List

load_dotenv()

MODEL_DEFAULT = "openrouter/meta-llama/llama-3.3-70b-instruct:free"

class Experiencia(BaseModel):
    empresa: str = Field(description="Nome da empresa onde trabalhou")
    cargo: str = Field(description="Cargo ocupado")
    anos: int = Field(description="Duração em anos (número inteiro)")
    
    
class Curriculo(BaseModel):
    nome_completo: str = Field(description="Nome do candidato em Title Case")
    resumo: str = Field(description="Um resumo executivo de 2 frases do perfil")
    habilidades_tecnicas: List[str] = Field(description="Lista de hard skills (ex: Python, SQL)")
    historico: List[Experiencia] = Field(description="Lista das experiências profissionais")
    # Este campo é especial: pedimos ao LLM para "pensar" e calcular algo
    senioridade_calculada: str = Field(
        description="Júnior, Pleno ou Sênior com base nos anos totais de experiência"
    )
    
guard = Guard.for_pydantic(
    output_class=Curriculo,
    messages=[{
        "role": "system",
        "content": "Analise o texto cru abaixo e extraia as informações seguindo estritamente a estrutura de dados."
    },{
        "role": "user",
        "content": "Texto do currículo: {input}"
    }]
)

# --- O TESTE ---
texto_baguncado = """
    Fala galera, sou o Carlos Silva. Tô na área de dados tem uns 5 anos. 
    Passei 2 anos na TechSolutions como analista jr, e agora tô na DataCorp 
    fechando 3 anos como cientista de dados. 
    Domino Python, Pandas e arranho no Docker.
"""

print("Enviando para o LLM via Guardrails...")

try:
    raw_ll_output, validated_output, *rest = guard(
        model=MODEL_DEFAULT,
        messages=[{"role": "user", "content":texto_baguncado}]
    )
    
    if validated_output:
        print("\n--- Currículo Extraído ---")
        print(f"Candidato: {validated_output['nome_completo']}")
        print(f"Nível: {validated_output['senioridade_calculada']}")
        print(f"Skills: {validated_output['habilidades_tecnicas']}")
        
        print("\n --- JSON COMPLETO (Para API) ---")
        print(validated_output) 
        
    else:
        print("O Guardrails não conseguiu validar a resposta do modelo.")
        
except Exception as e:
    print(f"Erro ao processar o currículo: {e}")