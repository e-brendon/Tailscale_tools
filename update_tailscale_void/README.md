# Para executar automático, insira isso em seu crontab 

```bash
0 0 * * * /usr/local/bin/update_tailscale.py
```
Assim ele executa todos os dias as 00:00h
## Copie o arquivo update_tailscale.py para /usr/local/bin

```bash
cp update_tailscale.py /usr/local/bin/
```
Outra forma seria já fazer o download direto para o diretório correto
```bash
curl -L -o /usr/local/bin/update_tailscale.py https://raw.githubusercontent.com/e-brendon/Tailscale_tools/refs/heads/main/update_tailscale_void/update_tailscale.py
```

