// ShopContent Component - Main shop page with filtering and pagination
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ShopContent.scss";
import ShopProduct from "./ShopProduct";
import config from "../../config/config";
import { mockAPI, PLACEHOLDER_IMAGE } from "../../utils/mockData";
import DemoFallback from "../DemoFallback/DemoFallback";
import { IoHomeOutline } from "react-icons/io5";
import { RiArrowDownSLine, RiArrowUpSLine } from "react-icons/ri";
import {
  FaBox,
  FaTshirt,
  FaLaptop,
  FaGamepad,
  FaTools,
  FaCamera,
  FaBrush,
  FaClock,
  FaBatteryFull,
  FaHdd,
  FaMouse,
  FaDesktop,
  FaPlane,
  FaMicrochip,
  FaSitemap,
  FaCouch,
  FaTv,
} from "react-icons/fa";
import { ChevronLeft, ChevronRight } from "lucide-react";

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
  const [loadingTimeout, setLoadingTimeout] = useState(false);

  const [currentPage, setCurrentPage] = useState(1);
  const [priceRange, setPriceRange] = useState({ min: 0, max: 1000 });
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [productsPerPage] = useState(30);

  useEffect(() => {
    if (category) {
      const parts = category.split(".");
      setSelectedMainCategory(parts[0] || "all");
      setSelectedSubCategory(parts[1] || "all");
    }
  }, [category]);

  const getAvailableBrands = () => {
    if (!products || !Array.isArray(products)) return [];

    const brands = new Set();
    products.forEach((product) => {
      if (product?.tags && Array.isArray(product.tags)) {
        product.tags.forEach((tag) => {
          if (tag && typeof tag === "string") {
            brands.add(tag);
          }
        });
      }
      if (product?.brand) {
        brands.add(product.brand);
      }
      if (product?.name) {
        const nameParts = product.name.split(" ");
        if (nameParts.length > 0 && nameParts[0] && nameParts[0].trim()) {
          brands.add(nameParts[0]);
        }
      }
    });
    return Array.from(brands).sort();
  };

  const resetAllFilters = () => {
    setPriceRange({ min: 0, max: 1000 });
    setSelectedBrands([]);
    setSearchTerm("");
    setSelectedMainCategory("all");
    setSelectedSubCategory("all");
    setCurrentPage(1);
    navigate("/category/all");
  };

  const clearPriceFilter = () => {
    setPriceRange({ min: 0, max: 1000 });
    setCurrentPage(1);
  };

  const handlePriceChange = (type, value) => {
    let numValue;
    if (value === "" || value === null || value === undefined) {
      numValue = type === "min" ? 0 : 1000;
    } else {
      numValue = Math.max(0, Number(value) || 0);
    }

    setPriceRange((prev) => {
      const newRange = { ...prev, [type]: numValue };

      if (type === "min" && newRange.min > newRange.max) {
        newRange.max = newRange.min;
      } else if (type === "max" && newRange.max < newRange.min) {
        newRange.min = newRange.max;
      }

      return newRange;
    });
    setCurrentPage(1);
  };

  const removeBrandFilter = (brand) => {
    setSelectedBrands((prev) => prev.filter((b) => b !== brand));
    setCurrentPage(1);
  };

  const clearSearchFilter = () => {
    setSearchTerm("");
    setCurrentPage(1);
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "Escape" && showFilterModal) {
        setShowFilterModal(false);
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [showFilterModal]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        if (config.useMockData) {
          console.log("ShopContent: Using mock data for categories");
          const data = await mockAPI.getCategories();
          console.log("ShopContent: Mock categories loaded:", data?.length);
          setCategories((data || []).map((cat) => cat.name));
        } else {
          const response = await fetch(`${config.apiUrl}/api/categories/`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          setCategories((data || []).map((cat) => cat.name));
        }
      } catch (error) {
        console.error("Error fetching categories:", error);
        setCategories([]);
      } finally {
        setIsLoadingCategories(false);
      }
    };

    const fetchProducts = async () => {
      try {
        if (config.useMockData) {
          console.log("ShopContent: Using mock data for products");
          const data = await mockAPI.getProducts();
          console.log("ShopContent: Mock products loaded:", data?.length);
          console.log("ShopContent: First product:", data?.[0]);
          setProducts(data || []);
        } else {
          const response = await fetch(`${config.apiUrl}/api/products/`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();
          setProducts(data || []);
        }
      } catch (error) {
        console.error("Error fetching products:", error);
        setProducts([]);
      } finally {
        setIsLoadingProducts(false);
      }
    };

    fetchCategories();
    fetchProducts();

    const timeoutId = setTimeout(() => {
      if (isLoadingProducts || isLoadingCategories) {
        console.log("ShopContent: Loading timeout - showing demo fallback");
        setLoadingTimeout(true);
        setIsLoadingProducts(false);
        setIsLoadingCategories(false);
      }
    }, 8000);

    const handleResize = () => {
      if (window.innerWidth < 868) {
        setIsSidebarOpen(false);
      } else {
        setIsSidebarOpen(true);
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    return () => {
      window.removeEventListener("resize", handleResize);
      clearTimeout(timeoutId);
    };
  }, [isLoadingProducts, isLoadingCategories]);

  useEffect(() => {
    setCurrentPage(1);
  }, [
    selectedMainCategory,
    selectedSubCategory,
    priceRange,
    selectedBrands,
    searchTerm,
  ]);

  const mainCategories = Array.from(
    new Set(
      (categories || [])
        .filter((cat) => cat && typeof cat === "string")
        .map((cat) => cat.split(".")[0]),
    ),
  );

  const subCategories =
    selectedMainCategory !== "all"
      ? (categories || [])
          .filter((cat) => cat && cat.startsWith(selectedMainCategory + "."))
          .map((cat) => cat.split(".")[1])
      : [];

  const filteredProducts = (products || []).filter((product) => {
    if (!product || !product.categories || !Array.isArray(product.categories))
      return false;

    const matchesCategory =
      selectedMainCategory === "all" ||
      product.categories.some((prodCat) => {
        if (!prodCat || typeof prodCat !== "string") return false;
        const [prodMain, prodSub = "all"] = prodCat.split(".");
        return selectedSubCategory === "all"
          ? prodMain === selectedMainCategory
          : prodMain === selectedMainCategory &&
              prodSub === selectedSubCategory;
      });

    const productPrice = parseFloat(product.price || 0);
    const matchesPrice =
      productPrice >= priceRange.min && productPrice <= priceRange.max;

    const matchesBrand =
      selectedBrands.length === 0 ||
      selectedBrands.some((brand) => {
        if (
          product.tags &&
          Array.isArray(product.tags) &&
          product.tags.includes(brand)
        )
          return true;
        if (product.brand === brand) return true;
        if (
          product.name &&
          product.name.toLowerCase().startsWith(brand.toLowerCase())
        )
          return true;
        return false;
      });

    const matchesSearch =
      !searchTerm ||
      (product.name &&
        product.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (product.description &&
        product.description.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (product.tags &&
        Array.isArray(product.tags) &&
        product.tags.some(
          (tag) =>
            tag &&
            typeof tag === "string" &&
            tag.toLowerCase().includes(searchTerm.toLowerCase()),
        ));

    return matchesCategory && matchesPrice && matchesBrand && matchesSearch;
  });

  console.log("ShopContent - Debug:", {
    totalProducts: products.length,
    filteredCount: filteredProducts.length,
    currentProductsCount: filteredProducts.slice(
      indexOfFirstProduct,
      indexOfLastProduct,
    ).length,
    selectedMainCategory,
    isLoadingProducts,
    config: config.useMockData,
  });

  const totalProducts = filteredProducts.length;
  const totalPages = Math.ceil(totalProducts / productsPerPage);
  const indexOfLastProduct = currentPage * productsPerPage;
  const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
  const currentProducts = filteredProducts.slice(
    indexOfFirstProduct,
    indexOfLastProduct,
  );

  const getCategoryIcon = (categoryName) => {
    const name = categoryName.toLowerCase();

    if (name === "accessories") return <FaTshirt />;
    if (name === "camera" || name === "cameras") return <FaCamera />;
    if (name === "cleaning") return <FaBrush />;
    if (name === "components") return <FaMicrochip />;
    if (name === "computers") return <FaDesktop />;
    if (name === "drones") return <FaPlane />;
    if (name === "electronics") return <FaTv />;
    if (name === "furniture") return <FaCouch />;
    if (name === "gadgets") return <FaTools />;
    if (name === "gaming") return <FaGamepad />;
    if (name === "laptop" || name === "laptops") return <FaLaptop />;
    if (name === "monitoring") return <FaTv />;
    if (name === "mounts") return <FaTools />;
    if (name === "networking") return <FaSitemap />;
    if (name === "office") return <FaDesktop />;
    if (name === "peripherals") return <FaMouse />;
    if (name === "power") return <FaBatteryFull />;
    if (name === "storage") return <FaHdd />;
    if (name === "vacuum") return <FaBrush />;
    if (name === "wearables") return <FaClock />;

    return <FaBox />;
  };

  const toggleSubCategories = (category) => {
    setExpandedCategories((prev) =>
      prev.includes(category)
        ? prev.filter((cat) => cat !== category)
        : [...prev, category],
    );
  };

  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const renderPaginationButtons = () => {
    const buttons = [];
    const maxVisiblePages = 5;

    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      buttons.push(
        <button
          key={i}
          className={`pagination-number ${currentPage === i ? "active" : ""}`}
          onClick={() => handlePageChange(i)}>
          {i}
        </button>,
      );
    }

    return buttons;
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
                        <span className="shop__sidebar-category-icon">
                          {getCategoryIcon(mainCat)}
                        </span>
                        <span className="shop__sidebar-name">
                          {mainCat.toUpperCase()}
                        </span>
                      </button>

                      {categories.some((cat) =>
                        cat.startsWith(mainCat + "."),
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

            <button
              className="shop__filter-toggle"
              onClick={() => setShowFilterModal(true)}>
              Filtry i wyszukiwanie
            </button>

            <div className="shop__filter-tags">
              {searchTerm && (
                <div className="shop__filter-tag">
                  <span>Szukaj: "{searchTerm}"</span>
                  <button onClick={clearSearchFilter}>×</button>
                </div>
              )}
              {(priceRange.min > 0 || priceRange.max < 1000) && (
                <div className="shop__filter-tag">
                  <span>
                    Cena: ${priceRange.min}-${priceRange.max}
                  </span>
                  <button onClick={clearPriceFilter}>×</button>
                </div>
              )}
              {selectedBrands.map((brand) => (
                <div key={brand} className="shop__filter-tag">
                  <span>Marka: {brand}</span>
                  <button onClick={() => removeBrandFilter(brand)}>×</button>
                </div>
              ))}

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
            ) : currentProducts.length > 0 ? (
              currentProducts.map((product) => (
                <ShopProduct
                  key={product.id}
                  id={product.id}
                  name={product.name || "Product name unavailable"}
                  price={product.price || 0}
                  old_price={product.old_price}
                  imgs={
                    config.useMockData
                      ? [PLACEHOLDER_IMAGE]
                      : product.photos &&
                          Array.isArray(product.photos) &&
                          product.photos.length > 0
                        ? product.photos.map(
                            (photo) => `${config.apiUrl}/media/${photo.path}`,
                          )
                        : [PLACEHOLDER_IMAGE]
                  }
                  category={
                    product.categories &&
                    Array.isArray(product.categories) &&
                    product.categories.length > 0
                      ? product.categories[0]
                      : "N/A"
                  }
                />
              ))
            ) : (
              (() => {
                if (
                  (!isLoadingProducts && products.length === 0) ||
                  loadingTimeout
                ) {
                  const isGitHubPages =
                    typeof window !== "undefined" &&
                    (window.location.hostname.includes("github.io") ||
                      window.location.hostname.includes(
                        "project.dawidolko.pl",
                      ) ||
                      (!window.location.hostname.includes("localhost") &&
                        !window.location.hostname.includes("127.0.0.1")));

                  if (isGitHubPages) {
                    return (
                      <DemoFallback
                        title="Shop - Demo Mode"
                        message="The product catalog requires database connectivity to display items, categories, and filtering. This feature is not available in the static demo version."
                        showBackButton={false}
                      />
                    );
                  }
                }
                return (
                  <p className="shop__no-products">
                    Brak produktów w tej kategorii.
                  </p>
                );
              })()
            )}
          </div>

          {totalPages > 1 && (
            <div className="pagination-container">
              <div className="pagination-info">
                <p className="pagination-text">
                  Wyświetlanie {indexOfFirstProduct + 1} do{" "}
                  {Math.min(indexOfLastProduct, totalProducts)} z{" "}
                  {totalProducts} produktów
                </p>
              </div>
              <div className="pagination-controls">
                <button
                  className={`pagination-button ${
                    currentPage === 1 ? "disabled" : ""
                  }`}
                  onClick={() => handlePageChange(currentPage - 1)}
                  disabled={currentPage === 1}>
                  <ChevronLeft size={16} />
                  <span>&lt;</span>
                </button>

                {renderPaginationButtons()}

                <button
                  className={`pagination-button ${
                    currentPage === totalPages ? "disabled" : ""
                  }`}
                  onClick={() => handlePageChange(currentPage + 1)}
                  disabled={currentPage === totalPages}>
                  <ChevronRight size={16} />
                  <span>&gt;</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {showFilterModal && (
        <div
          className="shop__modal-overlay"
          onClick={() => setShowFilterModal(false)}>
          <div className="shop__modal" onClick={(e) => e.stopPropagation()}>
            <div className="shop__modal-header">
              <h3>Filtry produktów</h3>
              <button
                className="common-modal-close search-modal-close"
                onClick={() => setShowFilterModal(false)}
                aria-label="Close Filter Modal">
                ×
              </button>
            </div>
            <div className="shop__modal-content">
              <div className="shop__filter-section">
                <label htmlFor="modal-search-input">Szukaj produkty:</label>
                <input
                  id="modal-search-input"
                  type="text"
                  placeholder="Wpisz nazwę produktu lub tag..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="shop__filter-input"
                />
              </div>
              <div className="shop__filter-section">
                <label>Zakres cen ($):</label>
                <div className="shop__price-filter">
                  <input
                    type="number"
                    placeholder="Od"
                    min="0"
                    max="10000"
                    step="1"
                    value={priceRange.min === 0 ? "" : priceRange.min}
                    onChange={(e) => handlePriceChange("min", e.target.value)}
                    className="shop__filter-input shop__price-input"
                  />
                  <span className="shop__price-separator">-</span>
                  <input
                    type="number"
                    placeholder="Do"
                    min="0"
                    max="10000"
                    step="1"
                    value={priceRange.max === 1000 ? "" : priceRange.max}
                    onChange={(e) => handlePriceChange("max", e.target.value)}
                    className="shop__filter-input shop__price-input"
                  />
                </div>
              </div>
              {getAvailableBrands().length > 0 && (
                <div className="shop__filter-section">
                  <label>Marki i tagi:</label>
                  <div className="shop__brand-filter">
                    {getAvailableBrands()
                      .slice(0, 15)
                      .map((brand) => (
                        <label key={brand} className="shop__brand-checkbox">
                          <input
                            type="checkbox"
                            checked={selectedBrands.includes(brand)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedBrands((prev) => [...prev, brand]);
                              } else {
                                setSelectedBrands((prev) =>
                                  prev.filter((b) => b !== brand),
                                );
                              }
                            }}
                          />
                          <span>{brand}</span>
                        </label>
                      ))}
                  </div>
                </div>
              )}
            </div>
            <div className="shop__modal-footer">
              <button
                className="shop__reset-filters-btn"
                onClick={resetAllFilters}>
                Resetuj filtry
              </button>
              <button
                className="shop__apply-filters-btn"
                onClick={() => setShowFilterModal(false)}>
                Zastosuj filtry
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ShopContent;
