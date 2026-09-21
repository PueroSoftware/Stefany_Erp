# Relación Pantallas - Tablas SQL

## 📱 MOBILE (React Native / Expo)

| Pantalla | Archivo SVG | Tablas SQL |
|----------|-------------:|------------|
| Login | login_mobile.svg | usuario |
| Dashboard | dashboard_mobile.svg | usuario, pedido, venta, producto_terminado, materia_prima |
| Proveedores | proveedores_mobile.svg | proveedor |
| Compras | compras_mobile.svg | compra, detalle_compra, proveedor, materia_prima |
| Inventario | inventario_mobile.svg | materia_prima, stock_materia_prima, movimiento_stock |
| Producto Terminado | producto_terminado_mobile.svg | producto_terminado, formula_producto |
| Formula | formula_mobile.svg | formula_producto, materia_prima, producto_terminado |
| Ordenes de Producción | ordenes_mobile.svg | orden_produccion, detalle_produccion, producto_terminado |
| **Formulario Producto** | **formproducto_mobile.svg** | producto_terminado, formula_producto |
| **Detalle Pedido** | **detallepedido_mobile.svg** | pedido, carrito, detalle_venta, usuario |
| **Checkout** | **checkout_mobile.svg** | pedido, carrito, producto_terminado |

---

## 💻 WEB (Expo Web)

| Pantalla | Archivo SVG | Tablas SQL |
|----------|-------------|------------|
| Login | login.svg, Pos-wireframe-Login.svg | usuario |
| Dashboard | dashboard.svg | usuario, pedido, venta, producto_terminado, materia_prima |
| Productos | Pos-wireframe-Productos.svg | producto_terminado |
| Formulario Producto | Pos-wireframe-FormProducto.svg | producto_terminado, formula_producto, materia_prima |
| Usuarios | Pos-wireframe-Usuarios.svg | usuario |
| Formulario Usuario | Pos-wireframe-FormUsuario.svg | usuario |
| Detalle Pedido | Pos-wireframe-DetallePedido.svg | pedido, carrito, detalle_venta, usuario |
| Checkout | Pos-wireframe-Checkout.svg | pedido, carrito, producto_terminado |
| Historial | Pos-wireframe-Historial.svg | pedido, venta, detalle_venta |
| Envíos | Pos-wireframe-Envios.svg | envio, pedido |
| Recibo | Pos-wireframe-Recibo.svg | pedido, venta, detalle_venta, envio |
| Presentación | Pos-wireframe-Opcion2-Presentacion.svg | - (landing) |

---

## 🗃️ Resumen por Módulo SQL

| Módulo | Tablas | Pantallas |
|--------|--------|-----------|
| **Auth** | usuario | Login (mobile/web), Formulario Usuario |
| **Compras** | proveedor, compra, detalle_compra, materia_prima | Proveedores, Compras |
| **Inventario** | materia_prima, stock_materia_prima, movimiento_stock | Inventario |
| **Producción** | producto_terminado, formula_producto, orden_produccion, detalle_produccion | Producto Terminado, Formula, Ordenes |
| **Ventas** | usuario, pedido, carrito, venta, detalle_venta, pago, envio | Dashboard, Detalle Pedido, Checkout, Historial, Envíos, Recibo |

---

## 🔄 Flujo de Datos

```
Materia Prima → Compra → Stock → Formula → Producción → Producto Terminado → Venta → Pedido → Envío
```
