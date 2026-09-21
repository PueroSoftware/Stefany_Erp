import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ActivityIndicator } from "react-native";
import { useAuth } from "../contexto/ContextoAuth";
import { fetchMe, updateProfile } from "../servicio/auth";
import { colores } from "../tema/colores";
import { estiloBoton } from "../tema/tipografia";

export function PerfilScreen() {
  const { usuario, logout } = useAuth();
  const [loading, setLoading] = useState(true);
  const [nombre, setNombre] = useState("");
  const [telefono, setTelefono] = useState("");
  const [direccion, setDireccion] = useState("");
  const [ciudad, setCiudad] = useState("");

  useEffect(() => {
    (async () => { const data = await fetchMe(); setNombre(data.nombre); setTelefono(data.telefono); setDireccion(data.direccion); setCiudad(data.ciudad); setLoading(false); })();
  }, []);

  const guardar = async () => { await updateProfile({ nombre, telefono, direccion, ciudad }); };

  if (loading) return <ActivityIndicator size="large" />;

  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Perfil</Text>
      <TextInput style={styles.input} value={nombre} onChangeText={setNombre} placeholder="Nombre" />
      <TextInput style={styles.input} value={telefono} onChangeText={setTelefono} placeholder="Teléfono" />
      <TextInput style={styles.input} value={direccion} onChangeText={setDireccion} placeholder="Dirección" />
      <TextInput style={styles.input} value={ciudad} onChangeText={setCiudad} placeholder="Ciudad" />
      <TouchableOpacity style={[styles.boton, { backgroundColor: colores.verde.sabio }]} onPress={guardar}><Text style={[estiloBoton, { color: colores.texto.claro }]}>Guardar</Text></TouchableOpacity>
      <TouchableOpacity onPress={logout} style={{ marginTop: 16 }}><Text style={{ color: "#D32F2F" }}>Cerrar sesión</Text></TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({ contenedor: { flex: 1, padding: 24 }, titulo: { fontSize: 24, fontWeight: "700", marginBottom: 16 }, input: { backgroundColor: "#FFF", borderColor: "#E0E0E0", borderWidth: 1, borderRadius: 8, padding: 12, marginBottom: 8, fontSize: 14 }, boton: { padding: 14, borderRadius: 10, alignItems: "center", marginTop: 16 } });