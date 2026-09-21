export interface Usuario {
  id_usuario: number;
  nombre: string;
  apellido: string;
  correo: string;
  telefono: string;
  direccion: string;
  ciudad: string;
  tipo: "cliente" | "fabril";
  estado: "activo" | "inactivo" | "bloqueado";
  activo: boolean;
  fecha_registro: string;
}
