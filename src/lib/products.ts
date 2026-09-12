import { getCollection } from "astro:content";
import { brandNameToSlug } from "../data/brands";

export interface ProductSummary {
  name: string;
  href: string;
  image: string;
  brand: string;
  clearance: boolean;
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

export function isClearanceProduct(product: {
  data: { clearance?: boolean };
}): boolean {
  return product.data.clearance === true;
}

export function toProductSummary(product: {
  data: { title: string; slug: string; images?: string[]; brand?: string; clearance?: boolean };
}): ProductSummary {
  return {
    name: product.data.title,
    href: `/product/${product.data.slug}/`,
    image: primaryProductImage(product.data.images).replace(/^\//, ""),
    brand: product.data.brand ?? "",
    clearance: isClearanceProduct(product),
  };
}

export async function getProducts(): Promise<ProductSummary[]> {
  const products = await getCollection("products");

  return products.map(toProductSummary).sort((a, b) => a.name.localeCompare(b.name));
}

export async function getProductsByBrand(brandSlug: string): Promise<ProductSummary[]> {
  const products = await getCollection("products");

  return products
    .filter((product) => brandNameToSlug(product.data.brand ?? "") === brandSlug)
    .map(toProductSummary)
    .sort((a, b) => a.name.localeCompare(b.name));
}
