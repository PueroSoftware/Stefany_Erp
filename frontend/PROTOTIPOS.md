# Prototipos — tienda-Fabril

## Descripción del Proyecto

Sistema de gestión para una fábrica artesanal de jabones y kits. El prototipo abarca desde la autenticación hasta las operaciones diarias de producción, cubriendo la cadena completa: proveedores → insumos → productos → fórmulas → compras → producción.

---

## Secuencia Lógica de Pantallas

### Flujo General

```
Login → Dashboard → [Módulos de Datos Maestros] → [Módulos de Operaciones]
```

### Detalle por Pantalla

| # | Pantalla | Tipo | Descripción |
|---|----------|------|-------------|
| 1 | Login | Autenticación | Formulario octogonal de inicio de sesión para administradores |
| 2 | Dashboard | Panel principal | KPIs, gráficos, accesos rápidos a todos los módulos |
| 3 | Proveedores | Dato maestro | CRUD de proveedores (quién vende insumos) |
| 4 | Inventario | Dato maestro | CRUD de materia prima y stock disponible |
| 5 | Producto Terminado | Dato maestro | CRUD de jabones, kits y promociones |
| 6 | Fórmulas | Dato maestro | Relaciones producto-insumo (recetas de fabricación) |
| 7 | Compras | Operación | Registro de compras a proveedores |
| 8 | Órdenes de Producción | Operación | Planificación y seguimiento de fabricación |

### Justificación del Orden

```
¿Por qué Proveedores antes que Inventario?
→ No puedes registrar insumos sin saber de dónde vienen.

¿Por qué Inventario antes que Fórmulas?
→ Necesitas tener los insumos definidos antes de crear recetas.

¿Por qué Productos antes que Fórmulas?
→ La fórmula conecta un producto con sus insumos, ambos deben existir.

¿Por qué Compras antes que Órdenes?
→ Necesitas tener stock de materia prima antes de producir.
```

### Dependencias entre Módulos

```
Proveedores ──────┐
                  ├──→ Compras ──→ Inventario (actualiza stock)
                  │
Inventario ───────┤
                  ├──→ Fórmulas
                  │
Productos ────────┘
                          │
                          ▼
                  Órdenes de Producción
                  (consume inventario,
                   genera productos)
```

---

## Metodología de Diseño

### 1. Definición del Sistema de Colores

Se estableció una paleta corporativa antes de diseñar cualquier pantalla:

| Token | Color | Uso |
|-------|-------|-----|
| primary | `#1D1D1B` | Header, texto principal |
| secondary | `#465A56` | Footer, paneles, acentos secundarios |
| tertiary | `#6E807F` | Bordes, indicadores, texto muted |
| accent | `#EADDCC` | Botones, FAB, logo, acentos destacados |
| background | `#F7F7F5` | Fondo general |
| surface | `#FFFFFF` | Tarjetas, paneles |
| success | `#10B981` | Estado activo, stock OK |
| warning | `#D32F2F` | Stock bajo, alertas |
| info | `#1976D2` | Órdenes en proceso |
| inactive | `#6B7280` | Estado inactivo |

**Archivos generados:**
- `design-system/colores.json` — Tokens en formato JSON
- `design-system/colores.css` — Variables CSS con clases de utilidad
- `design-system/preview-colores.html` — Vista previa interactiva

### 2. Definición de Tipografía

- Fuente principal: **Roboto** (con fallback a Arial)
- Tamaños: xs(11px), sm(12px), base(14px), lg(16px), xl(18px), 2xl(20px), 3xl(24px), 4xl(28px)
- Pesos utilizados: 300 (light), 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### 3. Mapeo de Enums

Se documentaron todos los enums del sistema para que los prototipos muestren los componentes UI correctos:

| Enum | Componente UI |
|------|---------------|
| Proveedor_estado | Toggle (Activo/Inactivo) |
| Categoria_materia_tipo | Chips (Base, Aroma, Color, Aditivo, Molde, Empaque) |
| Producto_terminado_aroma | Dropdown (24 opciones) |
| Producto_terminado_color | Dropdown (17 opciones) |
| Producto_terminado_peso | Dropdown (5 opciones) |
| Producto_terminado_tipo | Chips (Jabón, Kit, Promoción, Muestra) |
| Stock_materia_prima_estado | Badges coloridos |
| Compra_tipo_factura | Dropdown (Factura, Recibo, Nota de Venta, Boleta) |
| Orden_produccion_estado | Badges coloridos con colores semánticos |

**Archivo:** `ux/enums-ui-mapping.json`

### 4. Elementos Comunes (Shared Components)

Se definieron componentes reutilizables en todas las pantallas:

