# Respaldo de memorias mem0 — Proyecto Erp_Stefanny

> **Exportado:** 2026-09-21
> **Total observaciones:** 10 activas
> **Servidor:** mem0.ai (nube — NO se pierde al formatear)

---

## 🧠 Memorias activas en mem0.ai

### Identidad del proyecto

```
Proyecto: Erp_Stefanny_Django
Tipo: ERP Tienda Jabones
Backend: Django 6.0.8 (Python 3.13.15)
Frontend: Expo SDK 57.0.24 + React 19.3.0 + TypeScript 5.3.3
```

---

### Estado actual del proyecto

**Backend** — `/home/pucusoft/ProyectosPersonales 2026/StackWeb/Erp_Stefanny_Django/backend`
- Apps Django: core, inventario, compras, produccion, ventas
- Auth: JWT simplejwt (login, register, me, refresh)
- Usuario model: id_usuario como PK, correo como USERNAME_FIELD
- ObjectStorage público R2 (catálogo 162 imágenes)
- `config/settings_test.py` con SQLite para tests
- **Tests: 10/10 pasando**
- Endpoint `/api/usuarios/` registrado (UsuarioViewSet + IsFabril)

**Frontend** — `/home/pucusoft/ProyectosPersonales 2026/StackWeb/Erp_Stefanny_Django/frontend`
- Expo SDK 57.0.24, React Native 0.81.6, TypeScript 5.3.3
- **tsc --noEmit: 0 errores**
- Navegación: ContextoNavegacion propio (Opción B, sin React Navigation)
- Api layer: axios + AsyncStorage (SDK 57)
- ContextoAuth: useAuth, useIsFabril, useIsAuthenticated
- 16 pantallas (10 cliente + 6 fabril) — todas con exports de tipo función
- Componentes: Header, Card, ButtonPrimary, Input, Chips

---

### Fase 1 — API/Auth (completada)

- `src/servicio/api.ts`: axios + interceptores JWT + AsyncStorage
- `src/servicio/auth.ts`: login, register, refresh, fetchMe, logout
- `src/contexto/ContextoAuth.tsx`: AuthState, useAuth, useIsFabril, useIsAuthenticated
- `src/hooks/useAuth.ts`: re-export
- `src/models/usuario.ts`: Usuario interface

### Fase 2-π — Navegación (completada)

- BarraTabs.tsx con Ionicons (cliente: catalogo/carrito/historial/perfil; fabril: dashboard/inventario/compras/produccion/ventas/usuarios/perfil)
- AppRoutes.tsx con mapas PANTALLAS_CLIENTE/PANTALLAS_FABRIL, cabecera con botón volver
- ContextoNavegacion.tsx con pila: navegar(), reemplazar(), volver()

### Fase 3 — Pantallas cliente (9 pantallas, todas exportadas como `XScreen`)

| Pantalla | Estado |
|---|---|
| Login | ✅ Funcional (formulario + login + navegación register) |
| Register | ✅ Funcional (formulario completo) |
| Catalogo | ✅ Funcional (fetch + filtros por grupo) |
| DetalleImagen | ✅ (usa useNavegacion.parametros) |
| Carrito | 💤 Estático (array vacío) |
| Checkout | 💤 Botón pago sin acción |
| Confirmacion | 💤 Placeholder vacío |
| Historial | 💤 Placeholder vacío |
| Perfil | ✅ Funcional (fetchMe + updateProfile) |

### Fase 4 — Pantallas fabriles (completadas)

- Dashboard, Inventario, Compras, Produccion, Ventas, Usuarios
- Servicio `src/servicio/fabril.ts` con 9 funciones listar* usando `extraerResultados`
- BarraTabs con Ionicons

---

### Git (completado y activo)

```
Local:    /home/pucusoft/ProyectosPersonales 2026/StackWeb/Erp_Stefanny_Django
Commit:   347b371 (ambos remotos, sincronizados)
GitHub:   https://github.com/PueroSoftware/Stefany_Erp
GitLab:   git@gitlab.com:PueroSoftware/stefany_erp.git (SSH)
Pipeline: .gitlab-ci.yml (SAST + Secret Detection automático)
```

.gitignore efectivo: venv/, node_modules/, .env, __pycache__/, *.pyc, media/, .zed/, *.env, ApuntesDocentes_Back.md, MemoriaEngram.md, datos_sql.md

---

## ⚠️ Problemas críticos pendientes (Fase 1-π)

1. **Login no devuelve `usuario`** → llamar `fetchMe()` después de login
2. **Register devuelve `{token, message, usuario}`** en vez de `{access, refresh, usuario}`
3. **Refresh devuelve solo `{access}`** (sin nuevo refresh token)
4. **Catalogo paginado** → usar `data.results` en lugar del array directo
5. **BASE_URL** en api.ts = `10.0.2.2:8000` (solo emulador Android) → para web usar `localhost:8000`

---

## 📋 Pendientes de funcionalidad

- Carrito: array estático vacío → reemplazar por Zustand
- Checkout: botón sin acción
- Confirmacion/Historial: placeholders vacíos
- Zustand + React Query: instalados pero NO usados
- Componentes compartidos (`index.tsx`): Header, Card, ButtonPrimary, Input, Chips — creados pero no usados en ninguna pantalla

---

## 🔐 Al formatear (rescatar SOLO esto)

1. **`backend/.env`** → exportarlo/copiarlo a un lugar seguro
   ```
   SECRET_KEY=...
   DB_NAME=TiendaSoap
   DB_USER=admin
   DB_PASSWORD=...
   DB_HOST=localhost
   DB_PORT=5432
   ```

2. **`backend/database/`** → `Erp_TiendaSoap.sql` (si tienes datos reales en PostgreSQL, hacer pg_dump)

3. **`backend/media_webp/`** (31.8 MB, 162 imágenes) → ya está en R2 (Cloudflare) — no es urgente pero el mirror local se pierde

4. **mem0** → exportado en este archivo (MemoriaEngram_backup.md en el repo)

5. **Código fuente** → ya en GitHub + GitLab

---

## 🔄 Reconstrucción completa tras formatear

```bash
# Backend
cd backend
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Crear .env con las credenciales (ver arriba)
python manage.py migrate --settings=config.settings_test
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000

# Frontend
cd frontend
npm install --legacy-peer-deps
EXPO_NO_TYPESCRIPT_SETUP=true npx expo start --web
# Abrir: http://localhost:8081
```

---

*Este documento fue generado extrayendo memorias de mem0.ai y persistiendo en el repositorio Git.*
