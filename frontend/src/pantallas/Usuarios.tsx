import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, ActivityIndicator } from "react-native";
import { listarUsuarios } from "../servicio/fabril";
import { Usuario } from "../models/usuario";
import { colores } from "../tema/colores";

export function UsuariosScreen() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    listarUsuarios()
      .then((data) => setUsuarios(data as Usuario[]))
      .catch(() => {})
      .finally(() => setCargando(false));
  }, []);

  if (cargando) return <ActivityIndicator size="large" style={styles.centrado} color={colores.verde.sabio} />;

  return (
    <FlatList
      style={{ backgroundColor: colores.fondo.crema }}
      contentContainerStyle={styles.lista}
      data={usuarios}
      keyExtractor={(u) => String(u.id_usuario)}
      ListHeaderComponent={<Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Usuarios</Text>}
      ListEmptyComponent={<Text style={styles.vacio}>No hay usuarios registrados</Text>}
      renderItem={({ item }) => (
        <View style={styles.fila}>
          <View style={styles.avatar}><Text style={styles.avatarLetra}>{item.nombre?.charAt(0) ?? "?"}</Text></View>
          <View style={{ flex: 1 }}>
            <Text style={styles.nombre}>{item.nombre} {item.apellido ?? ""}</Text>
            <Text style={styles.detalle}>{item.correo}</Text>
          </View>
          <View style={[styles.badge, { backgroundColor: item.tipo === "fabril" ? colores.verde.menta : colores.acento.miel + "33" }]}>
            <Text style={[styles.badgeTexto, { color: item.tipo === "fabril" ? colores.verde.sabio : colores.acento.citrico }]}>{item.tipo}</Text>
          </View>
        </View>
      )}
    />
  );
}

const styles = StyleSheet.create({
  lista: { padding: 16 }, centrado: { flex: 1, justifyContent: "center" },
  titulo: { fontSize: 22, fontWeight: "700", marginBottom: 16 },
  fila: { flexDirection: "row", alignItems: "center", backgroundColor: colores.fondo.blanco, padding: 12, borderRadius: 10, marginBottom: 8, borderWidth: 1, borderColor: colores.borde },
  avatar: { width: 36, height: 36, borderRadius: 18, backgroundColor: colores.verde.menta, justifyContent: "center", alignItems: "center", marginRight: 12 },
  avatarLetra: { fontSize: 14, fontWeight: "700", color: colores.verde.sabio },
  nombre: { fontSize: 15, fontWeight: "600", color: colores.texto.oscuro },
  detalle: { fontSize: 12, color: colores.texto.atenuado, marginTop: 2 },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  badgeTexto: { fontSize: 11, fontWeight: "700" },
  vacio: { textAlign: "center", color: colores.texto.atenuado, marginTop: 40 },
});
