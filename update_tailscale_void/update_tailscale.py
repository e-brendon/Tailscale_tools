#!/usr/bin/env python3

import subprocess
import os
import datetime

# Caminho do log
LOG_DIR = "/var/log/update_tailscale"
LOG_FILE = os.path.join(LOG_DIR, "log.log")
LOG_RETENTION_DAYS = 30  # Tempo máximo dos logs (1 mês)

# Certifica-se de que o diretório de logs existe
os.makedirs(LOG_DIR, exist_ok=True)

def log_message(message):
    """Registra mensagens no log e mantém apenas os últimos 30 dias."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Adiciona a nova entrada ao log
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {message}\n")

    # Limpa logs antigos mantendo apenas os últimos 30 dias
    cleanup_old_logs()

def cleanup_old_logs():
    """Remove entradas do log mais antigas que 30 dias."""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log:
                lines = log.readlines()

            # Filtra apenas as linhas dentro do período desejado
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=LOG_RETENTION_DAYS)
            new_lines = [line for line in lines if is_recent_log(line, cutoff_date)]

            # Reescreve o log apenas com as entradas recentes
            with open(LOG_FILE, "w") as log:
                log.writelines(new_lines)
    except Exception as e:
        print(f"Erro ao limpar logs antigos: {e}")

def is_recent_log(line, cutoff_date):
    """Verifica se uma linha do log está dentro do período de retenção."""
    try:
        log_timestamp = line.split("]")[0][1:]  # Extrai a data/hora do log
        log_date = datetime.datetime.strptime(log_timestamp, "%Y-%m-%d %H:%M:%S")
        return log_date >= cutoff_date
    except:
        return True  # Se não puder interpretar a linha, mantém

def run_command(command):
    """Executa um comando e retorna a saída."""
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            log_message(f"SUCESSO: {command}")
            return result.stdout.strip()
        else:
            log_message(f"ERRO ({result.returncode}): {command}\n{result.stderr}")
            return None
    except Exception as e:
        log_message(f"EXCEÇÃO: {command}\n{str(e)}")
        return None

def main():
    log_message("Iniciando atualização do Tailscale...")

    # Atualiza o Tailscale automaticamente aceitando 'y'
    run_command("yes | tailscale update")

    # Reinicia o serviço
    run_command("vsv restart tailscaled")

    log_message("Atualização concluída.")

if __name__ == "__main__":
    main()