
import os
from dotenv import load_dotenv

load_dotenv()

# Perfil configurado para Victor Balestrassi: Analista de Suporte Técnico
# N2, com atuação em integração de sistemas fiscais e ERP (Oracle Fusion
# AP, SAP, Oracle APEX, PL/SQL, NF-e/NFS-e/CT-e). Só interessa vaga REMOTA
# (qualquer cidade, ver CIDADES abaixo) em país que fale português ou
# inglês (ver MERCADOS_REMOTO_ACEITOS).

# Cargo forte: título que só existe mesmo em vaga de suporte técnico/
# integração de sistemas, sem possibilidade real de ser outra área.
KEYWORDS_CARGO_FORTE = [
    "Analista de Suporte Técnico N2",
    "Analista de Suporte N2",
    "Analista de Suporte Nível 2",
    "Analista de Suporte Técnico Nível 2",
    "Suporte Técnico N2",
    "Suporte N2",
    "Suporte Nível 2",
    "Technical Support Analyst",
    "IT Support Analyst",
    "ERP Support Analyst",
    "Support Analyst",
    "Support Engineer",
    "Technical Support Engineer",
    "IT Support Engineer",
    "Tier 2 Support",
    "Level 2 Support",
    "L2 Support",
    "N2 Support",
    "Analista de Suporte Técnico",
    "Analista de Helpdesk",
    "Analista de Help Desk",
    "Analista de Service Desk",
    "Service Desk Analyst",
    "Help Desk Analyst",
    "Analista de Integração de Sistemas",
    "Analista de Integração",
    "Integration Analyst",
    "Systems Integration Analyst",
    "Analista Fiscal de Sistemas",
    "Analista de Sistemas Fiscais",
    "Tax Systems Analyst",
    "Oracle Support Analyst",
    "SAP Support Analyst",
    "Oracle Fusion Support Analyst",
    "ERP Analyst",
    # "Analista de Suporte" saiu da lista ambígua por pedido explícito do
    # usuário: mesmo sem qualificador junto (ex: "TI"/"técnico"), ele quer
    # ver essa vaga — aceita direto, sem exigir contexto adicional no
    # título.
    "Analista de Suporte",
]

# Cargo ambíguo: título que também é usado em vaga sem nada a ver com
# suporte técnico/ERP (ex: "Suporte" sozinho existe em suporte comercial,
# RH, vendas... qualquer área; "Analista Fiscal" existe em contabilidade
# pura, sem nada de sistemas). Só conta como match se o título TAMBÉM
# tiver um QUALIFICADORES_DADOS junto.
KEYWORDS_CARGO_AMBIGUO = [
    "Suporte",
    "Analista de Sistemas",
    "Analista Fiscal",
    "Functional Analyst",
    "SAP Analyst",
    "Oracle Analyst",
    "IT Analyst",
    "Consultor SAP",
    "Consultor Oracle",
    "SAP Consultant",
    "Oracle Consultant",
]

# Termo que precisa aparecer junto no título quando o cargo é ambíguo, pra
# confirmar que é vaga de suporte técnico/ERP/integração fiscal e não de
# outra área qualquer. NÃO inclui "suporte"/"support" aqui: como esses
# termos já são a própria KEYWORDS_CARGO_AMBIGUO, incluí-los aqui tornaria
# a exigência de qualificador circular (o próprio cargo ambíguo já contém a
# palavra que deveria confirmá-lo) — "Analista de Suporte" sozinho passaria
# sempre, o que é exatamente o falso positivo que essa regra existe pra
# evitar (suporte comercial, suporte a vendas etc.).
QUALIFICADORES_DADOS = [
    "técnico",
    "tecnico",
    "technical",
    "ti",
    "it",
    "sistemas",
    "systems",
    "erp",
    "sap",
    "oracle",
    "fiscal",
    "nf-e",
    "nfe",
    "nfs-e",
    "nfse",
    "ct-e",
    "cte",
    "sql",
    "integração",
    "integracao",
    "integration",
    "helpdesk",
    "help desk",
    "service desk",
    "n2",
    "nível 2",
    "nivel 2",
    "level 2",
    "tier 2",
]

# Ferramenta que aparece como núcleo do título (ex: "Analista SAP",
# "Consultor Oracle Fusion"). Só conta como match se o título TAMBÉM tiver
# uma palavra de cargo — evita que "SAP"/"Oracle"/"PL/SQL" sozinho aprove
# vaga de desenvolvimento pura ("SAP Developer", "PL/SQL Developer"), que
# não é o perfil buscado (suporte/análise, não programação).
FERRAMENTAS_TITULO = [
    "SAP",
    "Oracle Fusion",
    "Oracle EBS",
    "Oracle APEX",
    "PL/SQL",
]

