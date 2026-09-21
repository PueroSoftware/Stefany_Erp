 - Tienda Jabones Frontend (Skeleton con Expo)
 - Este repositorio aloja el frontend de Tienda Jabones, basado en Expo (React Native) con TypeScript. Es una base inicial con estructura mínima (src/, tsconfig.json, package.json) y ejemplos de flujo de usuario.
 - El backend no se gestiona aquí a menos que se indique expresamente; este repositorio es principalmente frontend. Si hay componentes de backend, deben mantenerse en un repositorio separado.
 - Estructura inicial: `src/`, `tsconfig.json`, `package.json`.
 - Instrucciones iniciales: instalar dependencias y arrancar con los scripts de Expo cuando se definan (start, web, android, ios).
-
## Estructura y propósito
- Estructura inicial: `src/`, `tsconfig.json`, `package.json`.
- Este repositorio es la base para desarrollar el backend con Express + TypeScript.
- Cuando se vaya a trabajar en la implementación, se irán añadiendo dependencias (Express, routers, controladores, middlewares).

## Cómo empezar
- Requisitos: Node.js LTS (recomendado 18.x o 20.x) y PNPM.
- Pasos iniciales:
  1) cd tienda-jabones-backend
  2) pnpm install
  3) pnpm run dev (si se define) o pnpm run build; luego node dist/index.js

## Scripts
- start: expo start
- web: expo start --web
- android: expo run:android
- ios: expo run:ios
- lint: eslint .
- typecheck: tsc --noEmit

Notas: Este skeleton no incluye dependencias de Express por defecto; se agregaran cuando se empiece a implementar la API.
- Estructura inicial: `src/`, `tsconfig.json`, `package.json`.
- Instrucciones iniciales: instalar dependencias y arrancar con un script de desarrollo cuando se definan.
