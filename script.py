import requests
from bs4 import BeautifulSoup

URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"
N8N_WEBHOOK = "https://sua_url_n8n/webhook-test/clientes" 

# 1) Baixar a página
html = requests.get(URL_PAGINA, timeout=30).text

# 2) Ler a tabela de clientes
soup = BeautifulSoup(html, "html.parser")
linhas = soup.select("#clientes tbody tr")
clientes = []
for linha in linhas:
    colunas = linha.find_all("td")
    cliente = {
        "nome": colunas[0].get_text(strip=True),
        "email": colunas[1].get_text(strip=True),
        "saldo": colunas[2].get_text(strip=True),
        "perfil": colunas[3].get_text(strip=True),
    }
    clientes.append(cliente)

print("Clientes encontrados:", len(clientes))
print("Exemplo 1º cliente:", clientes[0] if clientes else "nenhum")

# 3) Enviar pro n8n
payload = {"clientes": clientes}
resp = requests.post(
    N8N_WEBHOOK,
    json=payload,
    headers={"Content-Type": "application/json"},
    timeout=60
)
print("Status:", resp.status_code)
print("Headers:", dict(resp.headers))
print("Resposta (primeiros 1500 chars):")
print(resp.text[:1500])