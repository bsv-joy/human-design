import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      fontFamily: {
        sans: ["var(--font-inter)"],
        serif: ["var(--font-playfair)"],
      },
      colors: {
        gold: {
          50: "var(--color-gold-50)",
          100: "var(--color-gold-100)",
          200: "var(--color-gold-200)",
          300: "var(--color-gold-300)",
          400: "var(--color-gold-400)",
          500: "var(--color-gold-500)",
          600: "var(--color-gold-600)",
          700: "var(--color-gold-700)",
          800: "var(--color-gold-800)",
          900: "var(--color-gold-900)",
        },
        electric: {
          50: "var(--color-electric-50)",
          100: "var(--color-electric-100)",
          200: "var(--color-electric-200)",
          300: "var(--color-electric-300)",
          400: "var(--color-electric-400)",
          500: "var(--color-electric-500)",
          600: "var(--color-electric-600)",
          700: "var(--color-electric-700)",
          800: "var(--color-electric-800)",
          900: "var(--color-electric-900)",
        },
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [require("tailwindcss-animate"), require("@tailwindcss/typography")],
};
export default config;
