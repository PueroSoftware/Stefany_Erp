// src/tema/colores.ts
// =====================================================================
// TOKENS DE COLOR — Fuente única de verdad para toda la app.
// Extraídos de gemini-code-5.xml (paleta de la tienda de jabones).
// Cada componente importa `colores` en vez de escribir hex sueltos.
// `as const` congela los valores y da tipado literal (autocompletado).
// =====================================================================

export const colores = {
  // ---- Fondos (informacion_general > fondo_principal) ----
  fondo: {
    blanco: '#FFFFFF', // blanco puro — fondo base de pantalla
    crema: '#FAF8F5',  // crema muy suave — tarjetas/claras
  },

  // ---- Verdes (colores_secundarios + tarjetas "verde menta") ----
  verde: {
    sabio: '#6B8E5A', // verde sabio — acentos naturales
    menta: '#C9E4D4', // verde menta claro — fondo de tarjetas categoría
  },

  // ---- Acentos cálidos (colores_secundarios) ----
  acento: {
    miel: '#FDD750',     // amarillo miel — badges/insignias
    citrico: '#FA9909',  // naranja cítrico — carrusel "Cítrico fresco"
    floral: '#E8A0BF',   // rosa floral — carrusel "Flora ligera"
    cafe: '#8A5A44',     // café vegetal — jabones/chocolate
  },

  // ---- Insignia dorada vintage (marco_ilustracion de las tarjetas) ----
  insigniaDorada: '#C9A24B',

  // ---- Textos ----
  texto: {
    oscuro: '#1A1A1A', // títulos y texto principal
    atenuado: '#555555', // subtítulos/secundario
    claro: '#FAF8F5',  // texto sobre fondos oscuros
  },

  // ---- Barra inferior / footer (pie_pagina > barra_inferior) ----
  piePagina: '#1A1A1A',      // gris oscuro / negro
  iconoPiePagina: '#6B8E5A', // logo circular verde/negro del footer

  // ---- Utilidades ----
  borde: '#E0E0E0',                              // bordes finos de la rejilla
  cristal: 'rgba(255,255,255,0.25)',             // glassmorphism (cristal)
} as const;

// Tipo derivado para tipar un color si hiciera falta en props.
export type TipoColor = typeof colores[keyof typeof colores];
