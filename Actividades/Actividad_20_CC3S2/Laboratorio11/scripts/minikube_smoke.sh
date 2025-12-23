#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-user-service}"
PORT="${2:-8000}"
NS="${3:-default}"

ATTEMPTS=10
SLEEP=2

# Esperar a que el pod esté Running
for i in $(seq 1 $ATTEMPTS); do
  POD="$(kubectl -n "$NS" get pods -l app="$SERVICE" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || true)"
  STATUS="$(kubectl -n "$NS" get pod "$POD" -o jsonpath='{.status.phase}' 2>/dev/null || true)"
  if [[ "$STATUS" == "Running" ]]; then
    break
  fi
  echo "[i] Esperando pod $SERVICE ($i/$ATTEMPTS)..."
  sleep $SLEEP
  POD=""
done

if [[ -z "$POD" ]]; then
  echo "[!] No se encontró pod para $SERVICE en $NS"
  exit 1
fi

echo "[i] smoke: $SERVICE/$NS -> http://127.0.0.1:${PORT}"

# Port-forward en background
kubectl -n "$NS" port-forward "pod/${POD}" "${PORT}:${PORT}" >/tmp/pf_${SERVICE}.log 2>&1 &
PF_PID=$!
sleep 1

# Reintentos para /health
RC=1
for i in $(seq 1 $ATTEMPTS); do
  curl -fsS "http://127.0.0.1:${PORT}/health" && RC=0 && break
  echo "[i] Reintentando /health ($i/$ATTEMPTS)..."
  sleep $SLEEP
  RC=1
done

kill $PF_PID >/dev/null 2>&1 || true
wait $PF_PID 2>/dev/null || true

if [ $RC -eq 0 ]; then
  echo "[OK] SMOKE $SERVICE -> 200"
else
  echo "[!] SMOKE $SERVICE FALLÓ"
  exit 1
fi
