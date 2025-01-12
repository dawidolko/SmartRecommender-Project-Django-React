import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ShopContent.scss";
import ShopProduct from "./ShopProduct";

const ShopContent = () => {
  const { category } = useParams(); // Pobiera kategorię z URL
  const [selectedCategory, setSelectedCategory] = useState(category || "all");
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [isLoadingProducts, setIsLoadingProducts] = useState(true);
  const [isLoadingCategories, setIsLoadingCategories] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/categories/");
        const data = await response.json();
        setCategories(["all", ...data.map((cat) => cat.name)]);
        setIsLoadingCategories(false);
      } catch (error) {
        console.error("Error fetching categories:", error);
        setIsLoadingCategories(false);
      }
    };

    const fetchProducts = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/products/");
        const data = await response.json();
        setProducts(data);
        setIsLoadingProducts(false);
      } catch (error) {
        console.error("Error fetching products:", error);
        setIsLoadingProducts(false);
      }
    };

    fetchCategories();
    fetchProducts();
  }, []);

  useEffect(() => {
    if (category) {
      setSelectedCategory(category);
    }
  }, [category]);

  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
    navigate(`/category/${category}`); // Aktualizuje URL
  };

  const filteredProducts =
    selectedCategory === "all"
      ? products
      : products.filter((product) =>
          product.categories.some((cat) => cat === selectedCategory)
        );

  return (
    <div className="shop container">
      <h2 id="category" className="shop__title">
        {selectedCategory !== "all"
          ? `Products in "${selectedCategory}" category`
          : "Our Products"}
      </h2>

      <div className="shop__buttons">
        {isLoadingCategories ? (
          <p>Loading categories...</p>
        ) : (
          categories.map((category) => (
            <button
              key={category}
              onClick={() => handleCategoryClick(category)}
              className={selectedCategory === category ? "shop__active" : ""}>
              {category.toUpperCase()}
            </button>
          ))
        )}
      </div>

      <div className="shop__products">
        {isLoadingProducts ? (
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
