import os
import base64
import tempfile
from openai import AzureOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import JSONResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

env_path = Path(__file__).resolve(strict=True).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Carregar as variáveis de ambiente do arquivo .env
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


# Configuração do FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Configuração do cliente OpenAI
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint= AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME)

def criar_prompt_modelo_ameacas(tipo_aplicacao, 
                                autenticacao, 
                                acesso_internet, 
                                dados_sensiveis, 
                                descricao_aplicacao):
    prompt = """Aja como um especialista sênior em cibersegurança com mais de 20 anos de experiência 
    em modelagem de ameaças utilizando a metodologia STRIDE. Sua missão é analisar minuciosamente 
    a aplicação descrita e produzir um modelo de ameaças abrangente e específico.

    **CONTEXTO DA ANÁLISE:**
    - Tipo de Aplicação: {tipo_aplicacao}
    - Métodos de Autenticação: {autenticacao}
    - Exposta na Internet: {acesso_internet}
    - Dados Sensíveis Manipulados: {dados_sensiveis}
    - Descrição Técnica Detalhada: {descricao_aplicacao}

    **INSTRUÇÕES ESPECÍFICAS:**

    1. **ANÁLISE ESTRUTURADA POR CATEGORIA STRIDE:**
      Para cada categoria do STRIDE, identifique 3-4 ameaças REALMENTEs específicas e plausíveis:
      - Spoofing (Falsificação de Identidade)
      - Tampering (Violação de Integridade) 
      - Repudiation (Repúdio)
      - Information Disclosure (Divulgação de Informações)
      - Denial of Service (Negação de Serviço)
      - Elevation of Privilege (Elevação de Privilégio)

    2. **CRITÉRIOS DE QUALIDADE PARA AS AMEAÇAS:**
      - Baseadas em vetores de ataque reais e técnicas MITRE ATT&CK aplicáveis
      - Contextualizadas especificamente para esta aplicação
      - Considerando a arquitetura, dados sensíveis e métodos de autenticação
      - Com cenários concretos e impactos mensuráveis

    3. **FORMATO DE SAÍDA EXIGIDO:**
      JSON estruturado com:
      {
        "threat_model": [
          {
            "Threat Type": "Categoria STRIDE",
            "Scenario": "Descrição técnica detalhada do cenário de ameaça",
            "Potential Impact": "Impacto específico e quantificável quando possível"
          }
        ],
        "improvement_suggestions": [
          "Sugestões específicas sobre informações técnicas faltantes"
        ]
      }

    4. **DETALHAMENTO TÉCNICO OBRIGATÓRIO:**
      Cada ameaça deve incluir:
      - Vetor de ataque técnico específico
      - Condições necessárias para exploração
      - Impacto operacional/negócio
      - Relação com os componentes da aplicação

    5. **SUGESTÕES DE MELHORIA FOCADAS:**
      Identifique apenas lacunas de informação que impediram análise mais precisa:
      - Detalhes de arquitetura de rede e segmentação
      - Especificações de criptografia e armazenamento de secrets
      - Fluxos de dados críticos não documentados
      - Controles de acesso em nível granular
      - Mecanismos de logging e auditoria
      - Dependências externas e integrações

    **EXEMPLO DE AMEAÇA BEM ELABORADA:**
    {{
      "Threat Type": "Tampering",
      "Scenario": "Injeção de comandos SQL através do parâmetro 'user_id' na API /api/v1/profile devido à falta de parameterized queries, permitindo modificação não autorizada de dados de usuários",
      "Potential Impact": "Comprometimento de 100% dos registros de usuários, violação de LGPD com multas de até 2% do faturamento"
    }}

    **RESTRIÇÕES:**
    - Não inclua ameaças genéricas não relacionadas à aplicação
    - Foque em cenários técnicos específicos, não em recomendações genéricas
    - Baseie-se apenas nas informações fornecidas, indicando lacunas quando necessário
    - Mantenha linguagem técnica precisa e específica

    Gere agora a análise completa baseada nos dados fornecidos."""

    return prompt

@app.post("/analisar_ameacas")
async def analisar_ameacas(
    imagem: UploadFile = File(...),
    tipo_aplicacao: str = Form(...),
    autenticacao: str = Form(...),
    acesso_internet: str = Form(...),
    dados_sensiveis: str = Form(...),
    descricao_aplicacao: str = Form(...)
):
    try:
        
        print(imagem)
        # Criar o prompt para o modelo de ameaças
        prompt = criar_prompt_modelo_ameacas(tipo_aplicacao, 
                                              autenticacao, 
                                              acesso_internet, 
                                              dados_sensiveis, 
                                              descricao_aplicacao)
        # Salvar a imagem temporariamente
        content = await imagem.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(imagem.filename).suffix) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Convert imagem para base64
        with open(temp_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('ascii')


        # Adicionar a imagem codificada ao prompt
        chat_prompt = [
            {"role": "system", "content": "Você é uma IA especialista em cibersegurança, que analisa desenhos de arquitetura."},
            {"role": "user"
             , "content": [
                {"type": "text"
                 , "text": prompt
                 },
                {
                    "type": "image_url"
                 ,  "image_url": {"url": f"data:image/png;base64,{encoded_string}"}
                 },
                {"type": "text", 
                 "text": "Por favor, analise a imagem e o texto acima e forneça um modelo de ameaças detalhado."
                 }]
        }]
        # Chamar o modelo OpenAI
        response = client.chat.completions.create(
            messages = chat_prompt,
            temperature=0.7,
            max_tokens=1500,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream= False,
            model= AZURE_OPENAI_DEPLOYMENT_NAME
        )
        os.remove(temp_file_path)  # Remover o arquivo temporário após o uso

        # Retornar a resposta do modelo
        return JSONResponse(content=response.to_dict(), status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
