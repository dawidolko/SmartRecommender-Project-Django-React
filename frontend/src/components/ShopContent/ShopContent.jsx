import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ShopContent.scss";
import ShopProduct from "./ShopProduct";
import config from "../../config/config";
import { IoHomeOutline } from "react-icons/io5";
import { RiArrowDownSLine, RiArrowUpSLine } from "react-icons/ri";

const ShopContent = () => {
  const { category } = useParams();
  const navigate = useNavigate();

  const [selectedMainCategory, setSelectedMainCategory] = useState("all");
  const [selectedSubCategory, setSelectedSubCategory] = useState("all");
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isLoadingProducts, setIsLoadingProducts] = useState(true);
  const [isLoadingCategories, setIsLoadingCategories] = useState(true);
  const [expandedCategories, setExpandedCategories] = useState([]);

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

    const handleResize = () => {
      if (window.innerWidth < 868) {
        setIsSidebarOpen(false);
      } else {
        setIsSidebarOpen(true);
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    return () => window.removeEventListener("resize", handleResize);
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
          ? "Nasze Produkty"
          : `Produkty w kategorii "${selectedMainCategory.toUpperCase()}"`}
      </h2>

      <div className="shop__container__main">
        <button
          className={`hamburger-icon ${isSidebarOpen ? "active" : ""}`}
          onClick={toggleSidebar}
          aria-label="Toggle sidebar">
          <span></span>
          <span></span>
          <span></span>
        </button>

        <aside className={`shop__sidebar ${isSidebarOpen ? "open" : "closed"}`}>
          {isLoadingCategories ? (
            <div className="shop__loading-spinner"></div>
          ) : (
            <div className="shop__sidebar-content">
              <div className="shop__sidebar-item">
                <button
                  onClick={() => {
                    setSelectedMainCategory("all");
                    setSelectedSubCategory("all");
                    navigate(`/category/all`);
                  }}
                  className={`shop__sidebar-button ${
                    selectedMainCategory === "all" ? "active" : ""
                  }`}>
                  <IoHomeOutline className="shop__sidebar-icon" />
                  <span className="shop__sidebar-name">ALL PRODUCTS</span>
                </button>
              </div>

              {mainCategories.map((mainCat) => {
                const isExpanded =
                  selectedMainCategory === mainCat ||
                  expandedCategories.includes(mainCat);
                const hasSubCategories =
                  subCategories.length > 0 && selectedMainCategory === mainCat;

                return (
                  <div className="shop__sidebar-item" key={mainCat}>
                    <div className="shop__sidebar-main-category">
                      <button
                        onClick={() => {
                          setSelectedMainCategory(mainCat);
                          setSelectedSubCategory("all");
                          navigate(`/category/${mainCat}`);
                        }}
                        className={`shop__sidebar-button ${
                          selectedMainCategory === mainCat ? "active" : ""
                        }`}>
                        <span className="shop__sidebar-dot"></span>
                        <span className="shop__sidebar-name">
                          {mainCat.toUpperCase()}
                        </span>
                      </button>

                      {categories.some((cat) =>
                        cat.startsWith(mainCat + ".")
                      ) && (
                        <button
                          className="shop__sidebar-toggle"
                          onClick={() => toggleSubCategories(mainCat)}>
                          {isExpanded ? (
                            <RiArrowUpSLine />
                          ) : (
                            <RiArrowDownSLine />
                          )}
                        </button>
                      )}
                    </div>

                    {hasSubCategories && isExpanded && (
                      <div className="shop__sidebar-subcategories">
                        {subCategories.map((subCat) => (
                          <button
                            key={subCat}
                            onClick={() => {
                              setSelectedSubCategory(subCat);
                              navigate(`/category/${mainCat}.${subCat}`);
                            }}
                            className={`shop__sidebar-subbutton ${
                              selectedSubCategory === subCat ? "active" : ""
                            }`}>
                            <span className="shop__sidebar-subdot"></span>
                            <span>{subCat.toUpperCase()}</span>
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </aside>

        <div className="shop__products-container">
          <div className="shop__products-header">
            <h3 className="shop__products-title">Filtry:</h3>
            <div className="shop__filter-tags">
              {selectedMainCategory !== "all" && (
                <div className="shop__filter-tag">
                  <span>{selectedMainCategory.toUpperCase()}</span>
                  <button
                    onClick={() => {
                      setSelectedMainCategory("all");
                      setSelectedSubCategory("all");
                      navigate(`/category/all`);
                    }}>
                    ×
                  </button>
                </div>
              )}
              {selectedSubCategory !== "all" && (
                <div className="shop__filter-tag">
                  <span>{selectedSubCategory.toUpperCase()}</span>
                  <button
                    onClick={() => {
                      setSelectedSubCategory("all");
                      navigate(`/category/${selectedMainCategory}`);
                    }}>
                    ×
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="shop__products">
            {isLoadingProducts ? (
              <div className="shop__loading-spinner"></div>
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
              <p className="shop__no-products">
                Brak produktów w tej kategorii.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShopContent;
