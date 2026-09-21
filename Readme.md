# 🧼 ERP Tajmell Stefany / TiendaSoap

Sistema Integral ERP para Control de Producción Artesanal de Jabones y E-Commerce Full-Stack.

---

## 📋 Descripción General

**ERP Tajmell Stefany** es una solución integral diseñada para la gestión operativa y comercial de la fabricación de jabones artesanales. A diferencia de una tienda online tradicional, la plataforma conecta la administración industrial en planta con la venta directa al cliente final.

### Módulos Principales:
* **Gestión de Producción y Recetas (ERP/Fabril):** Control de materias primas (bases, aromas, colorantes), registro de fórmulas, seguimiento por fases de producción, lotes y cálculo automático de mermas.
* **Control de Inventario:** Movimientos de stock en tiempo real, trazabilidad de vencimientos y alertas de stock mínimo.
* **Comercio Electrónico (E-Commerce):** Catálogo dinámico con filtrado por aromas, tipos y pesos, gestión de carrito de compras, pedidos, clientes y pasarela de estado de pagos.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología | Versión | Descripción |
| :--- | :--- | :--- | :--- |
| **Backend** | Python / Django | 3.12.3 / 6.0.8 | ORM, lógica de negocio y panel de administración. |
| **API REST** | Django REST Framework | 3.17.1 | Exposición de endpoints JSON seguros para el frontend. |
| **Base de Datos** | PostgreSQL | — | BD relacional con tipos `ENUM`, funciones y triggers. |
| **Frontend** | Expo / React Native | ~52.0.0 / 0.76.6 | Interfaz de usuario móvil/web (PWA) con TypeScript. |
| **Estado Cliente** | React Query / Zustand | 5.x / 4.5.0 | Gestión de datos asíncronos y estado global. |
| **Cliente HTTP** | Axios | — | Consumo asíncrono de endpoints REST. |

---

## 📁 Estructura del Proyecto

```text
Erp_Stefanny_Django/
├── Readme.md                  # Documentación general del proyecto
├── backend/                   # Código fuente del Backend (Django)
│   ├── database/              # Script de la base de datos
│   │   └── Erp_TiendaSoap.sql # DDL completo: 24 tablas, 23 tipos ENUM,
│   │                          # funciones y triggers de PostgreSQL
│   ├── config/                # Configuración principal (settings, urls, asgi, wsgi)
│   ├── produccion/            # App Django (módulo de producción, en construcción)
│   ├── venv/                  # Entorno virtual de Python 3.12
│   ├── manage.py              # Script de administración de Django
│   └── requirements.txt       # Dependencias del backend
└── frontend/                  # Código fuente del Frontend (Expo / React Native)
    ├── App.tsx                # Entrada principal de la aplicación
    ├── presentation/          # Pantallas, componentes, navegación y tema
    │   └── screens/           # mockup.tsx (tienda pública), fabril/* (ERP)
    ├── src/                   # API, dominio, hooks y lógica de negocio
    │   └── api/               # index.ts (servicios REST) y hooks.ts
    ├── assets/                # Recursos estáticos
    ├── package.json           # Dependencias de Node.js
    └── tsconfig.json          # Configuración del compilador de TypeScript
```

---

## 🗄️ Base de Datos

* **Motor:** PostgreSQL (localhost, puerto `5432`).
* **Base de datos:** `TiendaSoap`.
* **Esquema:** definido en `backend/database/Erp_TiendaSoap.sql` — 24 tablas, 23 tipos `ENUM`, 1 función trigger (`set_fecha_actualizacion`) y 1 trigger (`trg_producto_actualizacion`).
* **Credenciales de desarrollo:** usuario `admin` (ver `datos_sql.md`; mover a variables de entorno en producción).
* **Pendiente de la BD:** wishlist, reseñas, cupones, promociones, notificaciones, procedimiento `registrar_compra` y triggers de automatización (fase ecommerce).

---

## 🔌 API REST (Frontend ↔ Backend)

Contrato de endpoints esperado por el frontend (`frontend/src/api/index.ts`):

* `POST /auth/login` y `POST /auth/register` → `{ token, usuario }` (JWT)
* CRUD por módulo: `/categorias`, `/proveedores`, `/materias-primas`, `/compras`, `/detalles-compra`, `/stock-materias-primas`, `/movimientos-stock`, `/productos-terminados`, `/formula-producto`, `/ordenes-produccion`, `/usuarios`, `/pedidos`, `/carritos`, `/ventas`, `/pagos`, `/envios`
* Proceso transaccional: `POST /sp/registrar-compra`

> **URL base actual del frontend:** `http://localhost:3000/api` (configurable con la variable `EXPO_PUBLIC_API_URL`). El backend Django se expone en `http://localhost:8000`.

---

## 🚀 Puesta en Marcha

### Backend (Django)
```bash
cd backend
python -m venv venv                # si no existe
source venv/bin/activate           # Linux/macOS
pip install -r requirements.txt
python manage.py runserver         # arranca en http://localhost:8000
```

### Frontend (Expo)
```bash
cd frontend
npm install
npm run start                      # Expo en http://localhost:19006
npm run web                        # variante web
```

---

## 📌 Estado del Proyecto

* **Backend (Django):** en construcción. Aplicación `produccion` creada; `core`, `inventario`, `compras` y `ventas` por crear; sin endpoints implementados aún.
* **Frontend (Expo):** funcional con datos *mock* para la tienda pública (`mockup.tsx`); las pantallas Fabril llaman a la API real. Se reorganizará una vez el backend esté terminado según la arquitectura.
* **SQL:** corregido y revisado (enums limpios, `prioridad` en `orden_produccion`, cascades protegidos). Pendiente aplicar a la BD.

---
