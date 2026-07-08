export interface Category {
  name: string;
  description: string;
  href: string;
  count?: string;
  icon: string;
}

export const categories: Category[] = [
  {
    name: "Standard Equipment",
    description: "MIG, TIG, MMA, plasma, and multi-process welders",
    href: "/product-category/standard-equipment/",
    count: "64",
    icon: "⚙",
  },
  {
    name: "Welding Consumables",
    description: "Electrodes, wires, flux, and filler metals",
    href: "/product-category/welding-consumables/",
    icon: "🔥",
  },
  {
    name: "Engine Driven Welders",
    description: "Portable engine-driven welding power sources",
    href: "/product-category/engine-driven-welder/",
    count: "4",
    icon: "🔧",
  },
  {
    name: "Welding Automation",
    description: "Carriages, submerged arc, columns, gantries",
    href: "/product-category/standard-welding-automation/",
    count: "14",
    icon: "🤖",
  },
  {
    name: "Robot Systems",
    description: "Welding robots, positioners, material handling",
    href: "/product-category/robot-systems/",
    count: "10",
    icon: "🦾",
  },
  {
    name: "CNC Cutting & Drilling",
    description: "Plasma, laser, plate and beam CNC machines",
    href: "/product-category/cutting-drilling-automation/",
    count: "11",
    icon: "✂️",
  },
  {
    name: "Tube & Pipe Solutions",
    description: "Orbital cutting, bevelling, and welding systems",
    href: "/product-category/tube-and-pipe-cutting-and-welding-solutions/",
    count: "37",
    icon: "🔗",
  },
  {
    name: "Induction Heating",
    description: "Pre-heat and post-heat induction systems",
    href: "/product-category/induction-heating-machine/",
    count: "6",
    icon: "🌡",
  },
  {
    name: "PPE & Accessories",
    description: "Helmets, gloves, spectacles, and safety gear",
    href: "/product-category/ppe-and-accessories/",
    count: "19",
    icon: "🦺",
  },
  {
    name: "Laser Welding",
    description: "Advanced laser welding technology",
    href: "/product-category/laser-welding/",
    count: "1",
    icon: "✨",
  },
  {
    name: "Welding & Cutting Torches",
    description: "Manual torches and cutting equipment",
    href: "/product-category/welding-and-cutting-torch/",
    count: "2",
    icon: "🔦",
  },
  {
    name: "Stud Welding",
    description: "Stud welding machines and accessories",
    href: "/product-category/stud-welding-equipment/",
    count: "3",
    icon: "📌",
  },
];
