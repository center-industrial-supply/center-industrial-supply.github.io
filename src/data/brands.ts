export interface Brand {
  name: string;
  slug: string;
  /** Official logo path, or empty when no verified asset is available. */
  logo: string;
  description: string;
  tagline: string;
}

export const brands: Brand[] = [
  {
    name: "ESAB",
    slug: "esab",
    logo: "/images/brands/esab.svg",
    tagline: "Global welding and cutting leader",
    description:
      "ESAB brings together a century of welding innovation under one name. From portable inverter machines to automated fabrication systems, their equipment is built for shops that demand repeatable quality. CISC supplies ESAB power sources, consumables, and PPE for shipbuilding, heavy fabrication, and maintenance teams across the Philippines.",
  },
  {
    name: "GYS",
    slug: "gys",
    logo: "/images/brands/gys.svg",
    tagline: "French engineering for the workshop floor",
    description:
      "GYS designs practical welding and induction equipment for everyday production work. Their MIG, TIG, and plasma cutters are known for straightforward controls and dependable output on busy shop floors. Through CISC, Philippine fabricators gain access to GYS machines suited for automotive repair, light structural work, and mobile service applications.",
  },
  {
    name: "OTC",
    slug: "otc",
    logo: "/images/brands/otc.svg",
    tagline: "Robotics and arc welding precision",
    description:
      "OTC DAIHEN specializes in arc welding automation and high-precision robotic cells used in automotive and appliance manufacturing worldwide. Their controllers integrate cleanly with production lines and support complex multi-pass routines. CISC represents OTC robotic systems and welding power sources for customers exploring semi-automated or fully robotic welding solutions.",
  },
  {
    name: "Hypertherm",
    slug: "hypertherm",
    logo: "/images/brands/hypertherm.png",
    tagline: "Plasma cutting performance you can measure",
    description:
      "Hypertherm plasma systems set the benchmark for cut quality, consumable life, and ease of operation on steel, stainless, and aluminum plate. Their Powermax and MAXPRO lines serve everything from field maintenance to CNC profiling. CISC provides Hypertherm cutting equipment and genuine consumables for contractors and fabrication shops that need clean, fast cuts day after day.",
  },
  {
    name: "AMG",
    slug: "amg",
    logo: "/images/brands/amg.png",
    tagline: "Heavy-duty plate processing machinery",
    description:
      "AMG builds large-format equipment for plate cutting, beveling, and drilling used in structural steel and pressure-vessel fabrication. Their machines are engineered for high throughput on thick plate and long production runs. CISC connects Philippine heavy-industry customers with AMG solutions for automated plate preparation and CNC profiling workflows.",
  },
  {
    name: "Aotai",
    slug: "aotai",
    logo: "/images/brands/aotai.png",
    tagline: "Reliable inverter welding at strong value",
    description:
      "Aotai manufactures inverter-based MMA, MIG, and TIG welders that deliver stable arc characteristics without the bulk of traditional transformer machines. Their product line suits training centers, small fabricators, and field crews that need portable, cost-effective power sources. CISC stocks Aotai equipment for customers balancing performance requirements with practical budget constraints.",
  },
  {
    name: "Kjellberg",
    slug: "kjellberg",
    logo: "/images/brands/kjellberg.png",
    tagline: "German plasma and oxy-fuel cutting expertise",
    description:
      "Kjellberg has engineered plasma and gas-cutting technology for industrial plate processing since the early twentieth century. Their HiFocus and Smart Plasma systems are trusted on shipyards and steel service centers where cut edge quality and machine uptime matter most. CISC offers Kjellberg cutting solutions for operations that process medium to heavy plate on a daily basis.",
  },
  {
    name: "MOSA",
    slug: "mosa",
    logo: "/images/brands/mosa.svg",
    tagline: "Engine-driven power where the grid cannot reach",
    description:
      "MOSA produces engine-driven welding generators and auxiliary power units built for construction sites, pipelines, and remote maintenance work. Their diesel and petrol sets combine welding output with AC power for tools and lighting on location. CISC supplies MOSA engine drives to contractors and utilities that weld and work far from permanent electrical infrastructure.",
  },
  {
    name: "Shindaiwa",
    slug: "shindaiwa",
    logo: "/images/brands/shindaiwa.svg",
    tagline: "Engine-driven welding for demanding sites",
    description:
      "Shindaiwa engine-driven welders are designed for outdoor construction, civil works, and emergency repair where portability and fuel efficiency are essential. Rugged enclosures and straightforward servicing keep crews productive in harsh environments. CISC provides Shindaiwa engine-drive welders to Philippine contractors who need dependable arc power on roads, bridges, and industrial projects nationwide.",
  },
  {
    name: "Weldflame",
    slug: "weldflame",
    logo: "/images/brands/weldflame.jpg",
    tagline: "Gas cutting and beveling tools that travel well",
    description:
      "Weldflame produces portable gas cutting machines, pipe bevelers, and magnetic track cutters used on pipelines, tanks, and structural steel in the field. Their equipment is valued for simple setup and consistent travel speed on curved and flat workpieces alike. CISC distributes Weldflame cutting and beveling tools to fitters and maintenance teams working on-site across the archipelago.",
  },
  {
    name: "Wilson",
    slug: "wilson",
    logo: "/images/brands/wilson.jpg",
    tagline: "Gas apparatus and torch components you can trust",
    description:
      "Wilson manufactures regulators, flowmeters, torch handles, and gas apparatus components that keep oxy-fuel and shielding-gas systems running safely. Their products meet recognized industrial standards and are widely used in combination with cutting and welding setups. CISC carries Wilson gas equipment and torch parts for shops maintaining legacy oxy-fuel rigs and modern MIG/TIG installations.",
  },
  {
    name: "Hgstar",
    slug: "hgstar",
    logo: "/images/brands/hgstar.png",
    tagline: "Specialized welding and cutting consumables",
    description:
      "Hgstar supplies welding and cutting consumables tailored for specific processes and base materials used in fabrication and repair work. From contact tips and nozzles to specialty accessories, their catalog supports shops that want consistent spare-part availability alongside their primary equipment. CISC offers Hgstar consumables as part of a complete supply solution for ongoing production needs.",
  },
  {
    name: "IKING",
    slug: "iking",
    logo: "/images/brands/iking.jpg",
    tagline: "Stud welding systems for structural connections",
    description:
      "IKING builds stud welding equipment used to fasten shear connectors, anchors, and threaded studs to steel plate and concrete forms. Their drawn-arc and capacitor-discharge systems serve bridge decks, precast plants, and industrial flooring applications. CISC supplies IKING stud welders and accessories to contractors who need certified, repeatable stud attachment on structural projects.",
  },
  {
    name: "Exact",
    slug: "exact",
    logo: "/images/brands/exact.png",
    tagline: "Pipe cutting and preparation on the job",
    description:
      "Exact manufactures portable pipe saws and preparation tools that give fitters square, burr-free cuts on stainless, carbon steel, and alloy pipe in tight spaces. Battery-powered and pneumatic options reduce setup time compared with traditional abrasive methods. CISC provides Exact pipe cutting tools to mechanical contractors and process piping teams working in refineries, power plants, and commercial builds.",
  },
];

/** Map product frontmatter brand strings to canonical brand slugs. */
const brandAliases: Record<string, string> = {
  esab: "esab",
  gys: "gys",
  otc: "otc",
  hypertherm: "hypertherm",
  amg: "amg",
  aotai: "aotai",
  kjellberg: "kjellberg",
  mosa: "mosa",
  shindaiwa: "shindaiwa",
  weldflame: "weldflame",
  wilson: "wilson",
  hgstar: "hgstar",
  iking: "iking",
  exact: "exact",
};

export function getBrandBySlug(slug: string): Brand | undefined {
  return brands.find((brand) => brand.slug === slug);
}

export function brandNameToSlug(name: string): string | undefined {
  const normalized = name.trim().toLowerCase();
  return brandAliases[normalized];
}

export function brandMatchesProduct(brand: Brand, productBrand: string): boolean {
  if (!productBrand) return false;
  const slug = brandNameToSlug(productBrand);
  return slug === brand.slug;
}
