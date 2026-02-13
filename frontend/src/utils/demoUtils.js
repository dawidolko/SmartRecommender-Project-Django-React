/**
 * GitHub Pages Detection Utility
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2026-02-13
 * Version: 1.0
 *
 * Utility function to consistently detect if the app is running on GitHub Pages
 * or other static hosting environments.
 */

/**
 * Detects if the current environment is GitHub Pages or static hosting
 * @returns {boolean} True if running on GitHub Pages/static hosting
 */
export const isGitHubPages = () => {
  if (typeof window === "undefined") return false;

  return (
    window.location.hostname.includes("github.io") ||
    window.location.hostname.includes("project.dawidolko.pl") ||
    window.location.hostname.includes("githubpages") ||
    window.location.hostname.includes("vercel.app") ||
    window.location.hostname.includes("netlify.app") ||
    (window.location.protocol === "https:" &&
      !window.location.hostname.includes("localhost") &&
      !window.location.hostname.includes("127.0.0.1") &&
      !window.location.hostname.includes("0.0.0.0"))
  );
};

/**
 * Gets appropriate fallback message for demo mode
 * @param {string} feature - Feature name (e.g., "Shop", "Cart")
 * @returns {string} Appropriate demo message
 */
export const getDemoMessage = (feature) => {
  const messages = {
    shop: "The product catalog requires database connectivity to display items, categories, and filtering. This feature is not available in the static demo version.",
    product:
      "Individual product pages require database connectivity to load product details, images, and specifications. This feature is not available in the static demo version.",
    cart: "Shopping cart functionality requires database connectivity to manage items, calculate totals, and process orders. This feature is not available in the static demo version.",
    favorites:
      "Favorites functionality requires database connectivity to save and manage your preferred items. This feature is not available in the static demo version.",
    search:
      "Product search functionality requires database connectivity to query and filter products. This feature is not available in the static demo version.",
    login:
      "User authentication requires backend server connectivity. This feature is not available in the static demo version.",
    contact:
      "Contact form submission requires backend server connectivity. This feature is not available in the static demo version.",
  };

  return (
    messages[feature.toLowerCase()] ||
    `${feature} functionality requires database connectivity and is not available in the static demo version.`
  );
};
