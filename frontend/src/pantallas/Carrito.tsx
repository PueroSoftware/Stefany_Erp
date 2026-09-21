import React from "react";
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from "react-native";
import { colores } from "../tema/colores";
import { estiloBoton } from "../tema/tipografia";

interface ItemCarrito { id: number; clave_r2: string; precio: number; cantidad: number; }

export function CarritoScreen() {
  const items: ItemCarrito[] = [];
  const total = items.reduce((s, i) => s + i.precio * i.cantidad, 0);

  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Carrito</Text>
      {items.length === 0 ? <Text style={{ color: colores.texto.atenuado }}>Tu carrito está vacío</Text> : (
        <>
          <FlatList data={items} keyExtractor={(i) => String(i.id)} renderItem={({ item }) => (
            <View style={styles.fila}><Text>{item.clave_r2}</Text><Text>{item.cantidad}x — ${item.precio}</Text></View>
          )} />
          <Text style={styles.total}>Total: ${total}</Text>
          <TouchableOpacity style={[styles.boton, { backgroundColor: colores.verde.sabio }]}><Text style={[estiloBoton, { color: colores.texto.claro }]}>Continuar</Text></TouchableOpacity>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: { flex: 1, padding: 16 }, titulo: { fontSize: 24, fontWeight: "700", marginBottom: 16 },
  fila: { flexDirection: "row", justifyContent: "space-between", padding: 12, backgroundColor: "#FFF", borderRadius: 8, marginBottom: 8 },
  total: { fontSize: 18, fontWeight: "700", marginTop: 16, textAlign: "right" },
  boton: { padding: 14, borderRadius: 10, alignItems: "center", marginTop: 16 },
});