# Palavra de cargo que confirma que a vaga de ferramenta é de suporte/
# análise. "desenvolvedor"/"developer"/"engenheiro de software" ficam FORA
# de propósito: é o que mantém vaga de programação pura fora do radar
# (perfil é suporte técnico, não desenvolvimento).
QUALIFICADORES_CARGO = [
    "analista",
    "analyst",
    "suporte",
    "support",
    "especialista",
    "specialist",
    "consultor",
    "consultant",
]

KEYWORDS = KEYWORDS_CARGO_FORTE + KEYWORDS_CARGO_AMBIGUO

# Termos de busca enviados a cada site. Ficam separados das KEYWORDS de
# propósito: TERMOS_BUSCA é a rede ampla (o que é pesquisado em cada site,
# incluindo termo de ferramenta/stack pra achar vaga com título atípico),
# enquanto KEYWORDS é o filtro final e só olha o título da vaga já
# encontrada.
#
# TERMOS_CARGO é derivado direto de KEYWORDS (em vez de mantido à mão em
# lista separada) — toda keyword nova em KEYWORDS já vira busca também,
# sem risco de duas listas divergirem.
TERMOS_CARGO_EXTRA = [
    # termos mais amplos que a keyword exata, mantidos por dar rede mais
    # larga na busca (a keyword em si é mais restrita, de propósito, pra
    # não gerar falso positivo no filtro de título).
    "suporte n2",
    "suporte técnico",
    "technical support",
    "service desk",
    "help desk",
    "erp support",
    "integração de sistemas",
    "analista fiscal",
]

TERMOS_CARGO = sorted(set(k.lower() for k in KEYWORDS) | set(TERMOS_CARGO_EXTRA))

# Termos de ferramenta/stack — dá rede mais ampla que só o cargo (vaga com
# título atípico que cita a stack como diferencial). Um termo de ferramenta
# só resulta em notificação se o TÍTULO da vaga também bater com uma
# keyword de cargo (mesma regra de FERRAMENTAS_TITULO acima) — evita falso
# positivo de vaga que só cita a ferramenta em algum ponto do anúncio.
TERMOS_FERRAMENTA = [
    "oracle fusion",
    "sap erp",
    "pl/sql",
    "oracle apex",
    "nf-e",
    "nfs-e",
]

TERMOS_BUSCA = TERMOS_CARGO + TERMOS_FERRAMENTA

# MEDIDO: os TERMOS_BUSCA inteiros rodando em TODO ciclo é o que gera as
# centenas de sessões de navegador por execução — o custo cresce linear com
# o tamanho da lista. TERMOS_POR_CICLO é o tamanho do BLOCO usado por ciclo,
# não o total de termos — main.py roda um bloco por vez em rodízio (ver
# _proximo_bloco_termos) e avança pro próximo bloco no ciclo seguinte,
# salvando a posição no jobs.db. Isso desacopla custo por ciclo de tamanho
# da lista de termos.
TERMOS_POR_CICLO = 10

# Perfil aceita QUALQUER cidade, desde que a vaga seja 100% remota — não há
# whitelist de cidade pra vaga híbrida/presencial. "Remoto" continua na
# lista porque é a porta de entrada da regra de modalidade remota (ver
# _FLAGS_REMOTO em job.py) — é o único valor aqui, então toda vaga híbrida/
# presencial (de qualquer cidade) é rejeitada, e só remoto passa.
CIDADES = [
    "Remoto",
]

# Não usado neste perfil (CIDADES já cobre "qualquer cidade, desde que
# remoto" sem precisar de eixo geográfico à parte) — mantido só porque
# config_intl.py importa este nome. Ver ATIVAR_EIXO_IBERICO_BR abaixo
# (desligado).
CIDADES_EUROPA_IBERICA = [
    "Portugal",
    "Lisboa",
    "Porto",
    "Braga",
    "Espanha",
    "España",
    "Spain",
    "Madrid",
    "Barcelona",
    "Valencia",
]

# DESLIGADO: perfil só quer vaga remota, então o eixo "presencial/híbrido
# na Ibéria, marcado como exploratório" não se aplica — vaga presencial ou
# híbrida em qualquer lugar (Ibéria incluída) já é rejeitada por CIDADES
# acima, sem precisar de eixo à parte.
ATIVAR_EIXO_IBERICO_BR = False

