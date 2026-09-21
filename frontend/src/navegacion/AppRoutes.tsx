import React from "react";
import { View, Text, TouchableOpacity, ActivityIndicator, StyleSheet } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useAuth, useIsFabril } from "../contexto/ContextoAuth";
import { useNavegacion, NombrePantalla } from "./ContextoNavegacion";
import { BarraTabs, ES_RAIZ_CLIENTE, ES_RAIZ_FABRIL } from "./BarraTabs";
import { colores } from "../tema/colores";

// ── Pantallas de autenticación ──────────────────────────────────────────────
import { LoginScreen } from "../pantallas/Login";
import { RegisterScreen } from "../pantallas/Register";

// ── Pantallas de cliente ────────────────────────────────────────────────────
import { CatalogoScreen } from "../pantallas/Catalogo";
import { DetalleImagenScreen } from "../pantallas/DetalleImagen";
import { CarritoScreen } from "../pantallas/Carrito";
import { CheckoutScreen } from "../pantallas/Checkout";
import { ConfirmacionScreen } from "../pantallas/Confirmacion";
import { HistorialScreen } from "../pantallas/Historial";

// ── Pantalla compartida (cliente y fabril) ──────────────────────────────────
import { PerfilScreen } from "../pantallas/Perfil";

// ── Pantallas fabriles (Fase 4) ─────────────────────────────────────────────
import { DashboardScreen } from "../pantallas/Dashboard";
import { InventarioScreen } from "../pantallas/Inventario";
import { ComprasScreen } from "../pantallas/Compras";
import { ProduccionScreen } from "../pantallas/Produccion";
import { VentasScreen } from "../pantallas/Ventas";
import { UsuariosScreen } from "../pantallas/Usuarios";

// Mapa de pantallas por rol. Si la pantalla actual no existe en el mapa del
// rol activo, caemos a la raíz correspondiente (catálogo / dashboard).
const PANTALLAS_CLIENTE: Partial<Record<NombrePantalla, React.ComponentType>> = {
  catalogo: CatalogoScreen,
  detalleImagen: DetalleImagenScreen,
  carrito: CarritoScreen,
  checkout: CheckoutScreen,
  confirmacion: ConfirmacionScreen,
  historial: HistorialScreen,
  perfil: PerfilScreen,
};

const PANTALLAS_FABRIL: Partial<Record<NombrePantalla, React.ComponentType>> = {
  dashboard: DashboardScreen,
  inventario: InventarioScreen,
  compras: ComprasScreen,
  produccion: ProduccionScreen,
  ventas: VentasScreen,
  usuarios: UsuariosScreen,
  perfil: PerfilScreen,
};

export function AppRoutes() {
  const { isAuthenticated, loading } = useAuth();
  const esFabril = useIsFabril();
  const { pantalla, volver } = useNavegacion();

  // Mientras se verifica la sesión guardada en AsyncStorage mostramos carga.
  if (loading) {
    return (
      <View style={[styles.centrado, { backgroundColor: colores.fondo.crema }]}>
        <ActivityIndicator size="large" color={colores.verde.sabio} />
      </View>
    );
  }

  // Sin sesión: solo existen login y register.
  if (!isAuthenticated) {
    return pantalla === "register" ? <RegisterScreen /> : <LoginScreen />;
  }

  // Con sesión: resolvemos la pantalla contra el mapa del rol.
  const mapa = esFabril ? PANTALLAS_FABRIL : PANTALLAS_CLIENTE;
  const PantallaActual = mapa[pantalla] ?? (esFabril ? DashboardScreen : CatalogoScreen);
  const raices = esFabril ? ES_RAIZ_FABRIL : ES_RAIZ_CLIENTE;
  const esRaiz = raices.includes(pantalla);

  return (
    <View style={styles.contenedor}>
      {/* Cabecera con botón volver SOLO en pantallas no-raíz (detalles, checkout...) */}
      {!esRaiz && (
        <View style={styles.cabecera}>
          <TouchableOpacity onPress={volver} style={styles.botonVolver}>
            <Ionicons name="arrow-back" size={20} color={colores.texto.oscuro} />
            <Text style={[styles.textoVolver, { color: colores.texto.oscuro }]}>Volver</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Contenido de la pantalla actual */}
      <View style={styles.contenido}>
        <PantallaActual />
      </View>

      {/* Tabs inferiores según el rol */}
      <BarraTabs esFabril={esFabril} />
    </View>
  );
}

const styles = StyleSheet.create({
  contenedor: { flex: 1, backgroundColor: colores.fondo.crema },
  centrado: { flex: 1, justifyContent: "center", alignItems: "center" },
  cabecera: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: colores.fondo.blanco,
    borderBottomWidth: 1,
    borderBottomColor: colores.borde,
  },
  botonVolver: { flexDirection: "row", alignItems: "center", gap: 6 },
  textoVolver: { fontSize: 15, fontWeight: "600" },
  contenido: { flex: 1 },
});
