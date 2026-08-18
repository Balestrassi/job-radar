
# Config do programa internacional (busca vaga remota fora do Brasil, em
# país de língua inglesa ou portuguesa). Separado do config.py de propósito
# — o pipeline BR (main.py/PERFIL_BR) já cobre o Brasil; este cobre o
# resto do mundo aceito (ver MERCADOS_REMOTO_ACEITOS_INTL abaixo).
#
# Credenciais do Telegram e caminho do banco são os MESMOS do projeto
# principal (reaproveita o bot já configurado, e o dedup por link no mesmo
# jobs.db não tem risco de colisão — o id é hash do link, e vaga
# internacional nunca vai ter o mesmo link de uma vaga brasileira).
from core.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DB_PATH, CIDADES_EUROPA_IBERICA  # noqa: F401

# Mesmo cargo-alvo de config.py (suporte técnico N2 / integração de
# sistemas ERP), só que sem as variantes em espanhol — o mercado deste
# perfil é anglófono + lusófono, não hispanofalante.
KEYWORDS_INTL = [
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
    "Service Desk Analyst",
    "Help Desk Analyst",
    "Integration Analyst",
    "Systems Integration Analyst",
    "ERP Analyst",
    "Oracle Support Analyst",
    "SAP Support Analyst",
    "Analista de Suporte Técnico N2",
    "Analista de Suporte N2",
    "Analista de Suporte Técnico",
    "Analista de Integração de Sistemas",
]

# Termos de busca: cargo puro, sempre escopado por país aceito
# (LOCATIONS_INTL) + remoto (f_WT=2 no LinkedIn, domínio local no Indeed) —
# nunca busca global sem filtro. Diferente do pipeline original (que
# precisava de "spanish speaker"/"portuguese speaker" na frase pra não
# virar busca sem idioma nenhum), aqui o próprio país já é o filtro de
# idioma: US/UK/Irlanda/Canadá/Austrália/Nova Zelândia/África do Sul falam
# inglês, Portugal fala português — não precisa repetir isso no termo.
TERMOS_BUSCA_INTL = [
    "technical support analyst",
    "it support analyst",
    "support analyst",
    "support engineer",
    "service desk analyst",
    "help desk analyst",
    "erp support",
    "integration analyst",
    "sap support",
    "oracle support",
    "analista de suporte técnico",
    "analista de suporte n2",
]

# Rodízio de termos, mesmo mecanismo do TERMOS_POR_CICLO em config.py (ver
# _proximo_bloco_termos em main.py) — chave de metadados própria (sufixo
# "_internacional"), pra não colidir com o rodízio do perfil BR.
TERMOS_POR_CICLO_INTL = 10

# Mercados pesquisados por rodada de busca no LinkedIn/Indeed (parâmetro
# location). Cobre os dois eixos do requisito: Anglosfera (Estados Unidos,
# Reino Unido, Irlanda, Canadá, Austrália, Nova Zelândia, África do Sul) +
# Lusofonia fora do Brasil (Portugal). Angola/Moçambique/Cabo Verde entram
# só em MERCADOS_REMOTO_ACEITOS_INTL (aceitar é comparação de string, custo
# zero) e não aqui (buscar é custo real — volume de vaga de TI remota
# nesses três é baixo o bastante pra não justificar o custo de busca
# dedicada; ainda assim, se aparecerem via LinkedIn/WeWorkRemotely sem
# busca por país, continuam sendo aceitos).
LOCATIONS_INTL = [
    "United States",
    "United Kingdom",
    "Ireland",
    "Canada",
    "Australia",
    "New Zealand",
    "South Africa",
    "Portugal",
]

# Sem cidade nenhuma — só remoto, de qualquer país aceito. "Remote" cobre o
# termo em inglês (a maioria dos cards vai estar em inglês), "Remoto" cobre
# os poucos que vierem em português.
CIDADES_INTL = ["Remote", "Remoto"]

# Ver MERCADOS_REMOTO_ACEITOS em config.py e Job.escopo_remoto/
# extrair_escopo_remoto em job.py. LOCATIONS_INTL é ONDE BUSCAR (custo
# real); esta lista é O QUE ACEITAR (custo zero — só comparação de
# string), por isso pode ser mais abrangente.
#
# NÃO inclui "Brasil" porque esse pipeline é o de vaga remota FORA do
# Brasil (main.py/PERFIL_BR já cobre o Brasil).
MERCADOS_REMOTO_ACEITOS_INTL = [
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

# DESLIGADO: perfil só quer vaga remota (ver mesmo toggle em config.py,
# ATIVAR_EIXO_IBERICO_BR) — vaga presencial/híbrida em Portugal não é o que
# o usuário quer, mesmo achada de propósito via LOCATIONS_INTL.
ATIVAR_EIXO_IBERICO = False

# Indeed usa subdomínio por país, não parâmetro de location como o
# LinkedIn. Cobre os mesmos mercados de LOCATIONS_INTL que têm domínio
# Indeed próprio.
#
# Aviso: Indeed tem proteção anti-bot que pode bloquear acesso automatizado
# (principalmente de IP de nuvem/datacenter), mesmo funcionando em teste
# manual.
DOMINIOS_INDEED_INTL = {
    "Estados Unidos": "www.indeed.com",
    "Reino Unido": "uk.indeed.com",
    "Irlanda": "ie.indeed.com",
    "Canadá": "ca.indeed.com",
    "Austrália": "au.indeed.com",
    "Nova Zelândia": "nz.indeed.com",
    "África do Sul": "za.indeed.com",
    "Portugal": "pt.indeed.com",
}
