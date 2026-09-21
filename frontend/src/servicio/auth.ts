import { api, setTokens, clearTokens } from "./api";
import type { Usuario } from "../models/usuario";

export interface LoginPayload {
  correo: string;
  password: string;
}

export interface RegisterPayload {
  nombre: string;
  correo: string;
  password: string;
  telefono?: string;
  tipo: "cliente" | "fabril";
}

export interface LoginResponse {
  access: string;
  refresh: string;
  usuario: Usuario;
}

export async function login({ correo, password }: LoginPayload): Promise<LoginResponse> {
  const { data } = await api.post<LoginResponse>("/auth/login/", { correo, password });
  await setTokens(data.access, data.refresh);
  return data;
}

export async function register(payload: RegisterPayload): Promise<LoginResponse> {
  const { data } = await api.post<LoginResponse>("/auth/register/", payload);
  await setTokens(data.access, data.refresh);
  return data;
}

export async function refreshSession(refreshToken: string) {
  const { data } = await api.post("/auth/token/refresh/", { refresh: refreshToken });
  await setTokens(data.access, data.refresh);
  return data;
}

export async function fetchMe() {
  const { data } = await api.get("/auth/me/");
  return data;
}

export async function updateProfile(payload: Partial<{ nombre: string; apellido: string; telefono: string; direccion: string; ciudad: string }>) {
  const { data } = await api.put("/auth/me/", payload);
  return data;
}

export async function logout() {
  await clearTokens();
}
