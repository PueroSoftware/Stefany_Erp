# ENVIRONMENT SETUP (Windows) for Tienda Jabones - Backend + Frontend (Repos Separados)

Este documento describe un flujo recomendado para preparar un entorno de desarrollo en Windows para trabajar con los repos separados de backend y frontend del proyecto Tienda Jabones.

Objetivo
- Establecer pasos reproducibles para instalar Node, PNPM, y herramientas básicas; crear skeletons y ejecutar el proyecto en desarrollo.

Requisitos previos
- Windows 10/11
- Conexión a Internet
- Permisos de administrador para instalaciones

1) Instalación de Node.js y PNPM
- Recomendación: usar Node LTS (v18.x o v20.x) para compatibilidad con TS y herramientas.
- Opción 1: Instalador oficial de Node.js desde nodejs.org (incluye npm). Luego instalar PNPM.
- Opción 2: usar nvm-windows para administrar versiones de Node y luego instalar PNPM.
- Comandos (PowerShell):
  - npm i -g pnpm
  - pnpm -v (verifica)

2) Configuración básica de PNPM
- Asegúrate de que PNPM gestione el caché de forma adecuada y que las rutas no estén bloqueadas por políticas de seguridad.

3) Configuración de ESLint/Prettier (opcional, para desarrollo)
- Dependencias en backend/frontend se añadirán cuando se empiecen a usar.
- Instalar globalmente si se desea: no recomendado, usar los bins locales de cada repo.

4) Expo CLI (opcional, si decides usar RN Web y Expo)
- Instalar global: `npm i -g expo-cli`
- Verificar instalación: `expo --version`

5) Setup de repos y dependencias (repos separados)
- Clona o accede a los directorios:
  - Backend: `tienda-jabones-backend/`
  - Frontend: `tienda-jabones-frontend/`

- Backend (tienda-jabones-backend)
  - Ejecutar: `cd tienda-jabones-backend`.
  - Instalar dependencias: `pnpm install` (si hay package.json con dependencias).
  - Construcción: `pnpm run build` (si hay script de build).
  - Desarrollo: `pnpm run dev` o `npm run dev` según los scripts definidos.
  - Compilar: `pnpm run build` para generar dist/.

- Frontend (tienda-jabones-frontend)
  - Ejecutar: `cd tienda-jabones-frontend`.
  - Instalar dependencias: `pnpm install` (si hay package.json).
  - Desarrollo: `pnpm run start` o el script definido. Si no hay scripts, usar placeholder para empezar.
  - Construcción: `pnpm run build` (si existe script).

6) Configurar tsconfig (si no está ya)
- Asegúrate de existir `tsconfig.json` en cada repos y ajusta `include`/`paths` si usas alias.

7) Variables de entorno
- Mantén las claves y secretos fuera del repositorio. Usa archivos `.env` listos para desarrollo y variables de entorno en el CI para producción.

8) Verificación rápida de salud
- Backend: arranca y verifica consola para confirmar que el servidor escuchando y no hay errores.
- Frontend: inicia el proyecto y verifica que la app carga (en RN Web o en un simulador).

9) Recomendaciones finales
- Documenta cualquier cambio en PLAN-UNIFICACION.md para historial.
- Mantén actualizados los README de cada repositorio con instrucciones de desarrollo y despliegue.

Notas
- Este documento propone un enfoque claro para Windows; si prefieres otro flujo (p. ej. WSL para Linux/Unix) puedo ajustarlo.
