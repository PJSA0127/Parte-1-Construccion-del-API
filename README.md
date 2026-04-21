# API Monitoreo SOS

## 📌 Descripción

API desarrollada con FastAPI para la gestión de eventos de monitoreo de alarmas.

Permite:

* Registrar eventos
* Consultar eventos
* Marcar eventos como resueltos

---

## ⚙️ Instalación

```bash
python -m pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
python -m uvicorn app.main:app --reload
```

---

## 🌐 Acceso

Abrir en el navegador:

http://127.0.0.1:8000/docs

---

## 📡 Endpoints

### 🔹 GET /eventos

Obtiene todos los eventos registrados

### 🔹 POST /eventos

Crea un nuevo evento

Ejemplo:

```json
{
  "cliente": "Empresa SOS",
  "tipo_evento": "Alarma activada",
  "descripcion": "Puerta abierta"
}
```

### 🔹 PUT /eventos/{evento_id}

Marca un evento como resuelto

---

## 📸 Evidencia

Aquí se muestran capturas del API funcionando localmente:

* Swagger funcionando
* Creación de eventos
* Consulta de eventos
* Actualización de eventos

(Aquí debes agregar tus capturas de pantalla)

---
