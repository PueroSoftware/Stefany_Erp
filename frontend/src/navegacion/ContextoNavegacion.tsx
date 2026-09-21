import React, { createContext, useContext, useState, ReactNode } from "react";

export type NombrePantalla =
  | "login" | "register"
  | "catalogo" | "detalleImagen" | "carrito" | "checkout" | "confirmacion" | "historial" | "perfil"
  | "dashboard"
  | "inventario" | "compras" | "produccion" | "ventas" | "usuarios";

export type ParametrosPantalla = Record<string, unknown>;

interface EstadoNavegacion {
  pantalla: NombrePantalla;
  parametros: ParametrosPantalla;
  navegar: (p: NombrePantalla, params?: ParametrosPantalla) => void;
  reemplazar: (p: NombrePantalla, params?: ParametrosPantalla) => void;
  volver: () => void;
}

const ContextoNavegacion = createContext<EstadoNavegacion | null>(null);

export function ProveedorNavegacion({ children }: { children: ReactNode }) {
  const [pila, setPila] = useState<{ pantalla: NombrePantalla; parametros: ParametrosPantalla }[]>([
    { pantalla: "login", parametros: {} },
  ]);

  // navegar = "empujar" a la pila (detalle encima de catálogo, etc.)
  const navegar = (pantalla: NombrePantalla, parametros: ParametrosPantalla = {}) => {
    setPila((anterior) => [...anterior, { pantalla, parametros }]);
  };

  // reemplazar = "resetear" la pila a una sola pantalla raíz.
  // Lo usan los tabs: cambiar de pestaña NO debe acumular pila.
  const reemplazar = (pantalla: NombrePantalla, parametros: ParametrosPantalla = {}) => {
    setPila((anterior) => {
      const ultima = anterior[anterior.length - 1];
      if (ultima.pantalla === pantalla) return anterior; // ya estamos ahí, no hacer nada
      return [{ pantalla, parametros }];
    });
  };

  const volver = () => {
    setPila((anterior) =>
      anterior.length > 1 ? anterior.slice(0, -1) : anterior,
    );
  };

  const actual = pila[pila.length - 1];

  return (
    <ContextoNavegacion.Provider value={{ pantalla: actual.pantalla, parametros: actual.parametros, navegar, reemplazar, volver }}>
      {children}
    </ContextoNavegacion.Provider>
  );
}

export function useNavegacion(): EstadoNavegacion {
  const ctx = useContext(ContextoNavegacion);
  if (!ctx) throw new Error("useNavegacion debe usarse dentro de <ProveedorNavegacion>");
  return ctx;
}
