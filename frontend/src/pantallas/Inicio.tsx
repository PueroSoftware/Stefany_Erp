// src/pantallas/Inicio.tsx
// =====================================================================
// PANTALLA INICIO — Esqueleto base (Fase 1).
// Desbloquea App.tsx y deja lista la composición con el tema y la
// navegación. En Fase 4 se rellena con Header, CategoryGrid, Carousel
// y BottomBar según gemini-code-5.xml.
// =====================================================================

import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { useTema } from "../tema/ThemeProvider";
import { estiloTituloTarjeta } from "../tema/tipografia";
import { useNavegacion } from "../navegacion/ContextoNavegacion";

export function Inicio() {
  const { colores } = useTema();
  const { pantalla } = useNavegacion();

  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      {/* Título con el estilo manuscrito de las tarjetas (token de tipografia) */}
      <Text style={estiloTituloTarjeta}>Tienda Jabones</Text>
      <Text style={[styles.subtitulo, { color: colores.texto.atenuado }]}>
        Pantalla actual: {pantalla}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
  },
  subtitulo: {
    fontSize: 14,
    marginTop: 8,
  },
});