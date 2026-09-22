# MemoriaEngram — Proyecto ERP TiendaSoap

> **Fecha de actualización:** 2026-09-21
> **Sesión:** Sincronización completa con GitHub + GitLab

---

## 📊 Estado actual: COMPLETO A UN ~80%

| Área | Estado | Comentario |
|---|---|---|
| **Backend Django** | ✅ **Funcional** | 10/10 tests OK, `/api/usuarios/` registrado |
| **Frontend Expo** | ✅ **Compila y arranca** | `tsc` → 0 errores, SDK 57 activo |
| **Git** | ✅ **Sincronizado** | Mismo commit `228ddf4` en los 3 lugares |
| **CI/CD GitLab** | ✅ **Pipeline** | SAST + Secret Detection automático |

**Funcionando end-to-end:** Login → Catalogo → Perfil → Pantallas fabriles

---

## 🗄️ Estructura del proyecto (Monorepo)

```
Erp_Stefanny_Django/
├── backend/          # Django 6.0.8 + PostgreSQL
│   ├── config/       # settings.py (JWT, CORS, DRF)
│   ├── core/         # auth (JWT), usuarios (ObjectStorage R2)
│   ├── inventario/   # Materias primas, stock, mermas
│   ├── compras/      # Proveedores, facturas
│   ├── produccion/   # Ordenes, productos terminados
│   ├── ventas/       # Pedidos, ventas, pagos, envios
│   ├── media_webp/   # Imágenes locales (espejo R2)
│   ├── database/     # Erp_TiendaSoap.sql (dump si hay Postgres)
│   └── venv/         # ⚠️ Excluido del repo (recrear con pip install)
│
├── frontend/         # Expo SDK 57 + React 19 + TypeScript
│   ├── src/
│   │   ├── pantallas/     # 16 pantallas (10 cliente + 6 fabril)
│   │   ├── navegacion/    # ContextoNavegacion + AppRoutes + BarraTabs
│   │   ├── servicio/      # api.ts + auth.ts + fabril.ts
│   │   ├── contexto/      # ContextoAuth (usuario, isAuth, login/logout)
│   │   ├── tema/          # colores.ts, tipografia.ts (tokens de diseño)
│   │   ├── componentes/   # index.tsx (Header, Card, Button, Chips)
│   │   ├── models/        # usuario.ts (tipado)
│   │   └── hooks/         # useAuth.ts (re-export)
│   ├── assets/       # Iconos, hero, etc.
│   └── node_modules/ # ⚠️ Excluido del repo (recreate con npm install)
│
├── .gitignore        # Excluye: venv, node_modules, .env, __pycache__
└── README.md          # Descripción corta del proyecto
```

---

## 🔐 Credenciales y URLs

| Componente | Valor | NOTA |
|---|---|---|
| GitHub | `https://github.com/PueroSoftware/Stefany_Erp` | ⭐ Public — hay que pasar a Private en settings |
| GitLab | `https://gitlab.com/PueroSoftware/stefany_erp` | ⭐ Public — mismo |
| Django Admin | `admin@tiendasoap.com` (login por correo) | Cualquier usuario con rol fabril |
| Base de datos | PostgreSQL `TiendaSoap` (localhost) | Usa `config/settings_test.py` para tests |
| R2 (imágenes) | `pub-8892b0ff54a14d2e91c70f633f3d6d6a.r2.dev` | 162 imágenes ya subidas |
| Frontend web | `http://localhost:8081` | `EXPO_NO_TYPESCRIPT_SETUP=true npx expo start --web` |
| Backend API | `http://localhost:8000/api/` | `manage.py runserver 0.0.0.0:8000` |

⚠️ **El `.env` no está en git (por seguridad).** Repos son públicos → NUNCA subirlo.
Después de formatear, crear un `.env` con:
```
SECRET_KEY=...
DEBUG=True
DB_NAME=TiendaSoap
DB_USER=admin
DB_PASSWORD=admin123
DB_HOST=localhost
DB_PORT=5432
```

---

## ✅ Qué ya está hecho (Fases completadas)

### Backend (Django 6.0.8)
- [x] JWT Auth (login, register, refresh, /me)
- [x] Catálogo de imágenes pública (`/api/storage/imagenes/`, sin token)
- [x] 5 apps con ViewSets: inventario, compras, producción, ventas, usuarios
- [x] `/api/usuarios/` — registrado y con permisos IsFabril
- [x] 10/10 tests (`python manage.py test core.tests --settings=config.settings_test`)
- [x] `settings_test.py` con SQLite in-memory (sin dependencias a Postgres local)

