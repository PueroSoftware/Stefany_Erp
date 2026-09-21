import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from "react-native";
import { useAuth } from "../contexto/ContextoAuth";
import { useNavegacion, NombrePantalla } from "../navegacion/ContextoNavegacion";
import { colores } from "../tema/colores";
import { listarMateriasPrimas, listarCompras, listarOrdenesProduccion, listarVentas } from "../servicio/fabril";

const TARJETAS: { nombre: NombrePantalla; titulo: string; descripcion: string }[] = [
  { nombre: "inventario", titulo: "Inventario", descripcion: "Materias primas y stock" },
  { nombre: "compras", titulo: "Compras", descripcion: "Proveedores y adquisiciones" },
  { nombre: "produccion", titulo: "Produccion", descripcion: "Ordenes y productos" },
  { nombre: "ventas", titulo: "Ventas", descripcion: "Pedidos y facturacion" },
  { nombre: "usuarios", titulo: "Usuarios", descripcion: "Clientes y administradores" },
];

export function DashboardScreen() {
  const { usuario } = useAuth();
  const { reemplazar } = useNavegacion();
  const [resumen, setResumen] = useState({ materias: 0, compras: 0, ordenes: 0, ventas: 0 });

  useEffect(() => {
    Promise.all([listarMateriasPrimas(), listarCompras(), listarOrdenesProduccion(), listarVentas()])
      .then(([m, c, o, v]) => setResumen({ materias: m.length, compras: c.length, ordenes: o.length, ventas: v.length }))
      .catch(() => {});
  }, []);

  return (
    <ScrollView style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <View style={styles.cabecera}>
        <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Hola, {usuario?.nombre ?? "Administrador"}</Text>
        <Text style={{ color: colores.texto.atenuado }}>Panel del area fabril</Text>
      </View>
      <View style={styles.grid}>
        {TARJETAS.map((t) => (
          <TouchableOpacity key={t.nombre} style={styles.tarjeta} onPress={() => reemplazar(t.nombre)}>
            <View style={styles.circulo}><Text style={styles.inicial}>{t.titulo.charAt(0)}</Text></View>
            <Text style={styles.tarjetaTitulo}>{t.titulo}</Text>
            <Text style={styles.tarjetaDesc}>{t.descripcion}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <View style={styles.estadisticas}>
        <Text style={styles.estadisticasTitulo}>Resumen rapido</Text>
        {[
          { etiqueta: "Materias primas", valor: resumen.materias },
          { etiqueta: "Compras registradas", valor: resumen.compras },
          { etiqueta: "Ordenes de produccion", valor: resumen.ordenes },
          { etiqueta: "Ventas", valor: resumen.ventas },
        ].map((fila) => (
          <View key={fila.etiqueta} style={styles.filaEstadistica}>
            <Text style={styles.filaEtiqueta}>{fila.etiqueta}</Text>
            <Text style={styles.filaValor}>{fila.valor}</Text>
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  contenedor: { flex: 1, padding: 16 },
  cabecera: { marginBottom: 20 },
  titulo: { fontSize: 22, fontWeight: "700" },
  grid: { gap: 12 },
  tarjeta: { backgroundColor: colores.fondo.blanco, borderRadius: 12, padding: 16, borderWidth: 1, borderColor: colores.borde },
  circulo: { width: 40, height: 40, borderRadius: 20, backgroundColor: colores.verde.menta, justifyContent: "center", alignItems: "center", marginBottom: 8 },
  inicial: { fontSize: 18, fontWeight: "700", color: colores.verde.sabio },
  tarjetaTitulo: { fontSize: 16, fontWeight: "700", color: colores.texto.oscuro },
  tarjetaDesc: { fontSize: 12, color: colores.texto.atenuado, marginTop: 2 },
  estadisticas: { marginTop: 24, backgroundColor: colores.fondo.blanco, borderRadius: 12, padding: 16, borderWidth: 1, borderColor: colores.borde },
  estadisticasTitulo: { fontSize: 16, fontWeight: "700", color: colores.texto.oscuro, marginBottom: 8 },
  filaEstadistica: { flexDirection: "row", justifyContent: "space-between", paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: colores.borde },
  filaEtiqueta: { color: colores.texto.atenuado },
  filaValor: { fontWeight: "700", color: colores.texto.oscuro },
});