| Componente | Especificación |
|------------|----------------|
| Header | Fondo `#1D1D1B`, logo "FABRIL" en `#EADDCC`, navegación, avatar usuario |
| Footer | Fondo `#465A56`, texto "Jose Puero · pucusoft.pages.dev" en `#EADDCC` |
| Botón Primario | Fondo `#EADDCC`, texto `#1D1D1B`, border-radius 10px |
| Botón Secundario | Borde `#EADDCC`, fondo transparente, border-radius 10px |
| FAB | Círculo 28px radio, fondo `#EADDCC`, ícono `+` |
| Card | Fondo `#FFFFFF`, borde `#E0E0E0`, sombra, border-radius 8-12px |
| Input | Fondo `#F3F4F6`, borde `#E0E0E0`, focus `#6E807F`, border-radius 8px |
| Tabla Header | Fondo `#F0F0F0`, texto `#465A56`, font-weight 600 |
| Chip Estado | Colores semánticos (verde/rojo/azul/gris), border-radius 12px |
| Modal | Overlay negro 40% opacidad, card blanca con borde `#6E807F` |

### 5. Wireframes Iniciales (SVG)

Se crearon 16 archivos SVG como wireframes básicos:
- 8 versiones desktop en `xml-designer/` (1400×640px)
- 8 versiones mobile en `xml-RN/` (360×640px)

Los wireframes usaron la paleta correcta desde el inicio pero con estilo simplificado (Arial, formas básicas).

### 6. Conversión a Mockups Realistas

Los 16 SVGs fueron transformados de wireframes a mockups con apariencia de producto final:

**Cambios aplicados:**
- Fuente cambiada de Arial a **Roboto**
- Agregados **filtros SVG** (feDropShadow) para profundidad en cards
- Agregados **gradientes lineales** en headers
- Contenido reemplazado con **datos realistas**:
  - Empresas con RUC paraguayos
  - Nombres de personas reales
  - Precios en USD coherentes
  - Fechas de 2024
- Agregados **iconos/emojis** representativos por módulo
- Agregados **estados semánticos** (Activo, Inactivo, En Proceso, etc.)
- Agregada **paginación** en tablas
- Agregados **filtros y búsqueda** en barras superiores

---

## Versión Desktop (xml-designer/)

**Resolución:** 1400 × 640 píxeles

### Características por Pantalla

#### 1. Login (`login.svg`)
- Forma: **Octágono regular** (no rectangular)
- Imagen lateral izquierda (560px) con branding de fábrica
- Formulario centrado en octágono con campos de usuario/contraseña
- Checkbox "Recordar sesión"
- Botones Ingresar/Limpiar

#### 2. Dashboard (`dashboard.svg`)
- Header con navegación horizontal + avatar usuario
- 4 tarjetas KPI (Proveedores, Productos, Stock Bajo, Órdenes)
- Gráfico de barras de producción mensual
- Grid 2×3 de accesos rápidos a módulos

#### 3. Proveedores (`proveedores_model3.svg`)
- Barra de búsqueda + botones Filtrar/Exportar
- Tabla con 6 columnas: Nombre, RUC/CI, Contacto, Teléfono, Email, Estado
- Avatares con iniciales del proveedor
- Chips de estado (Activo/Inactivo/Suspendido)
- Paginación (1-21)
- FAB para nuevo proveedor

#### 4. Inventario (`inventario_model3.svg`)
- Barra de búsqueda + filtro por categoría
- Tabla con 7 columnas: Insumo, Unidad, Stock, Mín, Máx, Precio, Categoría
- **Fila destacada en rojo** para stock bajo mínimo
- Badges de categoría (Aroma, Base, Color, Aditivo, Empaque)
- Badges de estado (Disponible/Agotado)

#### 5. Producto Terminado (`producto_terminado_model3.svg`)
- Barra de búsqueda + filtros Tipo/Categoría
- Grid de tarjetas (4 columnas) con imagen placeholder
- Cada tarjeta: emoji, nombre, aroma, color, tipo, precio
- Badges de tipo (Nuevo, Kit)
- Badges de estado (Activo/Inactivo)

#### 6. Fórmulas (`formula_model3.svg`)
- Barra de búsqueda
- Tabla con 6 columnas: Producto, Insumo, Cantidad, Unidad, Orden, Observaciones
- Chips de observaciones (Agregar 5%, Base de jabón, Mezcla base)

#### 7. Órdenes de Producción (`ordenes_model3.svg`)
- Barra de búsqueda + filtros Estado/Prioridad
- Tabla con 6 columnas: Nº Orden, Producto, Cantidad, Fecha, Responsable, Estado
- Estados coloridos (En Proceso/Planificada/Completada/Pausada/Cancelada)
- Prioridades coloridas (Alta/Media/Baja)

