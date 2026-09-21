import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useAuth } from "../contexto/ContextoAuth";
import { useNavegacion } from "../navegacion/ContextoNavegacion";
import { estiloBoton } from "../tema/tipografia";
import { colores } from "../tema/colores";

export function LoginScreen() {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const { navegar } = useNavegacion();

  const handleLogin = async () => {
    if (!correo || !password) { Alert.alert("Error", "Completa todos los campos"); return; }
    setLoading(true);
    try { await login(correo, password); } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Error de login";
      Alert.alert("Error", msg);
    } finally { setLoading(false); }
  };

  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Tienda Jabones</Text>
      <Text style={[styles.subtitulo, { color: colores.texto.atenuado }]}>Inicia sesión para continuar</Text>
      <View style={styles.formulario}>
        <Text style={[styles.label, { color: colores.texto.oscuro }]}>Correo</Text>
        <TextInput style={styles.input} value={correo} onChangeText={setCorreo} placeholder="tu@correo.com" placeholderTextColor={colores.texto.atenuado} autoCapitalize="none" keyboardType="email-address" />
        <Text style={[styles.label, { color: colores.texto.oscuro }]}>Contraseña</Text>
        <TextInput style={styles.input} value={password} onChangeText={setPassword} placeholder="********" placeholderTextColor={colores.texto.atenuado} secureTextEntry />
        <TouchableOpacity style={[styles.boton, { backgroundColor: colores.verde.sabio }]} onPress={handleLogin} disabled={loading}>
          <Text style={[estiloBoton, { color: colores.texto.claro }]}>{loading ? "Entrando..." : "Entrar"}</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity onPress={() => navegar("register")}>
        <Text style={[styles.enlace, { color: colores.verde.sabio }]}>¿No tienes cuenta? Regístrate</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: { flex: 1, alignItems: "center", justifyContent: "center", padding: 24 },
  titulo: { fontSize: 28, fontWeight: "700", marginBottom: 8 },
  subtitulo: { fontSize: 14, marginBottom: 32 },
  formulario: { width: "100%" },
  label: { fontSize: 14, marginBottom: 4, marginTop: 12 },
  input: { backgroundColor: colores.fondo.blanco, borderColor: colores.borde, borderWidth: 1, borderRadius: 8, padding: 12, fontSize: 14, marginBottom: 8 },
  boton: { padding: 14, borderRadius: 10, alignItems: "center", marginTop: 16 },
  enlace: { marginTop: 16, textAlign: "center", fontSize: 14 },
});