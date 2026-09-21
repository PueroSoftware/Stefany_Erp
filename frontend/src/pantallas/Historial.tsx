import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { colores } from "../tema/colores";

export function HistorialScreen() {
  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Historial de pedidos</Text>
      <Text style={{ color: colores.texto.atenuado }}>Aquí se mostrarán tus pedidos anteriores.</Text>
    </View>
  );
}

const styles = StyleSheet.create({ contenedor: { flex: 1, padding: 24, justifyContent: "center" }, titulo: { fontSize: 24, fontWeight: "700", marginBottom: 16 } });