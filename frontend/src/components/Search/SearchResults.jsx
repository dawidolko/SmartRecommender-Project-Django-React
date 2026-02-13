/**
 * SearchResults Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Displays search results for product queries entered by users in the search bar.
 * Fetches filtered products from backend API based on search query parameter.
 *
 * Features:
 *   - Real-time product search via API
 *   - Loading state during data fetch
 *   - Empty state when no results found
 *   - Reuses ShopProduct component for consistent UI
 *   - URL-based search query (deep linking support)
 *
 * Search Algorithm (Backend):
 *   - Searches in product names and descriptions
 *   - Case-insensitive matching
 *   - Returns partial matches
 *
 * API Endpoint:
 *   - GET /api/products/search/?q={query}
 *
 * URL Format:
 *   - /search/:query (e.g., /search/laptop)
 *
 * State Management:
 *   - products: Array of matching products from API
 *   - isLoading: Loading state for async fetch
 *   - query: Search query from URL params
 *
 * @component
 * @returns {React.ReactElement} Search results page with product grid
 */
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../ShopContent/ShopContent.scss";
import ShopProduct from "../ShopContent/ShopProduct";
import config from "../../config/config";
import { mockAPI } from "../../utils/mockData";
import DemoFallback from "../DemoFallback/DemoFallback";

const SearchResults = () => {
  const { query } = useParams();
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        if (config.useMockData) {
          const data = await mockAPI.searchProducts(query);
          setProducts(data);
        } else {
          const response = await fetch(
            `${config.apiUrl}/api/products/search/?q=${query}`,
          );
          const data = await response.json();
          setProducts(data);
        }
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching search results:", error);
        setIsLoading(false);
      }
    };

    fetchProducts();
  }, [query]);

  return (
    <div className="shop container">
      <h2 className="shop__title">Search Results for "{query}"</h2>

      <div className="shop__products">
        {isLoading ? (
          <div className="loading-spinner"></div>
        ) : products.length > 0 ? (
          products.map((product) => (
            <ShopProduct
              key={product.id}
              id={product.id}
              name={product.name}
              price={product.price}
              old_price={product.old_price}
              imgs={product.photos.map(
                (photo) => `${config.apiUrl}/media/${photo.path}`,
              )}
              category={product.categories[0] || "N/A"}
            />
          ))
        ) : (
          (() => {
            // Check if on GitHub Pages
            const isGitHubPages =
              typeof window !== "undefined" &&
              (window.location.hostname.includes("github.io") ||
                window.location.hostname.includes("project.dawidolko.pl") ||
                (!window.location.hostname.includes("localhost") &&
                  !window.location.hostname.includes("127.0.0.1")));

            if (isGitHubPages) {
              return (
                <DemoFallback
                  title="Search Results - Demo Mode"
                  message="Product search functionality requires database connectivity to query and filter products. This feature is not available in the static demo version."
                />
              );
            }

            return <p>No products match your search.</p>;
          })()
        )}
      </div>
    </div>
  );
};

export default SearchResults;
