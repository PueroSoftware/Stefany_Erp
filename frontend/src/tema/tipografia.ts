// src/tema/tipografia.ts
// =====================================================================
// TOKENS DE TIPOGRAFÍA — coherencia de texto en toda la app.
// Fuente manuscrita = títulos de tarjetas (vibe artesanal/orgánica).
// Fuente sans-serif = botones y texto UI (limpio y legible).
// NOTA: la fuente manuscrita debe registrarse con expo-font en App.tsx
//       (p.ej. Font.loadAsync({ 'Manuscrita': require('./fuentes/...') })).
// =====================================================================

export const tipografia = {
  // ---- Familias (deben coincidir con el nombre registrado en expo-font) ----
  familia: {
    manuscrita: 'Manuscrita', // estilo orgánico/manuscrito (títulos tarjeta)
    sans: 'System',           // sans-serif del sistema (botones/UI)
  },

  // ---- Tamaños (en px, unidad de RN) ----
  tamano: {
    tituloTarjeta: 20,
    subtitulo: 16,
    cuerpo: 14,
    boton: 14,
    pequeno: 12,
    grande: 28, // título de pantalla / hero
  },

  // ---- Pesos ----
  peso: {
    regular: '400',
    medio: '600',
    negrita: '700',
  },

  // ---- Interlineado recomendado (proporcional al tamaño) ----
  linea: {
    apretada: 1.2,
    normal: 1.4,
  },
} as const;

// Estilo compuesto reutilizable para un "título de tarjeta manuscrito".
// Se usa así: <Text style={estiloTituloTarjeta}>Jabón Rosa</Text>
export const estiloTituloTarjeta = {
  fontFamily: tipografia.familia.manuscrita,
  fontSize: tipografia.tamano.tituloTarjeta,
  fontWeight: tipografia.peso.medio as '600',
  lineHeight: Math.round(tipografia.tamano.tituloTarjeta * tipografia.linea.normal),
  color: '#1A1A1A',
};

// Estilo para botones (sans-serif, limpio).
export const estiloBoton = {
  fontFamily: tipografia.familia.sans,
  fontSize: tipografia.tamano.boton,
  fontWeight: tipografia.peso.negrita as '700',
  color: '#1A1A1A',
};
