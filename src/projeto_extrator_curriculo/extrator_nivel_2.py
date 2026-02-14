import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard
from typing import List, Literal

from guardrails.hub import ValidLength

load_dotenv()

MODEL_DEFAULT = "openrouter/meta-llama/llama-3.3-70b-instruct:free"

class Experiencia(BaseModel):
    empresa: str = Field(description="Nome da empresa onde trabalhou")
    cargo: str = Field(description="Cargo ocupado")
    anos: int = Field(description="Duração em anos (número inteiro)")
    
class Curriculo(BaseModel):
    nome_completo: str = Field(description="Nome do candidato em Title Case")
    
    resumo: str = Field(
        description="Um resumo executivo do perfil",
        validators=[ValidLength(min=10, max=50, on_fail="reask")] 
    )
    
    habilidades_tecnicas: List[str] = Field(description="Lista de hard skills (ex: Python, SQL)")
    historico: List[Experiencia] = Field(description="Lista das experiências profissionais")
    
    senioridade_calculada: Literal["Júnior", "Pleno", "Sênior"] = Field(
        description="Classifique APENAS como: Júnior, Pleno ou Sênior com base nos anos"
    )
    
guard = Guard.for_pydantic(output_class=Curriculo)


# --- O TESTE ---
# Vamos forçar um erro. O resumo gerado naturalmente teria mais de 50 caracteres.
texto_baguncado = """
Fala galera, sou o Carlos Silva. Tô na área de dados tem uns 5 anos. 
Passei 2 anos na TechSolutions como analista jr, depois trabalhei na Totvs por 2 anos como analista pleno, e agora tô na DataCorp fechando 1 ano como cientista de dados.
"""

print("Enviando para o LLM via Guardrails (Com validação de tamanho)...")


try:
    # ### NOVO: num_reasks=2
    # Damos ao LLM 2 chances extras para corrigir o erro de validação.
    raw_llm_output, validated_output, *rest = guard(
        model=MODEL_DEFAULT,
        messages=[
            {"role": "system", "content": "Você é um especialista em RH."},
            {"role": "user", "content": texto_baguncado}
        ],
        num_reasks=2 
    )

    if validated_output:
        print("\n--- SUCESSO! ---")
        print(f"Resumo Validado ({len(validated_output['resumo'])} chars): {validated_output['resumo']}")
        print("\n--- JSON COMPLETO ---")
        print(validated_output)
    else:
        print("O Guardrails não conseguiu corrigir a saída após as tentativas.")
        
except Exception as e:
    print(f"\nErro ou Falha de Validação Final: {e}")