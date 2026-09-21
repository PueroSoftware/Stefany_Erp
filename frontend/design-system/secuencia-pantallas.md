# Secuencia de Pantallas - tienda-Fabril

## Flujo de Usuario Principal
1. **Login** (autenticación)
2. **Dashboard** (panel de control principal)
3. **Acceso a módulos** desde Dashboard o navegación

## Pantallas Disponibles (Versión Desktop - xml-designer/)

| # | Pantalla | Archivo SVG | Descripción |
|---|----------|-------------|-------------|
| 1 | Login | `login.svg` | Formulario octogonal de inicio de sesión (para administradores) |
| 2 | Dashboard | `dashboard.svg` | Panel de control con KPIs y accesos rápidos a módulos |
| 3 | Proveedores | `proveedores_model3.svg` | CRUD de proveedores con tarjetas, FAB y panel lateral |
| 4 | Inventario | `inventario_model3.svg` | CRUD de materia prima + stock (similar a proveedores) |
| 5 | Producto Terminado | `producto_terminado_model3.svg` | CRUD de jabones/kits con dropdowns para enums |
| 6 | Fórmula | `formula_model3.svg` | Relaciones producto-insumo (recetas) |
| 7 | Órdenes de Producción | `ordenes_model3.svg` | Órdenes de producción (maestro-detalle) |
| 8 | Compras | `compras_model3.svg` | Compras a proveedores (maestro-detalle) |

## Pantallas Disponibles (Versión Mobile - xml-RN/)

| # | Pantalla | Archivo SVG | Adaptación Mobile |
|---|----------|-------------|-------------------|
| 1 | Login | `login_mobile.svg` | Formulario centrado, octogonal |
| 2 | Dashboard | `dashboard_mobile.svg` | Tarjetas KPI en columna, accesos rápidos en grid 2x |
| 3 | Proveedores | `proveedores_mobile.svg` | Tarjetas apiladas verticalmente, FAB flotante |
| 4 | Inventario | `inventario_mobile.svg` | Similar a proveedores mobile |
| 5 | Producto Terminado | `producto_terminado_mobile.svg` | Tarjetas con información compacta |
| 6 | Fórmula | `formula_mobile.svg` | Tarjetas de relaciones producto-insumo |
| 7 | Órdenes | `ordenes_mobile.svg` | Tarjetas de órdenes con estado |
| 8 | Compras | `compras_mobile.svg` | Tarjetas de compras con resumen |

## Elementos Comunes en Todas las Pantallas

### 1. **Header/Barra Superior**
- Color de fondo: `#1D1D1B` (primary)
- Logo "FABRIL": `#EADDCC` (accent)
- Menú de navegación: Proveedores, Categoría M., Insumos, Órdenes

### 2. **Footer**
- Color de fondo: `#465A56` (secondary)
- Texto: "Desarrollado por: José Puerro" en `#EADDCC` (accent)
- Placeholder para logo de la empresa

### 3. **Botones de Acción**
- **Guardar**: Fondo `#EADDCC` (accent), texto `#1D1D1B` (primary)
- **Limpiar**: Fondo transparente, borde `#EADDCC`, texto `#1D1D1B`
- **Nuevo**: FAB circular `#EADDCC` con ícono `+` en `#1D1D1B`

### 4. **Ventana de Confirmación (Modal)**
- Fondo semi-transparente: `#000000` con opacidad 0.4
- Tarjeta blanca: `#FFFFFF` con borde `#6E807F` (tertiary)
- Título: "Datos guardados correctamente" en `#1D1D1B`
- Botón OK: `#EADDCC` (accent)

### 5. **Cards/Tarjetas**
- Fondo: `#FFFFFF` (surface)
- Borde: `#E0E0E0` (border)
- Bordes redondeados: 8px
- Sombra: 0 2px 6px rgba(0,0,0,0.1)
- Padding: 12px

### 6. **Inputs y Búsquedas**
- Fondo: `#F3F4F6` (input background)
- Borde: `#E0E0E0` (border)
- Bordes redondeados: 6px
- Placeholder: `#7A7A7A` (text-muted)

### 7. **Tablas/Encabezados**
- Encabezados: Fondo `#F0F0F0` (table header)
- Filas: Fondo `#FFFFFF` con borde `#E0E0E0`
- Texto: `#465A56` (secondary) para encabezados, `#1D1D1B` (primary) para datos

### 8. **Chips/Estados**
- Activo: Fondo `#10B981` (success), texto blanco
- Inactivo: Fondo `#6B7280` (inactive), texto blanco
- Alerta: Fondo `#D32F2F` (warning), texto blanco
- Info: Fondo `#1976D2` (info), texto blanco

## Flujo de Navegación Sugerido

```
Login (octogonal)
    ↓
Dashboard (panel de control)
    ↓
Proveedores ←→ Inventario ←→ Producto Terminado
    ↓               ↓               ↓
  CRUD            CRUD            CRUD
    ↓               ↓               ↓
Fórmula       Órdenes Producción   Compras
    ↓               ↓               ↓
  CRUD            CRUD            CRUD
```

## Uso en Figma

1. **Importar colores**: Usa `colores.json` o `colores.css` como referencia
2. **Importar SVGs**: Cada archivo SVG puede importarse como componente
3. **Crear flujos**: Conecta las pantallas según la secuencia lógica
4. **Responsive**: Usa versiones mobile (xml-RN/) para diseño responsive

## Notas para Desarrollo

- Los enums deben ser **listas desplegables** (nunca texto libre)
- Todos los botones **Guardar** muestran modal de confirmación
- Los **FAB** (Floating Action Button) son para acciones principales (Nuevo)
- El **panel lateral** se usa para formularios de creación/edición
- Los **dropdowns** para enums usan el color `#6E807F` (tertiary) para el indicador `▼`