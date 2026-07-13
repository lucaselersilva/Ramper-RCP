#!/usr/bin/env python3
"""Extrai dados da API do Ramper Pipeline (lscrm) e salva em data/*.json."""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")
BASE_URL = "https://api.lscrm.com.br/v1"

PAGE_SIZE = 200
MAX_RETRIES = 3
RETRY_WAIT_SECONDS = 3

ENTITIES = {
    "opportunities": "opportunities.json",
    "tasks": "tasks.json",
    "organizations": "organizations.json",
    "persons": "persons.json",
    "users": "users.json",
    "stages": "stages.json",
    "pipes": "pipes.json",
}


def load_env(path):
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()
    return env


def fetch_page(endpoint, token, page, limit):
    params = {"page": page, "limit": limit}
    url = f"{BASE_URL}/{endpoint}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"access-token": token})

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            last_error = e
            print(f"  [aviso] tentativa {attempt}/{MAX_RETRIES} falhou para {endpoint} "
                  f"pagina {page}: {e}", file=sys.stderr)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_WAIT_SECONDS)
    raise RuntimeError(f"Falha ao buscar {endpoint} (pagina {page}) apos {MAX_RETRIES} tentativas: {last_error}")


def fetch_all(endpoint, token):
    items = []
    page = 1
    while True:
        data = fetch_page(endpoint, token, page, PAGE_SIZE)
        get_list = data.get("get_list", {})
        page_items = get_list.get("itens", [])
        pagination = get_list.get("pagination", {})
        items.extend(page_items)

        total = int(pagination.get("total", len(items)))
        print(f"  {endpoint}: pagina {page} -> {len(page_items)} itens "
              f"(acumulado {len(items)}/{total})")

        if len(page_items) < PAGE_SIZE or len(items) >= total:
            break
        page += 1
    return items


def write_dashboard_bundle(entities, sync_info):
    """Gera data/dashboard_data.js com os dados embutidos.

    O dashboard.html abre via file:// (sem servidor), e navegadores bloqueiam
    fetch()/XHR para JSON local por CORS. Um <script src="..."> comum nao sofre
    essa restricao, entao embutimos os dados num arquivo .js carregado como script.
    """
    bundle = {"last_sync": sync_info["last_sync"]}
    for entity in entities:
        path = os.path.join(DATA_DIR, ENTITIES[entity])
        with open(path, "r", encoding="utf-8") as f:
            bundle[entity] = json.load(f)

    js_path = os.path.join(DATA_DIR, "dashboard_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("// Gerado automaticamente por extract.py — nao editar a mao.\n")
        f.write("window.RAMPER_DATA = ")
        json.dump(bundle, f, ensure_ascii=False)
        f.write(";\n")
    print(f"  Bundle do dashboard salvo em data/dashboard_data.js")


def main():
    env = load_env(ENV_PATH)
    token = os.environ.get("RAMPER_API_TOKEN") or env.get("RAMPER_API_TOKEN")
    if not token:
        print("ERRO: RAMPER_API_TOKEN nao encontrado no .env nem nas variaveis de ambiente.",
              file=sys.stderr)
        sys.exit(1)

    os.makedirs(DATA_DIR, exist_ok=True)

    results = {}
    errors = {}

    for entity, filename in ENTITIES.items():
        print(f"Extraindo {entity}...")
        try:
            items = fetch_all(entity, token)
        except RuntimeError as e:
            print(f"  [ERRO] {e}", file=sys.stderr)
            errors[entity] = str(e)
            continue

        out_path = os.path.join(DATA_DIR, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        results[entity] = len(items)
        print(f"  OK: {len(items)} registros salvos em data/{filename}")

    sync_info = {
        "last_sync": datetime.now(timezone.utc).astimezone().isoformat(),
        "counts": results,
        "errors": errors,
        "success": len(errors) == 0,
    }
    with open(os.path.join(DATA_DIR, "last_sync.json"), "w", encoding="utf-8") as f:
        json.dump(sync_info, f, ensure_ascii=False, indent=2)

    write_dashboard_bundle(results.keys(), sync_info)

    print("\nResumo da extracao:")
    for entity, count in results.items():
        print(f"  {entity}: {count} registros")
    if errors:
        print("Entidades com erro:")
        for entity, msg in errors.items():
            print(f"  {entity}: {msg}")
        sys.exit(1)
    print("\nExtracao concluida com sucesso.")


if __name__ == "__main__":
    main()
