export interface Category {
  name: string;
  description: string;
  href: string;
  count?: string;
  image: string;
}

export const categories: Category[] = [
  {
    name: "Standard Equipment",
    description: "MIG, TIG, MMA, plasma, and multi-process welders",
    href: "/product-category/standard-equipment/",
    count: "64",
    image: "/images/categories/standard-equipment.jpg",
  },
  {
    name: "Welding Consumables",
    description: "Electrodes, wires, flux, and filler metals",
    href: "/product-category/welding-consumables/",
    image: "/images/categories/welding-consumables.jpg",
  },
  {
    name: "Engine Driven Welders",
    description: "Portable engine-driven welding power sources",
    href: "/product-category/engine-driven-welder/",
    count: "4",
    image: "/images/categories/engine-driven-welder.jpg",
  },
  {
    name: "Welding Automation",
    description: "Carriages, submerged arc, columns, gantries",
    href: "/product-category/standard-welding-automation/",
    count: "14",
    image: "/images/categories/standard-welding-automation.jpg",
  },
  {
    name: "Robot Systems",
    description: "Welding robots, positioners, material handling",
    href: "/product-category/robot-systems/",
    count: "10",
    image: "/images/categories/robot-systems.jpg",
  },
  {
    name: "CNC Cutting & Drilling",
    description: "Plasma, laser, plate and beam CNC machines",
    href: "/product-category/cutting-drilling-automation/",
    count: "11",
    image: "/images/categories/cutting-drilling-automation.jpg",
  },
  {
    name: "Tube & Pipe Solutions",
    description: "Orbital cutting, bevelling, and welding systems",
    href: "/product-category/tube-and-pipe-cutting-and-welding-solutions/",
    count: "37",
    image: "/images/categories/tube-and-pipe-cutting-and-welding-solutions.jpg",
  },
  {
    name: "Induction Heating",
    description: "Pre-heat and post-heat induction systems",
    href: "/product-category/induction-heating-machine/",
    count: "6",
    image: "/images/categories/induction-heating-machine.jpg",
  },
  {
    name: "PPE & Accessories",
    description: "Helmets, gloves, spectacles, and safety gear",
    href: "/product-category/ppe-and-accessories/",
    count: "19",
    image: "/images/categories/ppe-and-accessories.jpg",
  },
  {
    name: "Laser Welding",
    description: "Advanced laser welding technology",
    href: "/product-category/laser-welding/",
    count: "1",
    image: "/images/categories/laser-welding.jpg",
  },
  {
    name: "Welding & Cutting Torches",
    description: "Manual torches and cutting equipment",
    href: "/product-category/welding-and-cutting-torch/",
    count: "2",
    image: "/images/categories/welding-and-cutting-torch.jpg",
  },
  {
    name: "Stud Welding",
    description: "Stud welding machines and accessories",
    href: "/product-category/stud-welding-equipment/",
    count: "3",
    image: "/images/categories/stud-welding-equipment.jpg",
  },
];
