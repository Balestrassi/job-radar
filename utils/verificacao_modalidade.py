
import time

from playwright.sync_api import sync_playwright

from core.job import Job, _modalidade_pelo_texto
from core.logger import get_logger

logger = get_logger()

TIMEOUT_PAGINA_MS = 25000

# Custo: só abre a página completa de vaga com modalidade_confirmada=False
# (filtro nativo do LinkedIn/Indeed, ver core/job.py) — nunca a lista bruta
# inteira. Roda DEPOIS de filtrar_vagas(), sobre o que já passou cargo +
# cidade + mercado, então o volume por ciclo é pequeno (dezenas, não
# milhares) — é o mesmo motivo pelo qual TERMOS_POR_CICLO existe: manter o
# custo por ciclo proporcional ao que realmente precisa de verificação, não
# ao tamanho da busca bruta.


def filtrar_por_modalidade_real(vagas: list[Job]) -> tuple[list[Job], int]:
    """Reconfere, abrindo a página completa da vaga, toda vaga cujo
    modalidade="Remoto" veio de um filtro NATIVO da fonte sem confirmação
    própria (ver Job.modalidade_confirmada). Devolve (vagas_mantidas,
    quantas_descartadas).

    MEDIDO ao vivo (2026-08-18): duas vagas reais retornadas pelo filtro
    remoto do LinkedIn (f_WT=2) eram presencial/híbrida de verdade, e
    nenhuma tinha contradição no título — só na descrição completa. Sem
    essa segunda checagem, o usuário recebia vaga presencial disfarçada de
    remota (ver conversa que motivou este módulo).

    Falha ao abrir a página (timeout, bloqueio) NÃO descarta a vaga — trata
    como "não deu pra confirmar, mantém como está" em vez de "não deu pra
    confirmar, descarta". A alternativa (descartar em qualquer erro de
    rede) perderia vaga boa por instabilidade de conexão, que é um problema
    mais comum e menos grave do que ocasionalmente deixar passar uma vaga
    presencial pra o usuário conferir manualmente pelo link.
    """
    candidatas = [v for v in vagas if not v.modalidade_confirmada]
    if not candidatas:
        return vagas, 0

    rejeitadas_ids: set[str] = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        )

        for vaga in candidatas:
            try:
                page.goto(vaga.link, timeout=TIMEOUT_PAGINA_MS)
                time.sleep(1)
                texto_pagina = page.inner_text("body")
            except Exception as e:
                logger.warning(
                    f"[Verificação modalidade] Falha ao abrir '{vaga.titulo}' "
                    f"({vaga.site}): {e} — mantém como Remoto sem confirmar."
                )
                continue

            modalidade_real = _modalidade_pelo_texto(texto_pagina)
            if modalidade_real:
                logger.info(
                    f"[Verificação modalidade] '{vaga.titulo}' ({vaga.site}) "
                    f"veio como Remoto do filtro nativo, mas a descrição indica "
                    f"{modalidade_real} — descartada."
                )
                rejeitadas_ids.add(vaga.id)

        browser.close()

    if not rejeitadas_ids:
        return vagas, 0

    return [v for v in vagas if v.id not in rejeitadas_ids], len(rejeitadas_ids)
