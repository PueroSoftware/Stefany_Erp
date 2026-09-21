import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

const BASE_URL = "http://10.0.2.2:8000/api";

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const refreshToken = await AsyncStorage.getItem("refresh_token");
        const { data } = await axios.post(
          `${BASE_URL}/auth/token/refresh/`,
          { refresh: refreshToken }
        );
        await AsyncStorage.setItem("access_token", data.access);
        await AsyncStorage.setItem("refresh_token", data.refresh);
        original.headers.Authorization = `Bearer ${data.access}`;
        return axios(original);
      } catch {
        await AsyncStorage.removeItem("access_token");
        await AsyncStorage.removeItem("refresh_token");
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

export async function setTokens(access: string, refresh: string) {
  await AsyncStorage.setItem("access_token", access);
  await AsyncStorage.setItem("refresh_token", refresh);
}

export async function getAccessToken(): Promise<string | null> {
  return AsyncStorage.getItem("access_token");
}

export async function clearTokens() {
  await AsyncStorage.removeItem("access_token");
  await AsyncStorage.removeItem("refresh_token");
}
