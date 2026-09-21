import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from "react-native";
import { listarOrdenesProduccion, listarProductosTerminados, OrdenProduccion, ProductoTerminado } from "../servicio/fabril";
import { colores } from "../tema/colores";

export function ProduccionScreen() {
  const [ordenes, setOrdenes] = useState<OrdenProduccion[]>([]);
  const [productos, setProductos] = useState<ProductoTerminado[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    Promise.all([listarOrdenesProduccion(), listarProductosTerminados()])
      .then(([o, p]) => { setOrdenes(o); setProductos(p); })
      .catch(() => {})
      .finally(() => setCargando(false));
  }, []);

  if (cargando) return <ActivityIndicator size="large" style={styles.centrado} color={colores.verde.sabio} />;

  return (
    <FlatList
      style={{ backgroundColor: colores.fondo.crema }}
      contentContainerStyle={styles.lista}
      data={ordenes}
      keyExtractor={(o) => String(o.id)}
      ListHeaderComponent={
        <>
          <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Produccion</Text>
          <Text style={styles.subtitulo}>Ordenes de produccion</Text>
        </>
      }
      ListEmptyComponent={<Text style={styles.vacio}>No hay ordenes registradas</Text>}
      renderItem={({ item }) => (
        <View style={styles.fila}>
          <View style={{ flex: 1 }}>
            <Text style={styles.nombre}>Orden #{item.numero_orden}</Text>
            <Text style={styles.detalle}>Inicio: {item.fecha_inicio} — Cantidad: {item.cantidad_producir}</Text>
          </View>
          <View style={styles.badge}><Text style={styles.badgeTexto}>{item.estado}</Text></View>
        </View>
      )}
      ListFooterComponent={
        <>
          <Text style={styles.seccion}>Productos terminados ({productos.length})</Text>
          {productos.map((p) => (
            <View key={p.id} style={styles.fila}>
              <View style={{ flex: 1 }}>
                <Text style={styles.nombre}>{p.nombre}</Text>
                <Text style={styles.detalle}>Codigo: {p.codigo_producto} — Stock: {p.stock_disponible}</Text>
              </View>
              <Text style={styles.total}>${Number(p.precio_venta).toFixed(2)}</Text>
            </View>
          ))}
        </>
      }
    />
  );
}

const styles = StyleSheet.create({
  lista: { padding: 16 }, centrado: { flex: 1, justifyContent: "center" },
  titulo: { fontSize: 22, fontWeight: "700" }, subtitulo: { fontSize: 13, color: colores.texto.atenuado, marginBottom: 16 },
  seccion: { fontSize: 16, fontWeight: "700", color: colores.texto.oscuro, marginTop: 24, marginBottom: 12 },
  fila: { flexDirection: "row", alignItems: "center", backgroundColor: colores.fondo.blanco, padding: 12, borderRadius: 10, marginBottom: 8, borderWidth: 1, borderColor: colores.borde },
  nombre: { fontSize: 15, fontWeight: "600", color: colores.texto.oscuro },
  detalle: { fontSize: 12, color: colores.texto.atenuado, marginTop: 2 },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12, backgroundColor: colores.verde.menta },
  badgeTexto: { fontSize: 11, fontWeight: "700", color: colores.verde.sabio },
  total: { fontSize: 15, fontWeight: "700", color: colores.verde.sabio },
  vacio: { textAlign: "center", color: colores.texto.atenuado, marginTop: 40 },
});
