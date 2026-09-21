import React from "react";
import { View, Text, StyleSheet, TouchableOpacity, TextInput } from "react-native";
import { colores } from "../tema/colores";
import { estiloBoton } from "../tema/tipografia";

export function HeaderScreen({ titulo }: { titulo: string }) {
  return (<View style={styles.header}><Text style={styles.titulo}>{titulo}</Text></View>);
}

export function Card({ titulo, children }: { titulo: string; children: React.ReactNode }) {
  return (<View style={styles.card}><Text style={styles.cardTitulo}>{titulo}</Text>{children}</View>);
}

export function ButtonPrimary({ title, onPress }: { title: string; onPress: () => void }) {
  return (<TouchableOpacity style={styles.boton} onPress={onPress}><Text style={[estiloBoton, { color: "#FFF" }]}>{title}</Text></TouchableOpacity>);
}

export function Input({ placeholder, value, onChangeText }: { placeholder: string; value: string; onChangeText: (t: string) => void }) {
  return (<TextInput style={styles.input} placeholder={placeholder} value={value} onChangeText={onChangeText} />);
}

export function Chips({ label, active, onPress }: { label: string; active: boolean; onPress: () => void }) {
  return (<TouchableOpacity style={[styles.chip, active && styles.chipActivo]} onPress={onPress}><Text style={active ? { color: "#FFF" } : { color: "#1A1A1A" }}>{label}</Text></TouchableOpacity>);
}

const styles = StyleSheet.create({
  header: { backgroundColor: "#1D1D1B", padding: 16, alignItems: "center" },
  titulo: { color: "#EADDCC", fontSize: 20, fontWeight: "700" },
  card: { backgroundColor: "#FFF", borderRadius: 12, padding: 16, marginBottom: 12, borderColor: "#E0E0E0", borderWidth: 1 },
  cardTitulo: { fontSize: 16, fontWeight: "600", marginBottom: 8 },
  boton: { backgroundColor: "#EADDCC", padding: 14, borderRadius: 10, alignItems: "center" },
  input: { backgroundColor: "#F3F4F6", borderColor: "#E0E0E0", borderWidth: 1, borderRadius: 8, padding: 12, fontSize: 14 },
  chip: { paddingHorizontal: 12, paddingVertical: 8, borderRadius: 8, borderWidth: 1, borderColor: "#E0E0E0" },
  chipActivo: { backgroundColor: "#6B8E5A" },
});