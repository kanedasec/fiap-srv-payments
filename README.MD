# FIAP Payment Service 

Microserviço responsável por gerenciar pagamentos no ecossistema da plataforma de revenda de veículos.

---

## 🚀 Tecnologias

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL**
- **Docker / Docker Compose**

---

## ⚙️ Como rodar

### Pré-requisitos
- Docker e Docker Compose instalados

### Passos
```bash
# Subir containers
sudo docker compose up -d --build

# Rodar migrations
sudo docker compose exec fiap-srv-payment alembic upgrade head
```

---

## 📡 Endpoints

### Health

- **GET** `/healthz`  
  Retorna o status básico da aplicação.

  **Response:**
  ```json
  {
    "status": "ok"
  }
  ```

- **GET** `/readyz`  
  Verifica a conexão com o banco de dados.

  **Response:**
  ```json
  {
    "status": "ok"
  }
  ```

---

### Payments

#### Criar pagamento
- **POST** `/payments`

  **Body:**
  ```json
  {
    "buyer_id": "uuid",
    "vehicle_id": "uuid",
    "amount": 50000.0
  }
  ```

  **Response:**
  ```json
  {
    "id": "uuid",
    "buyer_id": "uuid",
    "vehicle_id": "uuid",
    "amount": 50000.0,
    "status": "PENDING"
  }
  ```

---

#### Listar pagamentos
- **GET** `/payments`

  **Query params (opcional):**
  - `status`: `PENDING | APPROVED | REJECTED`

  **Response:**
  ```json
  [
    {
      "id": "uuid",
      "buyer_id": "uuid",
      "vehicle_id": "uuid",
      "amount": 50000.0,
      "status": "PENDING"
    }
  ]
  ```

---

#### Buscar pagamento por ID
- **GET** `/payments/{payment_id}`

  **Response:**
  ```json
  {
    "id": "uuid",
    "buyer_id": "uuid",
    "vehicle_id": "uuid",
    "amount": 50000.0,
    "status": "PENDING"
  }
  ```

---

#### Atualizar status do pagamento
- **PATCH** `/payments/{payment_id}`

  **Body:**
  ```json
  {
    "status": "APPROVED"
  }
  ```

  **Response:**
  ```json
  {
    "id": "uuid",
    "buyer_id": "uuid",
    "vehicle_id": "uuid",
    "amount": 50000.0,
    "status": "APPROVED"
  }
  ```

---

## 🗄️ Estrutura do projeto

```
fiap-srv-payment/
│── src/
│   ├── adapters/
│   │   ├── db/
│   │   └── http/
│   ├── application/
│   ├── domain/
│   └── ports/
│── migrations/
│── tests/
│── requirements.txt
│── docker-compose.yml
│── Dockerfile
│── README.md
```

---

## 🧪 Testes

O projeto inclui um script de testes automatizados via `curl`:

```bash
cd tests
chmod +x tests.sh
./tests.sh
```

---

## 📌 Notas

- O campo `status` de um pagamento só pode assumir os valores: `PENDING`, `APPROVED`, `REJECTED`.
- O valor de `amount` deve ser **maior que zero**.
- IDs de comprador (`buyer_id`) e veículo (`vehicle_id`) devem ser fornecidos como **UUIDs válidos**.
