# Para executar automático, insira isso em seu crontab 

```bash
0 0 * * * /usr/local/bin/update_tailscale.py
```
Assim ele executa todos os dias as 00:00h
## Copie o arquivo update_tailscale.py para /usr/local/bin

```bash
cp update_tailscale.py /usr/local/bin/
```
