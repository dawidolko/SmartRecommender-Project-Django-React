import { useState } from "react";
import "./ShopContent.scss";
import shopData from "./ShopData";
import ShopProduct from "./ShopProduct";

const ShopContent = () => {
  // Set default category to 'all' to ensure products show by default
  const [selectedCategory, setSelectedCategory] = useState("all");

  // Updated categories array with lowercase for internal logic
  const categories = [
    "all",
    "computer",
    "laptop",
    "case",
    "cooler",
    "disk",
    "fan",
    "gpu",
    "processor",
    "motherboard",
    "ram",
    "powersupply",
  ];

  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
  };

  // Filter products by selected category
  const filteredProducts =
    selectedCategory === "all"
      ? shopData
      : shopData.filter((product) => product.category === selectedCategory);

  return (
    <div className="shop container">
      <h2 className="shop__title">Our Products</h2>

      <div className="shop__buttons">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => handleCategoryClick(category)}
            className={selectedCategory === category ? "shop__active" : ""}>
            {category.toUpperCase()} {/* Display category names in uppercase */}
          </button>
        ))}
      </div>

      <div className="shop__products">
        {filteredProducts.length > 0 ? (
          filteredProducts.map((product) => (
            <ShopProduct key={product.id} {...product} />
          ))
        ) : (
          <p>No products available in this category.</p>
        )}
      </div>
    </div>
  );
};

export default ShopContent;
