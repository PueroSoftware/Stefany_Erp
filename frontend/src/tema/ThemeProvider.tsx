// src/tema/ThemeProvider.tsx
// =====================================================================
// PROVEEDOR DE TEMA — Inyecta colores + tipografía vía Context.
// Mismo patrón que ContextoNavegacion.tsx (createContext + useContext
// con guardia). Así cualquier componente consume el tema sin imports
// de rutas relativas sueltas: const { colores } = useTema().
// =====================================================================

import React, { createContext, useContext } from "react";
import { colores } from "./colores";
import { tipografia } from "./tipografia";

// Forma del valor que expone el contexto (tipado estricto con `as const`).
interface Tema {
  colores: typeof colores;
  tipografia: typeof tipografia;
}

// Contexto con valor nulo por defecto (se llena en el Provider).
const ContextoTema = createContext<Tema | null>(null);

// ---- Provider: envuelve la app y expone el tema completo ----
export function ProveedorTema({ children }: { children: React.ReactNode }) {
  const valor: Tema = { colores, tipografia };

  return (
    <ContextoTema.Provider value={valor}>
      {children}
    </ContextoTema.Provider>
  );
}

// ---- Hook: forma limpia y tipada de consumir el tema ----
export function useTema(): Tema {
  const ctx = useContext(ContextoTema);
  if (!ctx) {
    // Error claro si usamos el hook fuera del Provider.
    throw new Error("useTema debe usarse dentro de <ProveedorTema>");
  }
  return ctx;
}