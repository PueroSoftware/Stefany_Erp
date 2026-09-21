import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { useAuth } from "../contexto/ContextoAuth";
import { colores } from "../tema/colores";
import { estiloBoton } from "../tema/tipografia";

export function CheckoutScreen() {
  const { usuario } = useAuth();
  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Checkout</Text>
      <Text style={{ color: colores.texto.atenuado }}>Dirección: {usuario?.direccion || "Sin dirección"}</Text>
      <Text style={{ color: colores.texto.atenuado }}>Ciudad: {usuario?.ciudad || "-"}</Text>
      <TouchableOpacity style={[styles.boton, { backgroundColor: colores.verde.sabio }]}><Text style={[estiloBoton, { color: colores.texto.claro }]}>Pagar</Text></TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({ contenedor: { flex: 1, padding: 24, justifyContent: "center" }, titulo: { fontSize: 24, fontWeight: "700", marginBottom: 16 }, boton: { padding: 14, borderRadius: 10, alignItems: "center", marginTop: 16 } });