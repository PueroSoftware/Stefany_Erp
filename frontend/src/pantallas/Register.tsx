import React, { useState } from "react";
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useAuth } from "../contexto/ContextoAuth";
import { useNavegacion } from "../navegacion/ContextoNavegacion";
import { estiloBoton } from "../tema/tipografia";
import { colores } from "../tema/colores";

export function RegisterScreen() {
  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const [telefono, setTelefono] = useState("");
  const [tipo, setTipo] = useState<"cliente" | "fabril">("cliente");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const { navegar } = useNavegacion();

  const handleRegister = async () => {
    if (!nombre || !correo || !password) { Alert.alert("Error", "Completa nombre, correo y contraseña"); return; }
    setLoading(true);
    try { await register({ nombre, correo, password, telefono, tipo }); } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Error de registro";
      Alert.alert("Error", msg);
    } finally { setLoading(false); }
  };

  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Crear cuenta</Text>
      <Text style={[styles.subtitulo, { color: colores.texto.atenuado }]}>Elige tu tipo de usuario</Text>
      <View style={styles.formulario}>
        <Text style={[styles.label, { color: colores.texto.oscuro }]}>Nombre</Text>
        <TextInput style={styles.input} value={nombre} onChangeText={setNombre} />
        <Text style={[styles.label, { color: colores.texto.oscuro }]}>Correo</Text>
        <TextInput style={styles.input} value={correo} onChangeText={setCorreo} keyboardType="email-address" />
        <Text style={[styles.label, { color: colores.texto.oscuro }]}>Contraseña</Text>
        <TextInput style={styles.input} value={password} onChangeText={setPassword} secureTextEntry />
        <Text style={[styles.label, { color: colores.texto.oscuro }]}>Teléfono (opcional)</Text>
        <TextInput style={styles.input} value={telefono} onChangeText={setTelefono} />
        <View style={styles.filaTipo}>
          {(["cliente", "fabril"] as const).map((t) => (
            <TouchableOpacity key={t} style={[styles.chipTipo, tipo === t && { backgroundColor: colores.verde.sabio }]} onPress={() => setTipo(t)}>
              <Text style={[estiloBoton, { color: tipo === t ? colores.texto.claro : colores.texto.oscuro }]}>{t === "cliente" ? "Cliente" : "Fabril"}</Text>
            </TouchableOpacity>
          ))}
        </View>
        <TouchableOpacity style={[styles.boton, { backgroundColor: colores.verde.sabio }]} onPress={handleRegister} disabled={loading}>
          <Text style={[estiloBoton, { color: colores.texto.claro }]}>{loading ? "Creando..." : "Registrarse"}</Text>
        </TouchableOpacity>
      </View>
      <TouchableOpacity onPress={() => navegar("login")}>
        <Text style={[styles.enlace, { color: colores.verde.sabio }]}>¿Ya tienes cuenta? Inicia sesión</Text>
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
  filaTipo: { flexDirection: "row", gap: 12, marginVertical: 8 },
  chipTipo: { paddingHorizontal: 16, paddingVertical: 10, borderRadius: 8, borderWidth: 1, borderColor: colores.borde },
  boton: { padding: 14, borderRadius: 10, alignItems: "center", marginTop: 16 },
  enlace: { marginTop: 16, textAlign: "center", fontSize: 14 },
});