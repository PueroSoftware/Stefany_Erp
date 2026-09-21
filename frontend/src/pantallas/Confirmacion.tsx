import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { colores } from "../tema/colores";

export function ConfirmacionScreen() {
  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.verde.sabio }]}>✅ Pedido confirmado</Text>
      <Text style={{ color: colores.texto.atenuado, marginTop: 16 }}>Tu pedido ha sido recibido. Gracias por comprar en Tienda Jabones.</Text>
    </View>
  );
}

const styles = StyleSheet.create({ contenedor: { flex: 1, alignItems: "center", justifyContent: "center", padding: 24 }, titulo: { fontSize: 28, fontWeight: "700" } });