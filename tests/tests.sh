#!/bin/bash

echo "==== Testando fiap-srv-payments ===="

# Criar pagamento
PAYMENT_ID=$(curl -s -X POST http://localhost:8003/payments \
  -H "Content-Type: application/json" \
  -d '{
    "buyer_id": "11111111-1111-1111-1111-111111111112",
    "vehicle_id": "11111111-1111-1111-1111-111111111112",
    "amount": 50000,
    "method": "credit_card"
  }' | jq -r '.id')

echo "Pagamento criado com ID: $PAYMENT_ID"

# Listar pagamentos
echo "Lista de pagamentos:"
curl -s http://localhost:8003/payments | jq .

# Buscar pagamento por ID
echo "Buscar pagamento por ID:"
curl -s http://localhost:8003/payments/$PAYMENT_ID | jq .

# Atualizar pagamento (ex: marcar como confirmado)
echo "Atualizando pagamento..."
curl -s -X PATCH http://localhost:8003/payments/$PAYMENT_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "APPROVED"}' | jq .

# Cancelar pagamento
echo "Rejeitando pagamento..."
curl -s -X PATCH http://localhost:8003/payments/$PAYMENT_ID \
  -H "Content-Type: application/json" \
  -d '{"status": "REJECTED"}' | jq .
