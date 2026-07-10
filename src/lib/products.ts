import { getCollection } from "astro:content";

export const PRODUCT_PLACEHOLDER = "/wp-content/uploads/woocommerce-placeholder.png";

export interface ProductSummary {
  name: string;
  href: string;
  image: string;
  brand: string;
}

export interface CategoryListItem {
  slug: string;
  title: string;
  image?: string;
}

export async function getProductImageMap(): Promise<Map<string, string>> {
  const products = await getCollection("products");

  return new Map(
    products.map((product) => [
      product.data.slug,
      product.data.images?.[0] ?? PRODUCT_PLACEHOLDER,
    ]),
  );
}

/** Prefer each product's `images` frontmatter over stale paths in category markdown. */
export function resolveCategoryProductImages(
  items: CategoryListItem[] | undefined,
  imageMap: Map<string, string>,
): CategoryListItem[] {
  if (!items) return [];

  return items.map((item) => ({
    ...item,
    image: imageMap.get(item.slug) ?? item.image ?? PRODUCT_PLACEHOLDER,
  }));
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
