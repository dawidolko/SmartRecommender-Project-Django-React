import { useState, useEffect } from "react";
import "./ShopContent.scss";
import ShopProduct from "./ShopProduct";

const ShopContent = () => {
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const categories = [
    "all",
    "peripherals.printers",
    "components.powerSupply",
    "peripherals.mousePads",
    "laptops.learning",
    "networking.networkCards",
    "storage.usbFlashDrives",
    "components.fans",
    "laptops.gaming",
  ];

  useEffect(() => {
    fetch("http://localhost:8000/api/random-products/")
      .then((response) => response.json())
      .then((data) => {
        setProducts(data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
        setIsLoading(false);
      });
  }, []);

  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
  };

  const filteredProducts =
    selectedCategory === "all"
      ? products
      : products.filter((product) =>
          product.categories.includes(selectedCategory)
        );

  return (
    <div className="shop container">
      <h2 id="category" className="shop__title">
        Our Products
      </h2>

      <div className="shop__buttons">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => handleCategoryClick(category)}
            className={selectedCategory === category ? "shop__active" : ""}>
            {category.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="shop__products">
        {isLoading ? (
          <p>Loading products...</p>
        ) : filteredProducts.length > 0 ? (
          filteredProducts.map((product) => (
            <ShopProduct
              key={product.id}
              id={product.id}
              name={product.name}
              price={product.price}
              old_price={product.old_price}
              imgs={product.photos.map(
                (photo) => `http://localhost:8000/media/${photo.path}`
              )}
              category={product.categories[0] || "N/A"}
            />
          ))
        ) : (
          <p>No products available in this category.</p>
        )}
      </div>
    </div>
  );
};

export default ShopContent;
