// src/servicio/fabril.ts
// =====================================================================
// SERVICIO FABRIL — endpoints de los módulos internos (inventario,
// compras, producción, ventas, usuarios). Todos requieren token JWT y
// en backend están protegidos con IsFabril/IsAuthenticated.
//
// DRF pagina las listas: { count, next, previous, results }
// Aquí siempre devolvemos el array `results` para simplificar las pantallas.
// =====================================================================

import { api } from "./api";

// ---- Tipos exportados (campos reales de cada modelo Django) ------------

export interface MateriaPrima {
  id: number;
  nombre: string;
  unidad_medida: string;
  stock_minimo: string;
  stock_maximo: string;
  precio_promedio: string;
  activo: boolean;
}

export interface StockMateriaPrima {
  id: number;
  lote: string;
  cantidad_disponible: string;
  cantidad_reservada: string;
  fecha_vencimiento: string;
  estado: string;
  ubicacion: string;
}

export interface Compra {
  id: number;
  numero_factura: string;
  fecha_compra: string;
  subtotal: string;
  iva: string;
  total: string;
  estado: string;
}

export interface Proveedor {
  id: number;
  nombre: string;
  ruc_ci: string;
  contacto: string;
  telefono: string;
}

export interface ProductoTerminado {
  id: number;
  codigo_producto: string;
  nombre: string;
  stock_disponible: number;
  precio_venta: string;
  activo: boolean;
}

export interface OrdenProduccion {
  id: number;
  numero_orden: string;
  cantidad_producir: string;
  fecha_inicio: string;
  estado: string;
}

export interface Venta {
  id_venta: number;
  fecha_venta: string;
  total_venta: string;
  tipo_venta: string;
  estado: string;
  vendedor: string;
}

export interface Pedido {
  id_pedido: number;
  fecha_pedido: string;
  estado: string;
  total: string;
}

// Tipo genérico de respuesta paginada de DRF
interface RespuestaPaginada<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// extraerResultados: DRF SIEMPRE devuelve { results: [...] } con
// PageNumberPagination, pero por si algún endpoint devuelve array
// directo (sin paginación), lo manejamos defensivamente.
function extraerResultados<T>(data: RespuestaPaginada<T> | T[]): T[] {
  return Array.isArray(data) ? data : (data?.results ?? []);
}

// ---- INVENTARIO ----------------------------------------------------------

export async function listarMateriasPrimas(): Promise<MateriaPrima[]> {
  const { data } = await api.get("/inventario/materias-primas/");
  return extraerResultados(data);
}

export async function listarStock(): Promise<StockMateriaPrima[]> {
  const { data } = await api.get("/inventario/stock-materias-primas/");
  return extraerResultados(data);
}

// ---- COMPRAS -------------------------------------------------------------

export async function listarCompras(): Promise<Compra[]> {
  const { data } = await api.get("/compras/compras/");
  return extraerResultados(data);
}

export async function listarProveedores(): Promise<Proveedor[]> {
  const { data } = await api.get("/compras/proveedores/");
  return extraerResultados(data);
}

// ---- PRODUCCIÓN ----------------------------------------------------------

export async function listarProductosTerminados(): Promise<ProductoTerminado[]> {
  const { data } = await api.get("/produccion/productos-terminados/");
  return extraerResultados(data);
}

export async function listarOrdenesProduccion(): Promise<OrdenProduccion[]> {
  const { data } = await api.get("/produccion/ordenes-produccion/");
  return extraerResultados(data);
}

// ---- VENTAS --------------------------------------------------------------

export async function listarVentas(): Promise<Venta[]> {
  const { data } = await api.get("/ventas/ventas/");
  return extraerResultados(data);
}

export async function listarPedidos(): Promise<Pedido[]> {
  const { data } = await api.get("/ventas/pedidos/");
  return extraerResultados(data);
}

// ---- USUARIOS (solo fabril) ----------------------------------------------

export async function listarUsuarios() {
  const { data } = await api.get("/usuarios/");
  return extraerResultados(data);
}
