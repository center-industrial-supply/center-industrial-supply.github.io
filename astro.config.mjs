// @ts-check
import { defineConfig } from "astro/config";

// https://astro.build/config
export default defineConfig({
  site: "https://center-industrial-supply.github.io",
  trailingSlash: "always",
  build: {
    format: "directory",
  },
});
