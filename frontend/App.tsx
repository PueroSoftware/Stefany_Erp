import React from "react";
import { StatusBar, SafeAreaView } from "react-native";
import { ProveedorTema } from "./src/tema/ThemeProvider";
import { ProveedorAuth } from "./src/contexto/ContextoAuth";
import { ProveedorNavegacion } from "./src/navegacion/ContextoNavegacion";
import { AppRoutes } from "./src/navegacion/AppRoutes";

export default function App() {
  return (
    <ProveedorTema>
      <ProveedorAuth>
        <ProveedorNavegacion>
          <StatusBar barStyle="dark-content" backgroundColor="#FAF8F5" />
          <SafeAreaView style={{ flex: 1, backgroundColor: "#FAF8F5" }}>
            <AppRoutes />
          </SafeAreaView>
        </ProveedorNavegacion>
      </ProveedorAuth>
    </ProveedorTema>
  );
}
