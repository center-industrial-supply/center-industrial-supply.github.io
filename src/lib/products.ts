import { getCollection } from "astro:content";

export interface ProductSummary {
  name: string;
  href: string;
  image: string;
  brand: string;
}

const PLACEHOLDER_IMAGE = "/wp-content/uploads/woocommerce-placeholder.png";

function primaryProductImage(images?: string[]): string {
  return images?.[0] ?? PLACEHOLDER_IMAGE;
}

export async function getProductImageMap(): Promise<Map<string, string>> {
  const products = await getCollection("products");

  return new Map(
    products.map((product) => [product.data.slug, primaryProductImage(product.data.images)]),
  );
}

export async function getProductTitleMap(): Promise<Map<string, string>> {
  const products = await getCollection("products");

  return new Map(products.map((product) => [product.data.slug, product.data.title]));
}

export async function getProducts(): Promise<ProductSummary[]> {
  const products = await getCollection("products");

  return products
    .map((product) => ({
      name: product.data.title,
      href: `/product/${product.data.slug}/`,
      image: primaryProductImage(product.data.images).replace(/^\//, ""),
      brand: product.data.brand ?? "",
    }))
    .sort((a, b) => a.name.localeCompare(b.name));
}
