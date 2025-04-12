import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "../ShopContent/ShopContent.scss";
import ShopProduct from "../ShopContent/ShopProduct";
import config from "../../config/config";

const SearchResults = () => {
  const { query } = useParams();
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch(
          `${config.apiUrl}/api/products/search/?q=${query}`
        );
        const data = await response.json();
        setProducts(data);
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
          <p>Loading products...</p>
        ) : products.length > 0 ? (
          products.map((product) => (
            <ShopProduct
              key={product.id}
              id={product.id}
              name={product.name}
              price={product.price}
              old_price={product.old_price}
              imgs={product.photos.map(
                (photo) => `${config.apiUrl}/media/${photo.path}`
              )}
              category={product.categories[0] || "N/A"}
            />
          ))
        ) : (
          <p>No products match your search.</p>
        )}
      </div>
    </div>
  );
};

export default SearchResults;
