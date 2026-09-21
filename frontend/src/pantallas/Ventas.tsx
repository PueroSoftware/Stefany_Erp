import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from "react-native";
import { listarVentas, Venta } from "../servicio/fabril";
import { colores } from "../tema/colores";

export function VentasScreen() {
  const [ventas, setVentas] = useState<Venta[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    listarVentas()
      .then(setVentas)
      .catch(() => {})
      .finally(() => setCargando(false));
  }, []);

  if (cargando) return <ActivityIndicator size="large" style={styles.centrado} color={colores.verde.sabio} />;

  const total = ventas.reduce((s, v) => s + Number(v.total_venta || 0), 0);

  return (
    <FlatList
      style={{ backgroundColor: colores.fondo.crema }}
      contentContainerStyle={styles.lista}
      data={ventas}
      keyExtractor={(v) => String(v.id_venta)}
      ListHeaderComponent={
        <>
          <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Ventas</Text>
          <Text style={styles.subtitulo}>{ventas.length} ventas — Total ${total.toFixed(2)}</Text>
        </>
      }
      ListEmptyComponent={<Text style={styles.vacio}>No hay ventas registradas</Text>}
      renderItem={({ item }) => (
        <View style={styles.fila}>
          <View style={{ flex: 1 }}>
            <Text style={styles.nombre}>Venta #{item.id_venta}</Text>
            <Text style={styles.detalle}>{item.fecha_venta} — {item.tipo_venta} — {item.vendedor || "Sin vendedor"}</Text>
          </View>
          <Text style={styles.total}>${Number(item.total_venta).toFixed(2)}</Text>
        </View>
      )}
    />
  );
}

const styles = StyleSheet.create({
  lista: { padding: 16 }, centrado: { flex: 1, justifyContent: "center" },
  titulo: { fontSize: 22, fontWeight: "700" }, subtitulo: { fontSize: 13, color: colores.texto.atenuado, marginBottom: 16 },
  fila: { flexDirection: "row", alignItems: "center", backgroundColor: colores.fondo.blanco, padding: 12, borderRadius: 10, marginBottom: 8, borderWidth: 1, borderColor: colores.borde },
  nombre: { fontSize: 15, fontWeight: "600", color: colores.texto.oscuro },
  detalle: { fontSize: 12, color: colores.texto.atenuado, marginTop: 2 },
  total: { fontSize: 15, fontWeight: "700", color: colores.verde.sabio },
  vacio: { textAlign: "center", color: colores.texto.atenuado, marginTop: 40 },
});
