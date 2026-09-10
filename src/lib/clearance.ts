import { getCollection } from "astro:content";
import { categories, type Category } from "../data/categories";
import { isClearanceProduct, toProductSummary, type ProductSummary } from "./products";

function categorySlugFromHref(href: string): string {
  return href.replace(/^\/product-category\//, "").replace(/\/$/, "");
}

export function inCategoryTree(
  productCategory: string | undefined,
  categorySlug: string,
): boolean {
  if (!productCategory) return false;
  return productCategory === categorySlug || productCategory.startsWith(`${categorySlug}/`);
}

export async function getClearanceEntries() {
  const products = await getCollection("products");
  return products.filter(isClearanceProduct);
}

export async function getClearanceSlugSet(): Promise<Set<string>> {
  const entries = await getClearanceEntries();
  return new Set(entries.map((product) => product.data.slug));
}

export async function getClearanceTopCategories(): Promise<Category[]> {
  const entries = await getClearanceEntries();
  if (entries.length === 0) return [];

  return categories.flatMap((category) => {
    const slug = categorySlugFromHref(category.href);
    const count = entries.filter((product) => inCategoryTree(product.data.category, slug)).length;
    if (count === 0) return [];
    return [
      {
        ...category,
        href: `/clearance/${slug}/`,
        count: String(count),
      },
    ];
  });
}

export function getTopLevelCategory(slug: string): Category | undefined {
  return categories.find((category) => categorySlugFromHref(category.href) === slug);
}

export async function getClearanceProductsInCategory(categorySlug: string): Promise<ProductSummary[]> {
  const entries = await getClearanceEntries();

  return entries
    .filter((product) => inCategoryTree(product.data.category, categorySlug))
    .map(toProductSummary)
    .sort((a, b) => a.name.localeCompare(b.name));
}
