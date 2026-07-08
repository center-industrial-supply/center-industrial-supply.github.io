import fs from "node:fs";
import path from "node:path";

export interface Product {
  name: string;
  href: string;
  image: string;
  brand: string;
}

const PRODUCT_ROOT = path.join(process.cwd(), "public", "product");

export function getProducts(): Product[] {
  if (!fs.existsSync(PRODUCT_ROOT)) {
    return [];
  }

  const products: Product[] = [];

  for (const entry of fs.readdirSync(PRODUCT_ROOT, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;

    const indexPath = path.join(PRODUCT_ROOT, entry.name, "index.html");
    if (!fs.existsSync(indexPath)) continue;

    const html = fs.readFileSync(indexPath, "utf-8");
    const titleMatch = html.match(/<title>([^<]+)<\/title>/);
    const h3Match = html.match(/class=product-title[^>]*>([^<]+)/);
    const imgMatch = html.match(/wp-content\/uploads\/[^"']+\.(?:jpg|png|webp)/);
    const brandMatch = html.match(/product-brand-container[^>]*>\s*<span>([^<]+)/);

    const name =
      h3Match?.[1]?.trim() ??
      titleMatch?.[1]?.split(" - ")[0]?.trim() ??
      entry.name;

    products.push({
      name,
      href: `/product/${entry.name}/`,
      image: imgMatch?.[0] ?? "wp-content/uploads/woocommerce-placeholder.png",
      brand: brandMatch?.[1]?.trim() ?? "",
    });
  }

  return products.sort((a, b) => a.name.localeCompare(b.name));
}