# LinkedInScraper é a única fonte do pipeline BR que também alcança vaga
# fora do Brasil — as outras são portais brasileiros.
#
# Vazio de propósito: como o perfil só quer remoto (nunca híbrido/
# presencial, nem no Brasil), não faz sentido rodar a passada de "modalidade
# completa" (que inclui presencial/híbrido) pra nenhum mercado — todo o
# resultado presencial/híbrido dela seria descartado por CIDADES=["Remoto"]
# mesmo assim. O Brasil entra em LOCATIONS_LINKEDIN_REMOTO_APENAS abaixo,
# junto com os outros mercados aceitos, só com a passada f_WT=2 (remoto).
LOCATIONS_LINKEDIN = []

# Mercados onde só interessa vaga REMOTA (f_WT=2) — Brasil entra aqui (não
# em LOCATIONS_LINKEDIN) porque só a modalidade remota interessa, mesmo
# morando aqui. Resto da lista é país de língua portuguesa ou inglesa com
# volume real de vaga de TI/suporte no LinkedIn — lista enxuta de propósito
# (cada país aqui multiplica busca × termo); MERCADOS_REMOTO_ACEITOS abaixo
# é mais abrangente porque aceitar é comparação de string (custo zero),
# achar exige busca de verdade (custo real).
LOCATIONS_LINKEDIN_REMOTO_APENAS = [
    "Brasil",
    "Portugal",
    "Estados Unidos",
    "Reino Unido",
    "Canadá",
    "Irlanda",
    "Austrália",
]

# Não usado neste perfil (LOCATIONS_LINKEDIN vazio, então a derivação abaixo
# também fica vazia) — mantido pelo mesmo motivo de compatibilidade que
# CIDADES_EUROPA_IBERICA.
LOCATIONS_LINKEDIN_CIDADES_PRESENCIAL = [c for c in CIDADES if c != "Remoto"]

# Mercado que a vaga remota precisa aceitar pra contar, quando o texto de
# local DECLARA um escopo geográfico ("Remote — US only", "Remote — India").
# Ver Job.escopo_remoto/RegrasFiltro.mercados_remoto_aceitos em job.py — sem
# isso, uma vaga remota só pra outro país passava igual a uma remota de
# verdade pro candidato. Vaga remota SEM escopo declarado no texto (a
# grande maioria) continua batendo normalmente, isso só filtra quando a
# fonte EXPLICITA um mercado incompatível.
#
# Cobre os dois eixos do requisito ("qualquer país que fale português ou
# inglês"): Lusofonia com job market relevante (Brasil, Portugal, Angola,
# Moçambique, Cabo Verde) + Anglosfera (Estados Unidos, Reino Unido,
# Canadá, Irlanda, Austrália, Nova Zelândia, África do Sul) — todos já
# mapeados em _MERCADOS_REMOTO (job.py).
MERCADOS_REMOTO_ACEITOS = [
    "Brasil",
    "Portugal",
    "Angola",
    "Moçambique",
    "Cabo Verde",
    "Estados Unidos",
    "Reino Unido",
    "Canadá",
    "Irlanda",
    "Austrália",
    "Nova Zelândia",
    "África do Sul",
]

INTERVALO_MINUTOS = int(os.getenv("INTERVALO_MINUTOS", 180))

# Digest ranqueado: vaga com Job.pontuar_relevancia() >= este limiar
# notifica na hora; abaixo disso, fica na fila do digest diário — ver
# _enviar_digest_diario em main.py.
LIMIAR_DIGEST_IMEDIATO = 7

# Hora UTC a partir da qual o digest diário pode sair (uma vez por perfil,
# por dia — ver _enviar_digest_diario em main.py). 9 UTC = ~06h em
# Brasília (UTC-3) / ~07h no horário de Portugal (UTC+1 no horário de
# verão) — chega de manhã, com a lista do dia anterior pronta pra revisar.
DIGEST_HORA_UTC = 9

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Caminho ancorado na RAIZ do projeto, não na pasta deste arquivo — ver
# tests/test_db_path.py. JOBRADAR_DB_PATH existe pra apontar um banco
# descartável em teste/experimento sem risco de escrever no banco real.
_RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.getenv("JOBRADAR_DB_PATH") or os.path.join(_RAIZ_PROJETO, "data", "jobs.db")