#### 8. Compras (`compras_model3.svg`)
- Barra de búsqueda + filtros Proveedor/Tipo
- Tabla con 7 columnas: Nº Factura, Proveedor, Fecha, Tipo, Artículos, Total, Estado
- Badges de tipo (Factura/Recibo/Nota Venta/Boleta)
- Estados (Pendiente/Recibida/Cancelada)

---

## Versión Mobile (xml-RN/)

**Resolución:** 360 × 640 píxeles

### Adaptaciones de Desktop a Mobile

| Elemento | Desktop | Mobile |
|----------|---------|--------|
| Header height | 72px | 56px |
| Navegación | Horizontal inline | Solo título de pantalla actual |
| Tablas | Tabla completa con columnas | Tarjetas apiladas verticalmente |
| KPIs | 4 en fila horizontal | 4 en columna vertical |
| Accesos rápidos | Grid 2×3 | Grid 2×2 (más scrollable) |
| FAB posición | Esquina inferior derecha (grande) | Esquina inferior derecha (compacto) |
| Footer height | 40px | 56px (más espacio para touch) |
| Búsqueda | 340px + filtros inline | 260px + botón menú |
| Tarjetas datos | 300px ancho | 320px ancho (casi full-width) |
| Paginación | Visible | No visible (scroll infinito implícito) |

### Características Específicas Mobile

#### Login (`login_mobile.svg`)
- Octágono más pequeño (radio 150px vs 200px desktop)
- Imagen placeholder compacta arriba del octágono
- Campos de formulario más estrechos
- Botones apilados si es necesario

#### Dashboard (`dashboard_mobile.svg`)
- KPIs en columna (uno debajo del otro)
- Accesos rápidos en grid 2×2
- Sin gráfico de barras (se reemplaza por indicadores numéricos)

#### Módulos CRUD (Proveedores, Inventario, Productos, Fórmulas)
- Tarjetas apiladas verticalmente (scroll)
- Información más compacta por tarjeta
- Avatar + datos principales + badge estado
- FAB más pequeño (radio 24px)

#### Módulos Operación (Órdenes, Compras)
- Tarjetas con resumen de información
- Estados y prioridades como badges compactos
- Información crítica visible sin expandir

---

## Archivos del Proyecto

```
tienda-Fabril/
├── PROTOTIPOS.md                    ← Este documento
├── design-system/
│   ├── colores.json                 Tokens de color
│   ├── colores.css                  Variables CSS
│   ├── preview-colores.html         Vista previa interactiva
│   └── secuencia-pantallas.md       Documentación de flujo
├── ux/
│   ├── design-guidelines.md         Guías de diseño
│   └── enums-ui-mapping.json        Mapeo enums → UI
├── xml-designer/                    Prototipos Desktop (1400×640)
│   ├── login.svg
│   ├── dashboard.svg
│   ├── proveedores_model3.svg
│   ├── inventario_model3.svg
│   ├── producto_terminado_model3.svg
│   ├── formula_model3.svg
│   ├── ordenes_model3.svg
│   └── compras_model3.svg
└── xml-RN/                          Prototipos Mobile (360×640)
    ├── login_mobile.svg
    ├── dashboard_mobile.svg
    ├── proveedores_mobile.svg
    ├── inventario_mobile.svg
    ├── producto_terminado_mobile.svg
    ├── formula_mobile.svg
    ├── ordenes_mobile.svg
    └── compras_mobile.svg
```

---

## Herramientas Utilizadas

| Herramienta | Uso |
|-------------|-----|
| SVG | Formato de prototipos (vectorial, escalable, editable) |
| CSS Variables | Sistema de colores reusable |
| JSON | Tokens de diseño y mapeo de enums |
| Roboto | Tipografía principal |
| Filtros SVG | Sombras y efectos de profundidad |
| Gradientes SVG | Headers con efecto visual |
| Emojis | Iconografía representativa por módulo |

---

## Estado Actual

- ✅ Sistema de colores definido
- ✅ Guías de diseño documentadas
- ✅ Mapeo de enums completado
- ✅ 16 prototipos SVG (8 desktop + 8 mobile)
- ✅ Secuencia lógica de pantallas definida
- ✅ Dependencias entre módulos documentadas
- 🔲 Pendiente: agregar logo de Pucusoft a footers
- 🔲 Pendiente: implementación en código (React Native / Web)
- 🔲 Pendiente: backend y base de datos

---

*Documento generado para el proyecto tienda-Fabril*
*Desarrollado por: Jose Puero — pucusoft.pages.dev*
