# Brand Official Sites Reference

Use these domains when searching for official product photography. Search with `site:{domain}` when possible.

| Brand (as in frontmatter) | Official domain(s) | Notes |
|---------------------------|-------------------|-------|
| ESAB | `esab.com`, `esabna.com` | Global and North America sites; product pages under `/na/...` or `/eu/...` |
| GYS | `gys.com`, `gys.fr` | French manufacturer; product images on product detail pages |
| OTC | `otc-daihen.com`, `daihen.co.jp` | Daihen/OTC robotics and welding; search model number |
| Hypertherm | `hypertherm.com` | Plasma cutting systems; high-quality product renders |
| AMG | `amg-machinery.com`, `amg.be` | CNC beam/drilling machines; check regional AMG sites |
| Aotai | `aotaiwelding.com`, `aotai.cn` | MMA/MIG/TIG power sources |
| Kjellberg | `kjellberg-finsterwalde.de`, `kjellberg.com` | Plasma cutting tables and consumables |
| MOSA | `mosa.com`, `mosa-generator.com` | Engine-driven welders/generators |
| Shindaiwa | `shindaiwa.co.jp` | Engine welders; may need model number search |
| Weldflame | `weldflame.com` | Gas apparatus, torches, regulators |
| Wilson | `wilsonweld.com` | Gas welding/cutting accessories |
| Hgstar | `hgstarlaser.com` | Laser cutting machines |
| IKING | `iking.cn`, `ikingtec.com` | Laser welding/cutting equipment |
| Exact | `exact-tools.com` | Pipe cutting tools |
| Axxair | `axxair.com`, `axxair.fr` | Orbital cutting/beveling machines |
| DWT | `dwt-gmbh.com` | Tube processing machinery |
| TBI | `tbi-industries.com` | Welding torches |
| Newfire | `newfire.com.cn` | Welding machines |
| Hyundai | `hdwelding.co.kr` | Welding consumables/equipment |
| Ironcat | `ironcatwelding.com` | Welding equipment |
| Dayok | `dayok.com` | Cutting equipment |
| Generico | (varies) | Generic gas apparatus — search Weldflame/Wilson equivalents |
| Weldmax | (distributor brand) | Search underlying manufacturer catalog |
| Permanent | (distributor brand) | Search underlying manufacturer catalog |

## Search Query Templates

```
"{brand}" "{product title}" site:{domain}
"{brand}" "{model number}" product image site:{domain}
"{product title}" filetype:pdf site:{domain}
```

## Finding High-Resolution URLs

On brand product pages, check in this order:

1. `<meta property="og:image">` — often full-size hero image
2. `<link rel="image_src">` or JSON-LD `"image"` field
3. `<img srcset="...">` — pick the largest width descriptor
4. Lightbox attributes: `data-zoom-image`, `data-large-image`, `data-src`
5. WordPress-style: remove `-300x300` or `-150x150` suffix from filename to get original
6. `<a href="...">` wrapping a thumbnail — href may point to full size

## Image URL Quality Heuristics

| Signal | Likely quality |
|--------|----------------|
| No dimension suffix in filename | Full size |
| `-300x300`, `-150x150`, `-scaled` | Thumbnail — find original |
| `/uploads/` or `/media/` path on brand CDN | Usually official |
| `thumbnail`, `thumb`, `small`, `icon` in path | Low res — avoid |
| `.pdf` cover or catalog scan | Acceptable fallback if no web image |

## Product Photography Signals

| Accept | Reject |
|--------|--------|
| White/gray studio background | Visible welding arc or sparks |
| Product centered, no people | Operator wearing PPE |
| Catalog/e-commerce gallery image | Factory floor wide shot |
| PNG cutout on transparent/neutral bg | Marketing lifestyle banner |
| Spec-sheet product render | Photo where product is background prop |