### Frontend (Expo SDK 57)
- [x] Fase 1: API layer + Auth (AsyncStorage reemplaza SecureStore para web)
- [x] Fase 2: Navegación propia (ContextoNavegacion + AppRoutes) — sin React Navigation
- [x] Fase 3: Pantallas cliente (Login, Register, Catalogo, DetalleImagen, Carrito, Checkout, Confirmacion, Historial, Perfil)
- [x] Fase 4: 6 pantallas fabriles (Dashboard, Inventario, Compras, Produccion, Ventas, Usuarios) + servicio `fabril.ts`
- [x] `BarraTabs.tsx` con iconos Ionicons
- [x] `tsc --noEmit` → 0 errores

### Git
- [x] Repositorio monorepo inicializado en raíz del proyecto
- [x] Remotes: `origin` (GitHub) + `gitlab` (GitLab)
- [x] Push completo a ambos (commit `228ddf4`)
- [x] `.gitignore` correcto (venv, node_modules, .env excluidos)

---

## ❌ Qué FALTA (pendientes)

### Críticos (bugs de contrato API)
- [ ] **Login no devuelve `usuario`** — el frontend recibe `{access, refresh}` pero no el usuario. Fix: llamar `fetchMe()` después del login, o crear un serializer custom.
- [ ] **Register devuelve claves distintas** — backend manda `{token, message, usuario}`, frontend espera `{access, refresh, usuario}`.
- [ ] **Catalogo paginación** — DRF devuelve `{count, results:[]}`, el frontend espera un array directo. Fix: usar `data.results`.
- [ ] **BASE_URL** api.ts tiene `10.0.2.2` (emulador Android). Para web debe ser `localhost:8000` (o mejor: rutas dinámicas).

### Funcionalidad (aplicación)
- [ ] Carrito de compras real (actualmente estático vacío) → usar Zustand
- [ ] Checkout enviar pedido a `/api/ventas/pedidos/`
- [ ] Confirmacion mostrar número de pedido creado
- [ ] Historial listar pedidos del usuario (`/api/ventas/pedidos/?usuario=X`)
- [ ] Usar React Query para cachear API calls (fue instalado pero no se usa)

### Git / Infra
- [ ] **Pasarlos a Private en GitHub + GitLab** (Settings del repo web — no se pudo via API por permisos)
- [ ] Crear `.env.example` (plantilla sin valores reales)
- [ ] Configurar GitHub Persona Access Token en el `credential.helper` (HTTPS funciona pero quizás el token expiró)
- [ ] Pipeline CI de GitLab está en Security (SAST + Secret Detection), no testing (no corre los 10 tests Django por ahora)

### Optimización
- [ ] banner.svg pesa 6.5 MB — optimizar

---

## 🔄 Cómo reconstruir el proyecto (tras formatear)

```bash
# 1. Clonar
git clone https://github.com/PueroSoftware/Stefany_Erp.git
cd Stefany_Erp

# 2. Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Crear .env (ver sección Credenciales arriba)
python manage.py migrate --settings=config.settings_test  # SQLite local
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000

# 3. Frontend (otra terminal)
cd frontend
npm install --legacy-peer-deps
EXPO_NO_TYPESCRIPT_SETUP=true npx expo start --web
# Abrir: http://localhost:8081
```

---

## 🧠 Decisión de diseño clave — Navegación propia

**Se descartó React Navigation** a favor de `ContextoNavegacion` por:

| Motivo | Detalle |
|---|---|
| React Navigation rompe web | `SafeAreaProvider` usa `ref` inválido en DOM |
| React Navigation exige SDK exacto | New Architecture obligatoria = riesgo |
| Más simple | La app solo tiene «pantallas raíz» después del login |
| Menos dependencias | Menos puntos de falla |

Desventaja: no es estándar. Si en el futuro se abre a otro desarrollador, considerar migrar.

---

## 📌 Aprendizajes clave de esta sesión

1. **tsc puede dar 0 errores pero la app no renderiza** — el stub `() => null` de AppRoutes.tsx era el culpable. Tener shapes correctas no es suficiente.
2. **`--legacy-peer-deps` instala versiones peligrosas** (`expo-secure-store@57` en vez de `~14.0.1`) — siempre verificar la versión y el peer.
3. **`EXPO_NO_TYPESCRIPT_SETUP=true`** — sin esto, Metro reescribe `tsconfig.json` rompiendo la compilación.
4. **`git pull --allow-unrelated-histories`** — unificó historias divergentes de GitHub/GitLab sin perder el CI que Gitlab puso.
