import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from "react-native";
import { listarMateriasPrimas, listarStock, MateriaPrima, StockMateriaPrima } from "../servicio/fabril";
import { colores } from "../tema/colores";

export function InventarioScreen() {
  const [materias, setMaterias] = useState<MateriaPrima[]>([]);
  const [stock, setStock] = useState<StockMateriaPrima[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    Promise.all([listarMateriasPrimas(), listarStock()])
      .then(([m, s]) => { setMaterias(m); setStock(s); })
      .catch(() => {})
      .finally(() => setCargando(false));
  }, []);

  if (cargando) return <ActivityIndicator size="large" style={styles.centrado} color={colores.verde.sabio} />;

  return (
    <FlatList
      style={{ backgroundColor: colores.fondo.crema }}
      contentContainerStyle={styles.lista}
      data={materias}
      keyExtractor={(m) => String(m.id)}
      ListHeaderComponent={<Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Inventario</Text>}
      ListEmptyComponent={<Text style={styles.vacio}>No hay materias primas registradas</Text>}
      renderItem={({ item }) => {
        const lotes = stock.filter((s) => s.estado === "disponible").length;
        return (
          <View style={styles.fila}>
            <View style={{ flex: 1 }}>
              <Text style={styles.nombre}>{item.nombre}</Text>
              <Text style={styles.detalle}>Unidad: {item.unidad_medida} | Min: {item.stock_minimo} / Max: {item.stock_maximo}</Text>
            </View>
            <View style={[styles.badge, { backgroundColor: item.activo ? colores.verde.menta : "#FDECEA" }]}>
              <Text style={[styles.badgeTexto, { color: item.activo ? colores.verde.sabio : "#C62828" }]}>{item.activo ? "Activo" : "Inactivo"}</Text>
            </View>
          </View>
        );
      }}
    />
  );
}

const styles = StyleSheet.create({
  lista: { padding: 16 }, centrado: { flex: 1, justifyContent: "center" },
  titulo: { fontSize: 22, fontWeight: "700", marginBottom: 16 },
  fila: { flexDirection: "row", alignItems: "center", backgroundColor: colores.fondo.blanco, padding: 12, borderRadius: 10, marginBottom: 8, borderWidth: 1, borderColor: colores.borde },
  nombre: { fontSize: 15, fontWeight: "600", color: colores.texto.oscuro },
  detalle: { fontSize: 12, color: colores.texto.atenuado, marginTop: 2 },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  badgeTexto: { fontSize: 11, fontWeight: "700" },
  vacio: { textAlign: "center", color: colores.texto.atenuado, marginTop: 40 },
});
