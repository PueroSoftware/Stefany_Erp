UX/UI Reference: Fabril (Mobile & Web) Wireframes

Este documento utiliza la carpeta wireframes como fuente de referencia para el diseño de UX/UI de las pantallas Fabril. Incluye las versiones móviles y web y propone cómo alinear la implementación actual con los wireframes disponibles.

Archivos de wireframes disponibles
- Mobile (React Native / Expo)
- Web (Expo Web)

- Lista de archivos relevantes (ejemplos):
  - wireframes/mobile/dashboard_mobile.svg
  - wireframes/mobile/ordenes_mobile.svg
  - wireframes/mobile/produccion_mobile.svg
  - wireframes/mobile/login_mobile.svg
  - wireframes/web/dashboard.svg
  - wireframes/web/Pos-wireframe-Productos.svg
  - wireframes/web/Pos-wireframe-DetallePedido.svg
  - wireframes/web/Pos-wireframe-Checkout.svg
  - wireframes/web/Pos-wireframe-Login.svg
  - wireframes/web/Pos-wireframe-Envios.svg
  - wireframes/web/Pos-wireframe-Usuarios.svg
  - wireframes/web/Pos-wireframe-Recibo.svg
  - wireframes/web/Pos-wireframe-Historial.svg
  - wireframes/web/index.svg

Notas sobre el mapeo Fabril (basado en PANTALLAS_SQL.md)
- Módulo Producción en la API backend se vincula con: Producto Terminado, Fórmula Producto, Ordenes Producción, Detalle Producción.
- En la UI Fabril se sugiere mostrar:
  - Panel de control (dashboard)
  - Inventario y Fórmulas (relacionados con productos terminados)
  - Órdenes de Producción y Detalles de Producción
  - Productos terminados y sus fórmulas asociadas
  - Proveedores y Reportes (para un flujo de fábrica completo)

Guía de implementación (sugerido, en fases)
- Fase 1: pantalla FabrilDashboard con cards de métricas básicas (mock) y navegación a submódulos; replicar el layout de dashboard.svg (web) y dashboard_mobile.svg (mobile).
- Fase 2: pantalla de Órdenes de Producción (FabrilProduction) integrada con ENUMs (estado, prioridad) y un Formulario de creación de órdenes que se alinee con FormProducto/Formula/DetalleProducción del backend.
- Fase 3: pantallas de Inventario, Productos Terminados y Fórmulas, correlacionando con las tablas SQL descritas en PANTALLAS_SQL.md.
- Fase 4: guía de estilo y componentes comunes (EnumChips, tarjetas, encabezados) para asegurar consistencia entre web y móvil.

Cómo usar este recurso en el equipo
- Revisa cada SVG para entender la estructura deseada y las posiciones clave de componentes (menus, headers, content blocks).
- En el desarrollo de nuevas pantallas, usa los wireframes como guía de layout, espaciados y jerarquía visual antes de empezar a codificar. Si el mock difiere, prioriza la usabilidad y la consistencia entre plataformas.
- Agrega un componente UI que permita alternar entre vista móvil y web cuando corresponda (responsive). 

Integración futura
- Podríamos crear una vista de “guía UX” dentro de la app que muestre estas imágenes en modo desarrollo para que el equipo pueda consultarlas en tiempo real mientras implementa.
