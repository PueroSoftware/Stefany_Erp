import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from "react-native";
import { listarCompras, Compra } from "../servicio/fabril";
import { colores } from "../tema/colores";

export function ComprasScreen() {
  const [compras, setCompras] = useState<Compra[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    listarCompras()
      .then(setCompras)
      .catch(() => {})
      .finally(() => setCargando(false));
  }, []);

  if (cargando) return <ActivityIndicator size="large" style={styles.centrado} color={colores.verde.sabio} />;

  return (
    <FlatList
      style={{ backgroundColor: colores.fondo.crema }}
      contentContainerStyle={styles.lista}
      data={compras}
      keyExtractor={(c) => String(c.id)}
      ListHeaderComponent={<Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Compras</Text>}
      ListEmptyComponent={<Text style={styles.vacio}>No hay compras registradas</Text>}
      renderItem={({ item }) => (
        <View style={styles.fila}>
          <View style={{ flex: 1 }}>
            <Text style={styles.nombre}>Factura #{item.numero_factura}</Text>
            <Text style={styles.detalle}>{item.fecha_compra} — Estado: {item.estado}</Text>
          </View>
          <Text style={styles.total}>${Number(item.total).toFixed(2)}</Text>
        </View>
      )}
    />
  );
}

const styles = StyleSheet.create({
  lista: { padding: 16 }, centrado: { flex: 1, justifyContent: "center" },
  titulo: { fontSize: 22, fontWeight: "700", marginBottom: 16 },
  fila: { flexDirection: "row", alignItems: "center", backgroundColor: colores.fondo.blanco, padding: 12, borderRadius: 10, marginBottom: 8, borderWidth: 1, borderColor: colores.borde },
  nombre: { fontSize: 15, fontWeight: "600", color: colores.texto.oscuro },
  detalle: { fontSize: 12, color: colores.texto.atenuado, marginTop: 2 },
  total: { fontSize: 15, fontWeight: "700", color: colores.verde.sabio },
  vacio: { textAlign: "center", color: colores.texto.atenuado, marginTop: 40 },
});
