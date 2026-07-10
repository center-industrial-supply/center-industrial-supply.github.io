import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const breadcrumbSchema = z.object({
  label: z.string(),
  href: z.string().optional(),
});

const categoryItemSchema = z.object({
  slug: z.string(),
  title: z.string(),
  image: z.string().optional(),
});

const products = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/products" }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    layout: z.literal("product"),
    description: z.string().optional(),
    brand: z.string().optional(),
    category: z.string().optional(),
    images: z.array(z.string()).optional(),
    breadcrumb: z.array(breadcrumbSchema).optional(),
  }),
});

const productCategories = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/product-categories" }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    layout: z.literal("category"),
    description: z.string().optional(),
    image: z.string().optional(),
    parent: z.string().optional(),
    subcategories: z.array(categoryItemSchema).optional(),
    products: z.array(categoryItemSchema).optional(),
    breadcrumb: z.array(breadcrumbSchema).optional(),
  }),
});

const brandProductCategorySchema = z.object({
  slug: z.string(),
  title: z.string(),
  categoryPath: z.string(),
});

const brands = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/brands" }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    layout: z.literal("brand"),
    description: z.string().optional(),
    featured: z.boolean().optional(),
    officialUrl: z.string().url().optional(),
    logo: z.string().optional(),
    productCount: z.number().optional(),
    brandProductCategories: z.array(brandProductCategorySchema).optional(),
  }),
});

export const collections = {
  products,
  "product-categories": productCategories,
  brands,
};
