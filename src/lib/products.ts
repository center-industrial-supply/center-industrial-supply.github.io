import { getCollection, type CollectionEntry } from "astro:content";
import { brandMatchesProduct, getBrandBySlug } from "../data/brands";

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

function toProductSummary(product: CollectionEntry<"products">): ProductSummary {
  return {
    name: product.data.title,
    href: `/product/${product.data.slug}/`,
    image: primaryProductImage(product.data.images).replace(/^\//, ""),
    brand: product.data.brand ?? "",
  };
}

export async function getProducts(): Promise<ProductSummary[]> {
  const products = await getCollection("products");

  return products.map(toProductSummary).sort((a, b) => a.name.localeCompare(b.name));
}

export async function getProductsByBrand(brandSlug: string): Promise<ProductSummary[]> {
  const brand = getBrandBySlug(brandSlug);
  if (!brand) return [];

  const products = await getCollection("products");

  return products
    .filter((product) => brandMatchesProduct(brand, product.data.brand ?? ""))
    .map(toProductSummary)
    .sort((a, b) => a.name.localeCompare(b.name));
}
