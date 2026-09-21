import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { useAuth } from "../contexto/ContextoAuth";
import { useNavegacion } from "../navegacion/ContextoNavegacion";
import { colores } from "../tema/colores";
import { estiloBoton } from "../tema/tipografia";

// Detalle de una imagen del catálogo. Los parámetros llegan por ContextoNavegacion
// (useNavegacion().parametros) — ya no dependemos de React Navigation.
export function DetalleImagenScreen() {
  const { parametros, navegar } = useNavegacion();
  const { usuario } = useAuth();
  const id = Number(parametros.id ?? 0);

  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Imagen #{id}</Text>
      <View style={styles.imagePlaceholder}><Text style={{ fontSize: 80 }}>🧼</Text></View>
      <Text style={styles.info}>ID: {id}</Text>
      <Text style={styles.info}>Usuario: {usuario?.nombre}</Text>
      <TouchableOpacity style={[styles.boton, { backgroundColor: colores.verde.sabio }]} onPress={() => navegar("carrito")}>
        <Text style={[estiloBoton, { color: colores.texto.claro }]}>Añadir al carrito</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: { flex: 1, alignItems: "center", padding: 24 },
  titulo: { fontSize: 24, fontWeight: "700", marginBottom: 16 },
  imagePlaceholder: { width: 200, height: 200, backgroundColor: colores.fondo.blanco, borderRadius: 12, justifyContent: "center", alignItems: "center", marginBottom: 16 },
  info: { fontSize: 14, color: colores.texto.atenuado, marginBottom: 4 },
  boton: { padding: 14, borderRadius: 10, alignItems: "center", marginTop: 16, width: "100%" },
});
