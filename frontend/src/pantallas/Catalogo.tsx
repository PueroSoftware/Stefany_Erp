import React, { useEffect, useState } from "react";
import { View, Text, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator, Alert } from "react-native";
import { useAuth } from "../contexto/ContextoAuth";
import { api } from "../servicio/api";
import { colores } from "../tema/colores";
import { estiloBoton } from "../tema/tipografia";
import { useNavegacion } from "../navegacion/ContextoNavegacion";

interface ItemStorage { id_archivo: number; clave_r2: string; url_publica: string; grupo: string; orden: number; }

export function CatalogoScreen() {
  const [items, setItems] = useState<ItemStorage[]>([]);
  const [loading, setLoading] = useState(true);
  const [grupo, setGrupo] = useState("");
  const { navegar } = useNavegacion();

  const fetchCatalogo = async () => {
    try {
      const params = new URLSearchParams();
      if (grupo) params.set("grupo", grupo);
      const { data } = await api.get<ItemStorage[]>(`/storage/imagenes/?${params}`);
      setItems(data);
    } catch { Alert.alert("Error", "No se pudo cargar el catálogo"); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchCatalogo(); }, [grupo]);

  if (loading) return <ActivityIndicator size="large" />;

  return (
    <View style={[styles.contenedor, { backgroundColor: colores.fondo.crema }]}>
      <Text style={[styles.titulo, { color: colores.texto.oscuro }]}>Catálogo</Text>
      <View style={styles.filtros}>
        {["", "grupos", "esencias"].map((g) => (
          <TouchableOpacity key={g} style={[styles.chip, !grupo && g === "" && styles.chipActivo]} onPress={() => setGrupo(g)}>
            <Text style={[estiloBoton, { color: colores.texto.oscuro }]}>{g || "Todos"}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <FlatList data={items} keyExtractor={(i) => String(i.id_archivo)} numColumns={2} contentContainerStyle={styles.grid}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.card} onPress={() => navegar("detalleImagen", { id: item.id_archivo })}>
            <Text style={{ fontSize: 40 }}>🧼</Text>
            <Text style={{ fontSize: 12, color: colores.texto.oscuro }}>{item.grupo}</Text>
            <Text style={{ fontSize: 10, color: colores.texto.atenuado }}>{item.clave_r2}</Text>
          </TouchableOpacity>
        )} />
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: { flex: 1, padding: 16 }, titulo: { fontSize: 24, fontWeight: "700", marginBottom: 16 },
  filtros: { flexDirection: "row", gap: 8, marginBottom: 16 },
  chip: { paddingHorizontal: 12, paddingVertical: 8, borderRadius: 8, borderWidth: 1, borderColor: colores.borde },
  chipActivo: { backgroundColor: colores.verde.menta }, grid: { gap: 12 },
  card: { flex: 1, backgroundColor: colores.fondo.blanco, borderRadius: 12, padding: 16, alignItems: "center" },
});