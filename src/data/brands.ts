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
    logo: "/images/brands/esab.png",
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
    logo: "/images/brands/otc.png",
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
    logo: "/images/brands/kjellberg.svg",
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
    logo: "",
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
  {
    name: "JFY",
    slug: "jfy",
    logo: "/images/brands/jfy.png",
    tagline: "Sheet metal machines from the TRUMPF family",
    description:
      "JFY builds press brakes, turret punches, shears, and fiber-laser cutting systems for production shops that form and cut sheet metal every day. As a member of the TRUMPF Group, their machines emphasize repeatable accuracy and straightforward operation on carbon steel, stainless, and aluminum. CISC supplies JFY equipment to Philippine fabricators expanding from job-shop work into higher-volume sheet processing.",
  },
  {
    name: "Weldmax",
    slug: "weldmax",
    logo: "/images/brands/weldmax.png",
    tagline: "Filler metals that keep production moving",
    description:
      "Weldmax supplies welding wire and related consumables used on everyday MIG and MAG work in fabrication and repair shops. The line is chosen for consistent feed, clean deposits, and practical packaging for busy stores and site crews. CISC stocks Weldmax consumables so customers can match filler metal to the machines already on their floor.",
  },
  {
    name: "DWT",
    slug: "dwt",
    logo: "/images/brands/dwt.png",
    tagline: "German pipe cutting and beveling on site",
    description:
      "DWT manufactures portable ID-mount and OD-mount pipe bevelers plus cold-cutting clamshells for weld-edge preparation in the field. The machines are built in Bottrop for heavy-wall pipe on pipelines, boilers, and shipyard work where heat-affected zones must stay small. CISC represents DWT pipe tools for Philippine contractors who prepare joints on location rather than in a machine shop.",
  },
  {
    name: "Norton",
    slug: "norton",
    logo: "/images/brands/norton.png",
    tagline: "Abrasives for weld prep and finishing",
    description:
      "Norton, a Saint-Gobain abrasives brand, makes cutting discs, grinding wheels, and finishing products used to dress welds and prepare metal edges. Their bonded and coated abrasives are specified across fabrication, maintenance, and shipyard work. CISC carries Norton abrasives so welders can cut, grind, and blend with materials that match the rest of the CISC equipment lineup.",
  },
  {
    name: "HR Laser",
    slug: "hr-laser",
    logo: "/images/brands/hr-laser.png",
    tagline: "Handheld laser welding for production and repair",
    description:
      "HR Laser builds fiber-laser welding systems for shops that want faster, cleaner joins on thin to medium sheet without the heat input of conventional MIG. Handheld and workstation formats suit both production cells and mobile repair. CISC introduces HR Laser equipment to Philippine fabricators evaluating laser welding alongside their existing arc processes.",
  },
  {
    name: "Taiwan Plasma",
    slug: "taiwan-plasma",
    logo: "/images/brands/taiwan-plasma.png",
    tagline: "Industrial plasma cutting from Taiwan",
    description:
      "Taiwan Plasma Corp. designs portable and CNC plasma cutting systems, including the Pla-Cut range used for plate and structural work. Their machines emphasize stable cutting current and practical torch design for daily shop use. CISC supplies Taiwan Plasma cutters to contractors and fabricators who need dependable air-plasma performance without stepping up to a full CNC cell.",
  },
  {
    name: "Axxair",
    slug: "axxair",
    logo: "/images/brands/axxair.png",
    tagline: "Orbital cutting, beveling, and welding",
    description:
      "Axxair designs orbital machines that cut, bevel, square, and TIG-weld tube and pipe to a consistent geometry. The equipment is widely used in process piping, food-grade stainless, and heat-exchanger work where joint fit-up has to be repeatable. CISC provides Axxair orbital systems to Philippine mechanical contractors and fabricators building sanitary and high-spec tubular assemblies.",
  },
  {
    name: "Max Photonics",
    slug: "max-photonics",
    logo: "/images/brands/max-photonics.png",
    tagline: "Fiber laser sources for welding and cutting",
    description:
      "Max Photonics manufactures fiber-laser sources used in handheld welders and CNC cutting systems. Their modules are specified where shops want compact laser power with straightforward integration into production equipment. CISC offers Max Photonics laser technology as part of a broader welding and cutting lineup for customers moving into laser processes.",
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
  iking: "iking",
  exact: "exact",
  jfy: "jfy",
  weldmax: "weldmax",
  dwt: "dwt",
  norton: "norton",
  "hr laser": "hr-laser",
  hrlaser: "hr-laser",
  "taiwan plasma": "taiwan-plasma",
  taiwanplasma: "taiwan-plasma",
  axxair: "axxair",
  "max photonics": "max-photonics",
  maxphotonics: "max-photonics",
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
