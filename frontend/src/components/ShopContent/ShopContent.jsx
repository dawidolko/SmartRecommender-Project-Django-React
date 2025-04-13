import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ShopContent.scss";
import ShopProduct from "./ShopProduct";
import config from "../../config/config";

const ShopContent = () => {
  const { category } = useParams();
  const navigate = useNavigate();

  const [selectedMainCategory, setSelectedMainCategory] = useState("all");
  const [selectedSubCategory, setSelectedSubCategory] = useState("all");
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Do kontrolowania stanu sidebaru (otwarty/zwiń)
  const [isLoadingProducts, setIsLoadingProducts] = useState(true);
  const [isLoadingCategories, setIsLoadingCategories] = useState(true);
  const [expandedCategories, setExpandedCategories] = useState([]); // Nowy stan do zarządzania rozwinięciem kategorii

  useEffect(() => {
    if (category) {
      const parts = category.split(".");
      setSelectedMainCategory(parts[0] || "all");
      setSelectedSubCategory(parts[1] || "all");
    }
  }, [category]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch(`${config.apiUrl}/api/categories/`);
        const data = await response.json();
        setCategories(data.map((cat) => cat.name));
        setIsLoadingCategories(false);
      } catch (error) {
        console.error("Error fetching categories:", error);
        setIsLoadingCategories(false);
      }
    };

    const fetchProducts = async () => {
      try {
        const response = await fetch(`${config.apiUrl}/api/products/`);
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

  const mainCategories = Array.from(
    new Set(categories.map((cat) => cat.split(".")[0]))
  );
  const subCategories =
    selectedMainCategory !== "all"
      ? categories
          .filter((cat) => cat.startsWith(selectedMainCategory + "."))
          .map((cat) => cat.split(".")[1])
      : [];

  const filteredProducts = products.filter((product) => {
    const matchesCategory =
      selectedMainCategory === "all" ||
      product.categories.some((prodCat) => {
        const [prodMain, prodSub = "all"] = prodCat.split(".");
        return selectedSubCategory === "all"
          ? prodMain === selectedMainCategory
          : prodMain === selectedMainCategory &&
              prodSub === selectedSubCategory;
      });

    return matchesCategory;
  });

  const toggleSubCategories = (category) => {
    setExpandedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((cat) => cat !== category)
        : [...prev, category]
    );
  };

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <div className="shop container">
      <h2 className="shop__title">
        {selectedMainCategory === "all"
          ? "Our Products"
          : `Products in "${selectedMainCategory.toUpperCase()}" category`}
      </h2>

      <div className="shop__container__main">
        <button className="hamburger-icon" onClick={toggleSidebar}>
          {isSidebarOpen ? "☰" : "X"}
        </button>
        <div
          style={{
            position: "fixed",
            display: isSidebarOpen ? "none" : "flex",
            top: 110,
            left: 0,
            bottom: 0,
            color: "#d5d5d5",
            border: "1px solid black",
            backgroundColor: "white",
            width: "250px",
            zIndex: 100,
            flexDirection: "column",
            height: "100%",
            paddingBottom: "50px",
          }}>
          {isLoadingCategories ? (
            <div className="loading-spinner"></div>
          ) : (
            <div className="shop__main-categories">
              <button
                onClick={() => {
                  setSelectedMainCategory("all");
                  setSelectedSubCategory("all");
                  navigate(`/category/all`);
                }}
                className={
                  selectedMainCategory === "all" ? "shop__active" : ""
                }>
                ALL PRODUCTS
              </button>
              {mainCategories.map((mainCat) => (
                <div
                  key={mainCat}
                  className={`shop__category ${
                    expandedCategories.includes(mainCat) ? "expanded" : ""
                  }`}>
                  <button
                    onClick={() => {
                      setSelectedMainCategory(mainCat);
                      setSelectedSubCategory("all");
                      navigate(`/category/${mainCat}`);
                    }}
                    className={
                      selectedMainCategory === mainCat ? "shop__active" : ""
                    }>
                    {mainCat.toUpperCase()}
                  </button>
                  {selectedMainCategory === mainCat &&
                    subCategories.length > 0 && (
                      <div className="shop__sub-categories">
                        {subCategories.map((subCat) => (
                          <button
                            key={subCat}
                            onClick={() => {
                              setSelectedSubCategory(subCat);
                              navigate(`/category/${mainCat}.${subCat}`);
                            }}
                            className={
                              selectedSubCategory === subCat
                                ? "shop__active"
                                : ""
                            }>
                            {subCat.toUpperCase()}
                          </button>
                        ))}
                      </div>
                    )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Products section */}
        <div className="shop__products">
          <h1 className="shop__title">Filter by category and subcategory:</h1>
          {isLoadingProducts ? (
            <div className="loading-spinner"></div>
          ) : filteredProducts.length > 0 ? (
            filteredProducts.map((product) => (
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
            <p>No products available in this category.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ShopContent;
