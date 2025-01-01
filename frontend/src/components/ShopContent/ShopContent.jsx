import { useState } from "react";
import "./ShopContent.scss";
import shopData from "./ShopData";
import ShopProduct from "./ShopProduct";

const ShopContent = () => {
  const [selectedCategory, setSelectedCategory] = useState("all");

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

  const filteredProducts =
    selectedCategory === "all"
      ? shopData
      : shopData.filter((product) => product.category === selectedCategory);

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
        {filteredProducts.length > 0 ? (
          filteredProducts.map((product, index) => (
            <ShopProduct key={product.id || index} {...product} />
          ))
        ) : (
          <p>No products available in this category.</p>
        )}
      </div>
    </div>
  );
};

export default ShopContent;
