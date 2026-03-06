import resolve from "@rollup/plugin-node-resolve";
import terser from "@rollup/plugin-terser";
import typescript from "@rollup/plugin-typescript";

export default {
  input: "src/genius-lyrics-card.ts",
  output: {
    file: "dist/genius-lyrics-card.js",
    format: "es",
    sourcemap: true,
  },
  plugins: [resolve(), typescript({ tsconfig: "./tsconfig.json" }), terser()],
};
