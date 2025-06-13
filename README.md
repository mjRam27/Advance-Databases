
## 🚆 VBB Real-Time Transport Tracker

This project fetches **live public transport data** from the official **VBB API**, and uses **FastAPI**, **MongoDB**, **Redis**, **Neo4j**, and **Vue.js** to deliver a responsive frontend and analytics-ready backend.

### 🔧 Tech Stack

| Layer      | Technology                                                      |
| ---------- | --------------------------------------------------------------- |
| Frontend   | Vue.js                                                          |
| Backend    | FastAPI (Python)                                                |
| Databases  | MongoDB (Storage), Redis (Caching), Neo4j (Graph relationships) |
| API Source | [VBB Transport REST API](https://vbb.transport.rest)            |

---

## 🔍 Features

* 🚉 **Live Departures** from any station (with caching)
* 🔄 **Journey Search** with filters (bus/train/tram)
* 🛑 **Stopovers** display with route expansion
* 🔁 **User history logging**
* 🔗 **Graph Visualization** of routes (Neo4j)

---

## 🧪 How to Run (via Docker)

### 1. 🐳 Clone the Repository

```bash
git clone https://github.com/mjRam27/Advance-Databases.git
cd Advance-Databases
```

### 2. 🔐 Setup Environment

Create a `.env` file in `backend_vbb` with:

```env
MONGO_URI=mongodb://mongo:27017
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

> ⚠️ Make sure this matches your Docker Compose.

---

### 3. 🚀 Run with Docker Compose

```bash
docker-compose up --build
```

This will spin up:

* `fastapi-backend` (on port 8000)
* `frontend` (Vue app on port 5173)
* `redis` (caching)
* `mongo` (data storage)
* `neo4j_db` (graph store on port 7474)

---

## 🌐 App Access

* Frontend UI: [http://localhost:5173](http://localhost:5173)
* Backend API (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)
* Neo4j Browser: [http://localhost:7474](http://localhost:7474)

---

## 📦 Sample Endpoints

| Feature             | Endpoint                                                |
| ------------------- | ------------------------------------------------------- |
| Search Journey      | `/journey?from_station=X&to_station=Y&products[]=train` |
| View Departures     | `/departures?station_id=900000003201`                   |
| User History        | `/user-history?user_id=user123`                         |
| Route Visualization | `/route?start_station=X&end_station=Y`                  |

---

## ✍️ Contributors

| Name                 | Role                                               |
| -------------------- | ---------------------------------------------------|
| Manoj Padmanabha     | Real-time departures & journey search+ LiveBoard   |
| Mahesh Babu          | Station data                                       |
| Manikanta Goud       | User history logging                               |
| Yathish              | Route connections via Neo4j                        |

---
