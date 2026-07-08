import { getCollection } from "astro:content";

export interface ProductSummary {
  name: string;
  href: string;
  image: string;
  brand: string;
}

export async function getProducts(): Promise<ProductSummary[]> {
  const products = await getCollection("products");

  return products
    .map((product) => ({
      name: product.data.title,
      href: `/product/${product.data.slug}/`,
      image: product.data.images?.[0]?.replace(/^\//, "") ?? "wp-content/uploads/woocommerce-placeholder.png",
      brand: product.data.brand ?? "",
    }))
    .sort((a, b) => a.name.localeCompare(b.name));
}
