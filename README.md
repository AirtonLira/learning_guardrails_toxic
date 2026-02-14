# AI Guardrails - Estudos e Experimentos

Fala, mano! Esse repositorio aqui eh um projeto de estudo que montei pra entender na pratica como funciona a biblioteca **Guardrails AI**. A ideia eh simples: aprender como validar e estruturar as respostas que vem dos modelos de linguagem (LLMs), garantindo que a saida esteja no formato certo e com os dados que a gente espera.

Nao eh nada de producao, eh pra aprendizado mesmo. Fui testando, errando, ajustando e documentando tudo num notebook Jupyter pra ficar mais facil de acompanhar o raciocinio.

## O que foi feito

O projeto ta organizado num notebook (`src/validations.ipynb`) com exemplos progressivos de validacao usando Guardrails:

### Exemplo 1 - Validacao basica com Pydantic
Validacao simples de saida estruturada. O modelo recebe um prompt pedindo sugestao de pet e retorna um JSON validado com nome e tipo do animal, tudo tipado com Pydantic.

### Exemplo 2 - Listas e objetos aninhados
Validacao de estruturas mais complexas. O modelo retorna uma cesta com frutas, cada uma com nome e cor, validando uma lista de objetos Pydantic aninhados.

### Exemplo 3 - Validacao com RegexMatch
Extracao de dados de um historico de chat de entregas. Usa o validator `RegexMatch` do Guardrails Hub pra garantir que o nome do cliente siga um padrao especifico via expressao regular.

### Exemplo 4 - Validator customizado com modelo de ML
Esse eh o mais da hora. Criei um validator personalizado chamado `ToxicLanguageValidator` que usa o modelo `toxic-bert` da Hugging Face pra detectar linguagem toxica na saida do LLM. Se o texto passar do threshold de toxicidade, a validacao falha.

## Stack e requisitos

- **Python** >= 3.10
- **guardrails-ai** >= 0.8.1
- **openai** >= 2.21.0
- **torch** >= 2.10.0
- **transformers** >= 5.1.0
- **ipykernel** >= 7.2.0
- **python-dotenv**
- **LiteLLM** (dependencia do guardrails)

O LLM usado nos exemplos roda via **OpenRouter** com modelo gratuito (`meta-llama/llama-3.3-70b-instruct:free`), entao voce precisa de uma API key do OpenRouter configurada no `.env`:

```
OPENAI_API_KEY="sua-chave-do-openrouter-aqui"
```

## Como rodar

1. Clone o repositorio
2. Instale as dependencias com `uv`:
```bash
uv sync
```
3. Instale o validator do Guardrails Hub:
```bash
guardrails hub install hub://guardrails/regex_match
```
4. Crie o arquivo `.env` na raiz com sua chave do OpenRouter
5. Abra o notebook `src/validations.ipynb` e execute as celulas em ordem

## Sobre

Esse projeto foi feito puramente pra fins de estudo. Queria entender melhor como o Guardrails AI funciona, como integrar validators prontos do Hub, como criar validators customizados com modelos de ML e como usar tudo isso com provedores de LLM gratuitos via OpenRouter.

## Autor

**Airton Lira Junior**
