import React, { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { Usuario } from "../models/usuario";
import { login as apiLogin, register as apiRegister, fetchMe, logout as apiLogout, refreshSession } from "../servicio/auth";
import { getAccessToken, clearTokens } from "../servicio/api";

interface AuthState {
  usuario: Usuario | null;
  tipo: "cliente" | "fabril" | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (correo: string, password: string) => Promise<void>;
  register: (payload: { nombre: string; correo: string; password: string; telefono?: string; tipo: "cliente" | "fabril" }) => Promise<void>;
  logout: () => Promise<void>;
  checkSession: () => Promise<void>;
}

const ContextoAuth = createContext<AuthState | null>(null);

export function ProveedorAuth({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [tipo, setTipo] = useState<"cliente" | "fabril" | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  const checkSession = async () => {
    try {
      const token = await getAccessToken();
      if (!token) { setLoading(false); return; }
      const data = await fetchMe();
      setUsuario(data);
      setTipo(data.tipo);
      setIsAuthenticated(true);
    } catch {
      await clearTokens();
      setUsuario(null);
      setTipo(null);
      setIsAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const login = async (correo: string, password: string) => {
    const data = await apiLogin({ correo, password });
    setUsuario(data.usuario);
    setTipo(data.usuario.tipo);
    setIsAuthenticated(true);
  };

  const register = async (payload: { nombre: string; correo: string; password: string; telefono?: string; tipo: "cliente" | "fabril" }) => {
    const data = await apiRegister(payload);
    setUsuario(data.usuario);
    setTipo(data.usuario.tipo);
    setIsAuthenticated(true);
  };

  const logout = async () => {
    await apiLogout();
    setUsuario(null);
    setTipo(null);
    setIsAuthenticated(false);
  };

  useEffect(() => { checkSession(); }, []);

  return (
    <ContextoAuth.Provider value={{ usuario, tipo, isAuthenticated, loading, login, register, logout, checkSession }}>
      {children}
    </ContextoAuth.Provider>
  );
}

export function useAuth(): AuthState {
  const ctx = useContext(ContextoAuth);
  if (!ctx) throw new Error("useAuth debe usarse dentro de <ProveedorAuth>");
  return ctx;
}

export function useIsFabril(): boolean {
  return useAuth().tipo === "fabril";
}

export function useIsAuthenticated(): boolean {
  return useAuth().isAuthenticated;
}
