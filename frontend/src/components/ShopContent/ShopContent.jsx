import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ShopContent.scss";
import ShopProduct from "./ShopProduct";

const ShopContent = () => {
  const { category } = useParams();
  const navigate = useNavigate();

  const [selectedMainCategory, setSelectedMainCategory] = useState("all");
  const [selectedSubCategory, setSelectedSubCategory] = useState("all");
  const [selectedTag, setSelectedTag] = useState(null);

  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [tags, setTags] = useState([]);

  const [isLoadingProducts, setIsLoadingProducts] = useState(true);
  const [isLoadingCategories, setIsLoadingCategories] = useState(true);
  const [isLoadingTags, setIsLoadingTags] = useState(true);

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
        const response = await fetch("http://localhost:8000/api/categories/");
        const data = await response.json();
        setCategories(data.map((cat) => cat.name));
        setIsLoadingCategories(false);
      } catch (error) {
        console.error("Error fetching categories:", error);
        setIsLoadingCategories(false);
      }
    };

    const fetchTags = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/tags/");
        const data = await response.json();
        setTags(data);
        setIsLoadingTags(false);
      } catch (error) {
        console.error("Error fetching tags:", error);
        setIsLoadingTags(false);
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
    fetchTags();
    fetchProducts();
  }, []);

  const mainCategories = Array.from(new Set(categories.map((cat) => cat.split(".")[0])));
  const subCategories =
    selectedMainCategory !== "all"
      ? categories
          .filter((cat) => cat.startsWith(selectedMainCategory + "."))
          .map((cat) => cat.split(".")[1])
      : [];

  // Product filtering - we take into account the category and the selected tag
  const filteredProducts = products.filter((product) => {
    const matchesCategory =
      selectedMainCategory === "all" ||
      product.categories.some((prodCat) => {
        const [prodMain, prodSub = "all"] = prodCat.split(".");
        return selectedSubCategory === "all"
          ? prodMain === selectedMainCategory
          : prodMain === selectedMainCategory && prodSub === selectedSubCategory;
      });

    const matchesTag = !selectedTag || product.tags.includes(selectedTag);

    return matchesCategory && matchesTag;
  });

  return (
    <div className="shop container">
      <h2 className="shop__title">
        {selectedMainCategory === "all"
          ? "Our Products"
          : `Products in "${selectedMainCategory.toUpperCase()}" category`}
      </h2>

      <div className="shop__buttons">
        {isLoadingCategories ? (
          <p>Loading categories...</p>
        ) : (
          <>
            <div className="shop__main-categories">
              <p>Filter by category and subcategory:</p>
              <button
                onClick={() => {
                  setSelectedMainCategory("all");
                  setSelectedSubCategory("all");
                  navigate(`/category/all`);
                }}
                className={selectedMainCategory === "all" ? "shop__active" : ""}
              >
                ALL PRODUCTS
              </button>
              {mainCategories.map((mainCat) => (
                <button
                  key={mainCat}
                  onClick={() => {
                    setSelectedMainCategory(mainCat);
                    setSelectedSubCategory("all");
                    navigate(`/category/${mainCat}`);
                  }}
                  className={selectedMainCategory === mainCat ? "shop__active" : ""}
                >
                  {mainCat.toUpperCase()}
                </button>
              ))}
            </div>

            {selectedMainCategory !== "all" && subCategories.length > 0 && (
              <div className="shop__sub-categories">
                <button
                  onClick={() => {
                    setSelectedSubCategory("all");
                    navigate(`/category/${selectedMainCategory}`);
                  }}
                  className={selectedSubCategory === "all" ? "shop__active" : ""}
                >
                  ALL PRODUCTS
                </button>
                {subCategories.map((subCat) => (
                  <button
                    key={subCat}
                    onClick={() => {
                      setSelectedSubCategory(subCat);
                      navigate(`/category/${selectedMainCategory}.${subCat}`);
                    }}
                    className={selectedSubCategory === subCat ? "shop__active" : ""}
                  >
                    {subCat.toUpperCase()}
                  </button>
                ))}
              </div>
            )}

            {!isLoadingTags && tags.length > 0 && (
              <div className="shop__tags">
                <p>Filter by tag:</p>
                <button
                  onClick={() => setSelectedTag(null)}
                  className={!selectedTag ? "shop__active" : ""}
                >
                  ALL TAGS
                </button>
                {tags.map((tag) => (
                  <button
                    key={tag.id}
                    onClick={() => setSelectedTag(tag.name)}
                    className={selectedTag === tag.name ? "shop__active" : ""}
                  >
                    {tag.name.toUpperCase()}
                  </button>
                ))}
              </div>
            )}
          </>
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
          <p>No products available in this category or tag.</p>
        )}
      </div>
    </div>
  );
};

export default ShopContent;
