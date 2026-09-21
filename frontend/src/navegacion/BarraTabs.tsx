import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useNavegacion, NombrePantalla } from "./ContextoNavegacion";
import { colores } from "../tema/colores";

// Definicion de tabs. Cada tab es una pantalla RAIZ (usa reemplazar, no navegar).
const TABS_CLIENTE: { nombre: NombrePantalla; icono: keyof typeof Ionicons.glyphMap; etiqueta: string }[] = [
  { nombre: "catalogo", icono: "grid-outline", etiqueta: "Catalogo" },
  { nombre: "carrito", icono: "cart-outline", etiqueta: "Carrito" },
  { nombre: "historial", icono: "time-outline", etiqueta: "Historial" },
  { nombre: "perfil", icono: "person-outline", etiqueta: "Perfil" },
];

const TABS_FABRIL: { nombre: NombrePantalla; icono: keyof typeof Ionicons.glyphMap; etiqueta: string }[] = [
  { nombre: "dashboard", icono: "stats-chart-outline", etiqueta: "Panel" },
  { nombre: "inventario", icono: "cube-outline", etiqueta: "Inventario" },
  { nombre: "compras", icono: "bag-outline", etiqueta: "Compras" },
  { nombre: "produccion", icono: "construct-outline", etiqueta: "Produccion" },
  { nombre: "ventas", icono: "cash-outline", etiqueta: "Ventas" },
  { nombre: "usuarios", icono: "people-outline", etiqueta: "Usuarios" },
  { nombre: "perfil", icono: "person-outline", etiqueta: "Perfil" },
];

// Mapas exportados para que AppRoutes sepa cuales pantallas son "raiz" (sin boton volver)
export const ES_RAIZ_CLIENTE: NombrePantalla[] = TABS_CLIENTE.map((t) => t.nombre);
export const ES_RAIZ_FABRIL: NombrePantalla[] = TABS_FABRIL.map((t) => t.nombre);

export function BarraTabs({ esFabril }: { esFabril: boolean }) {
  const { pantalla, reemplazar } = useNavegacion();
  const tabs = esFabril ? TABS_FABRIL : TABS_CLIENTE;

  return (
    <View style={styles.barra}>
      {tabs.map((tab) => {
        const activo = pantalla === tab.nombre;
        const color = activo ? colores.verde.sabio : colores.texto.atenuado;
        return (
          <TouchableOpacity key={tab.nombre} style={styles.tab} onPress={() => reemplazar(tab.nombre)}>
            <Ionicons name={tab.icono} size={20} color={color} />
            <Text style={[styles.etiqueta, { color }, activo && styles.etiquetaActiva]}>{tab.etiqueta}</Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  barra: {
    flexDirection: "row",
    borderTopWidth: 1,
    borderTopColor: colores.borde,
    backgroundColor: colores.fondo.blanco,
    paddingVertical: 8,
  },
  tab: { flex: 1, alignItems: "center", justifyContent: "center", paddingVertical: 2 },
  etiqueta: { fontSize: 10, marginTop: 2 },
  etiquetaActiva: { fontWeight: "700" },
});
