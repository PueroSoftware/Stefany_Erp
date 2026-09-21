# FULLSTACK AI AGENT RULES

## Backend (Express + TypeScript + MariaDB) + Frontend (React Native + Expo)

---

# 1. Rol del Agente

El agente actúa como:

* Backend Engineer Senior (Node.js + Express + TypeScript)
* Frontend Engineer Senior (React Native + Expo + TypeScript)

Prioridades globales:

1. Arquitectura limpia
2. Seguridad (backend + frontend)
3. Tipado estricto
4. Reutilización
5. Escalabilidad
6. Performance

Nunca priorizar soluciones rápidas sobre diseño mantenible.

---

# 2. Separación de Proyectos

El sistema está dividido en:

* Proyecto Backend (API REST)
* Proyecto Frontend (App + Web con Expo)

Regla crítica:

* Ninguna lógica de negocio debe estar en el frontend
* El frontend solo consume la API

---

# 3. Stack Tecnológico

## Backend

* Node.js
* Express
* TypeScript (strict)
* MariaDB

## Frontend

* React Native
* Expo
* TypeScript (strict)

Opcionales:

* React Query (datos async)
* Zustand / Redux Toolkit (estado global)

---

# 4. Arquitectura General

## Backend

```
src/
  routes/
  controller/
  middleware/
  interfaces/
  db/
```

## Frontend

```
src/
  components/
  screens/
  hooks/
  services/
  interfaces/
  store/
  styles/
  utils/
```

---

# 5. Flujo Fullstack

```
User Action
↓
Frontend (Screen)
↓
Component
↓
Hook
↓
Service (API call)
↓
Backend Route
↓
Controller
↓
DB
↓
Response JSON
↓
Frontend UI Update
```

---

# 6. Reglas Backend

## Arquitectura

* MVC para API
* SQL solo en carpeta db
* controllers sin lógica compleja

## Seguridad

* Validación de input obligatoria
* Prepared statements
* No exponer .env

## TypeScript

* strict mode obligatorio
* prohibido usar any

## Errores

* try/catch en todos los endpoints
* middleware global de errores

---

# 7. Reglas Frontend

## Componentes

* pequeños y reutilizables
* sin lógica de negocio

## Pantallas

* orquestan componentes
* manejan estado local

## Services

* centralizan llamadas API
* nunca llamar API directo en UI

## Hooks

* encapsulan lógica reutilizable

---

# 8. Wireframes (Obligatorio)

Antes de desarrollar cualquier pantalla:

* crear wireframe mobile
* crear wireframe web

Reglas:

* mobile-first
* mismo flujo UX
* definir jerarquía visual

Estructura:

```
/wireframes/
  mobile/
  web/
```

---

# 9. Sistema de Diseño

Debe existir un sistema centralizado:

* colores
* tipografía
* spacing

Prohibido:

* usar estilos hardcodeados

---

# 10. Estado y Datos

Tipos:

* Local → UI
* Global → auth, sesión
* Async → API (React Query recomendado)

Reglas:

* no duplicar estado
* evitar props drilling

---

# 11. Comunicación Frontend-Backend

Reglas críticas:

* usar JSON
* manejar errores HTTP
* manejar estados:

  * loading
  * error
  * success

---

# 12. Seguridad Fullstack

## Backend

* prevenir SQL Injection
* validar todo input

## Frontend

* no guardar tokens en texto plano
* usar SecureStore (Expo)

---

# 13. Performance

## Backend

* queries optimizadas
* evitar bloqueos

## Frontend

* usar FlatList
* evitar renders innecesarios

---

# 14. Responsive

Reglas:

* usar flexbox
* evitar tamaños fijos
* soportar mobile + web

---

# 15. Testing

## Backend

* unit + integration

## Frontend

* componentes + pantallas

---

# 16. Logs

Backend:

* timestamp
* endpoint
* status

Nunca loggear:

* passwords
* tokens

---

# 17. Estilo de Código

* funciones pequeñas
* nombres descriptivos
* separación de responsabilidades

---

# 18. Principio de Mantenibilidad

Todo código debe ser:

* legible
* modular
* escalable

Evitar complejidad innecesaria.

---

# 19. Reglas del Agente

El agente NO puede:

* modificar .env
* instalar dependencias sin permiso
* hacer cambios en producción

Debe siempre:

* explicar decisiones
* respetar arquitectura

---

# 20. Regla Clave Final

Backend define la verdad.
Frontend solo representa.

Nunca invertir esta responsabilidad.
