// Mock data for GitHub Pages deployment
// This data is used when REACT_APP_USE_MOCK_DATA=true

export const mockProducts = [
  {
    id: 1,
    name: "Laptop Dell XPS 15",
    price: 7499.99,
    old_price: 8999.99,
    description:
      "Powerful laptop with Intel Core i7, 16GB RAM, and 512GB SSD. Perfect for professionals and content creators.",
    categories: [{ id: 1, name: "Laptops" }],
    tags: [
      { id: 1, name: "premium" },
      { id: 2, name: "professional" },
    ],
    photos: [{ path: "laptops/dell-xps-15.jpg" }],
  },
  {
    id: 2,
    name: "iPhone 14 Pro",
    price: 5499.99,
    old_price: 5999.99,
    description:
      "Latest iPhone with A16 Bionic chip, Pro camera system, and Dynamic Island.",
    categories: [{ id: 2, name: "Smartphones" }],
    tags: [
      { id: 3, name: "apple" },
      { id: 4, name: "flagship" },
    ],
    photos: [{ path: "phones/iphone-14-pro.jpg" }],
  },
  {
    id: 3,
    name: "Samsung Galaxy S23",
    price: 4299.99,
    old_price: null,
    description:
      "Premium Android smartphone with Snapdragon 8 Gen 2 and excellent camera.",
    categories: [{ id: 2, name: "Smartphones" }],
    tags: [
      { id: 5, name: "samsung" },
      { id: 4, name: "flagship" },
    ],
    photos: [{ path: "phones/galaxy-s23.jpg" }],
  },
  {
    id: 4,
    name: "Sony WH-1000XM5",
    price: 1599.99,
    old_price: 1799.99,
    description:
      "Industry-leading noise cancelling headphones with exceptional sound quality.",
    categories: [{ id: 3, name: "Audio" }],
    tags: [
      { id: 6, name: "headphones" },
      { id: 2, name: "premium" },
    ],
    photos: [{ path: "audio/sony-wh1000xm5.jpg" }],
  },
  {
    id: 5,
    name: 'iPad Pro 12.9"',
    price: 5299.99,
    old_price: null,
    description: "Professional tablet with M2 chip, Liquid Retina XDR display.",
    categories: [{ id: 4, name: "Tablets" }],
    tags: [
      { id: 3, name: "apple" },
      { id: 2, name: "professional" },
    ],
    photos: [{ path: "tablets/ipad-pro.jpg" }],
  },
  {
    id: 6,
    name: "MacBook Air M2",
    price: 6499.99,
    old_price: 6999.99,
    description:
      "Thin and light laptop with Apple M2 chip, all-day battery life.",
    categories: [{ id: 1, name: "Laptops" }],
    tags: [
      { id: 3, name: "apple" },
      { id: 7, name: "ultrabook" },
    ],
    photos: [{ path: "laptops/macbook-air-m2.jpg" }],
  },
  {
    id: 7,
    name: 'LG OLED C3 55"',
    price: 6999.99,
    old_price: 7999.99,
    description: "Premium OLED TV with perfect blacks, HDMI 2.1, and webOS.",
    categories: [{ id: 5, name: "TVs" }],
    tags: [
      { id: 8, name: "oled" },
      { id: 2, name: "premium" },
    ],
    photos: [{ path: "tvs/lg-oled-c3.jpg" }],
  },
  {
    id: 8,
    name: "Nintendo Switch OLED",
    price: 1599.99,
    old_price: null,
    description:
      "Gaming console with OLED screen, perfect for portable gaming.",
    categories: [{ id: 6, name: "Gaming" }],
    tags: [
      { id: 9, name: "console" },
      { id: 10, name: "portable" },
    ],
    photos: [{ path: "gaming/switch-oled.jpg" }],
  },
  {
    id: 9,
    name: "Canon EOS R6",
    price: 12999.99,
    old_price: 13999.99,
    description: "Professional mirrorless camera with 20MP full-frame sensor.",
    categories: [{ id: 7, name: "Cameras" }],
    tags: [
      { id: 11, name: "mirrorless" },
      { id: 2, name: "professional" },
    ],
    photos: [{ path: "cameras/canon-r6.jpg" }],
  },
  {
    id: 10,
    name: "Logitech MX Master 3S",
    price: 449.99,
    old_price: 499.99,
    description:
      "Premium wireless mouse with ultra-fast scrolling and multi-device support.",
    categories: [{ id: 8, name: "Accessories" }],
    tags: [
      { id: 12, name: "mouse" },
      { id: 13, name: "wireless" },
    ],
    photos: [{ path: "accessories/mx-master-3s.jpg" }],
  },
  {
    id: 11,
    name: "Samsung 970 EVO Plus 1TB",
    price: 549.99,
    old_price: null,
    description: "High-performance NVMe SSD with read speeds up to 3,500 MB/s.",
    categories: [{ id: 9, name: "Storage" }],
    tags: [
      { id: 14, name: "ssd" },
      { id: 15, name: "nvme" },
    ],
    photos: [{ path: "storage/970-evo-plus.jpg" }],
  },
  {
    id: 12,
    name: "Corsair K95 RGB",
    price: 799.99,
    old_price: 899.99,
    description:
      "Mechanical gaming keyboard with Cherry MX switches and RGB lighting.",
    categories: [{ id: 8, name: "Accessories" }],
    tags: [
      { id: 16, name: "keyboard" },
      { id: 17, name: "gaming" },
    ],
    photos: [{ path: "accessories/corsair-k95.jpg" }],
  },
  {
    id: 13,
    name: "AirPods Pro 2",
    price: 1099.99,
    old_price: null,
    description:
      "Wireless earbuds with active noise cancellation and spatial audio.",
    categories: [{ id: 3, name: "Audio" }],
    tags: [
      { id: 3, name: "apple" },
      { id: 18, name: "earbuds" },
    ],
    photos: [{ path: "audio/airpods-pro-2.jpg" }],
  },
  {
    id: 14,
    name: "PlayStation 5",
    price: 2499.99,
    old_price: 2699.99,
    description:
      "Next-gen gaming console with ultra-high speed SSD and ray tracing.",
    categories: [{ id: 6, name: "Gaming" }],
    tags: [
      { id: 9, name: "console" },
      { id: 19, name: "playstation" },
    ],
    photos: [{ path: "gaming/ps5.jpg" }],
  },
  {
    id: 15,
    name: "DJI Mini 3 Pro",
    price: 3999.99,
    old_price: 4499.99,
    description: "Compact drone with 4K HDR video and 34-minute flight time.",
    categories: [{ id: 10, name: "Drones" }],
    tags: [
      { id: 20, name: "drone" },
      { id: 21, name: "4k" },
    ],
    photos: [{ path: "drones/dji-mini-3.jpg" }],
  },
  {
    id: 16,
    name: "Apple Watch Series 9",
    price: 1899.99,
    old_price: null,
    description:
      "Smartwatch with advanced health features and bright always-on display.",
    categories: [{ id: 11, name: "Wearables" }],
    tags: [
      { id: 3, name: "apple" },
      { id: 22, name: "smartwatch" },
    ],
    photos: [{ path: "wearables/apple-watch-9.jpg" }],
  },
  {
    id: 17,
    name: "Kindle Paperwhite",
    price: 699.99,
    old_price: 799.99,
    description:
      'E-reader with 6.8" glare-free display and adjustable warm light.',
    categories: [{ id: 12, name: "E-readers" }],
    tags: [
      { id: 23, name: "kindle" },
      { id: 24, name: "reading" },
    ],
    photos: [{ path: "ereaders/kindle-paperwhite.jpg" }],
  },
  {
    id: 18,
    name: "GoPro Hero 11 Black",
    price: 2199.99,
    old_price: 2499.99,
    description: "Action camera with 5.3K video and HyperSmooth stabilization.",
    categories: [{ id: 7, name: "Cameras" }],
    tags: [
      { id: 25, name: "action-camera" },
      { id: 26, name: "waterproof" },
    ],
    photos: [{ path: "cameras/gopro-hero-11.jpg" }],
  },
  {
    id: 19,
    name: "Dyson V15 Detect",
    price: 3299.99,
    old_price: null,
    description: "Cordless vacuum with laser detection and LCD screen.",
    categories: [{ id: 13, name: "Home" }],
    tags: [
      { id: 27, name: "vacuum" },
      { id: 28, name: "cordless" },
    ],
    photos: [{ path: "home/dyson-v15.jpg" }],
  },
  {
    id: 20,
    name: "Razer Blade 15",
    price: 8999.99,
    old_price: 9999.99,
    description: "Gaming laptop with RTX 4070, 240Hz display, and per-key RGB.",
    categories: [{ id: 1, name: "Laptops" }],
    tags: [
      { id: 17, name: "gaming" },
      { id: 29, name: "razer" },
    ],
    photos: [{ path: "laptops/razer-blade-15.jpg" }],
  },
];

// Placeholder image for products without photos
export const PLACEHOLDER_IMAGE =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Crect width='400' height='400' fill='%23f0f0f0'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='24' fill='%23999'%3ENo Image%3C/text%3E%3C/svg%3E";

// Mock API functions
export const mockAPI = {
  getProducts: () => Promise.resolve(mockProducts),

  getRandomProducts: (count = 8) => {
    const shuffled = [...mockProducts].sort(() => 0.5 - Math.random());
    return Promise.resolve(shuffled.slice(0, count));
  },

  searchProducts: (query) => {
    const filtered = mockProducts.filter(
      (product) =>
        product.name.toLowerCase().includes(query.toLowerCase()) ||
        product.description.toLowerCase().includes(query.toLowerCase()),
    );
    return Promise.resolve(filtered);
  },

  getRecommendationSettings: () =>
    Promise.resolve({
      active_algorithm: "random",
      algorithms: ["random", "content_based", "collaborative"],
    }),

  getRecommendationPreview: (algorithm) => {
    // Return random products as recommendations for mock
    return mockAPI.getRandomProducts(8);
  },
};
