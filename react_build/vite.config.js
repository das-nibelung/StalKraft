import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: "build", // Папка для бандлов
    assetsDir: "assets", // Подпапка для CSS, images
    rollupOptions: {
      output: {
        entryFileNames: "js/[name].js", // JS в build/js/
        chunkFileNames: "js/[name].js",
        assetFileNames: ({ name }) => {
          if (/\.css$/.test(name ?? "")) {
            return "css/[name].[ext]"; // CSS в build/css/
          }
          return "assets/[name].[ext]";
        },
      },
    },
  },
  server: {
    port: 3000, // Dev порт
    open: false,
  },
});
