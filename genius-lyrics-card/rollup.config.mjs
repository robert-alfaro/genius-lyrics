import resolve from "@rollup/plugin-node-resolve";
import typescript from "@rollup/plugin-typescript";
import { terser } from "rollup-plugin-terser";

export default {
  input: "src/genius-lyrics-card.ts",
  output: {
    file: "dist/genius-lyrics-card.js",
    format: "es",
    sourcemap: true,
  },
  plugins: [resolve(), typescript({ tsconfig: "./tsconfig.json" }), terser()],
};
