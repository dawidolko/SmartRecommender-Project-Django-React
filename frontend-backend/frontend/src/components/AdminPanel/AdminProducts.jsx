import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Edit, Trash2, Search, Package, DollarSign, TrendingUp, ChevronUp, ChevronDown, ChevronLeft, ChevronRight } from "lucide-react";
import Header from "./AdminHeader";
import StatCard from "./StatCard";
import SalesTrendChart from "./SalesTrendChart";
import CategoryDistributionChart from "./CategoryDistributionChart";
import "./AdminPanel.scss";

const AdminProducts = () => {
  const [products, setProducts] = useState([]);
  const [stats, setStats] = useState({
    totalProducts: 0,
    totalSales: 0,
    topSelling: 0,
    lowStock: 0,
    trend: { labels: [], data: [] },
    category_distribution: { labels: [], data: [] },
  });
  
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [oldPrice, setOldPrice] = useState("");
  const [description, setDescription] = useState("");
  const [tags, setTags] = useState([]);
  const [category, setCategory] = useState("");
  const [photos, setPhotos] = useState([]);
  
  const [availableTags, setAvailableTags] = useState([]);
  const [availableCategories, setAvailableCategories] = useState([]);
  
  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editPrice, setEditPrice] = useState("");
  const [editOldPrice, setEditOldPrice] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [editTags, setEditTags] = useState([]);
  const [editCategory, setEditCategory] = useState("");
  const [editPhotos, setEditPhotos] = useState([]);
  
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [productsPerPage] = useState(10);
  const [sortField, setSortField] = useState("name");
  const [sortDirection, setSortDirection] = useState("asc");

  useEffect(() => {
    fetchProducts();
    fetchStats();
  }, []);

  useEffect(() => {
    const filtered = products.filter(
      (product) =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (product.description &&
          product.description.toLowerCase().includes(searchTerm.toLowerCase()))
    );
    const sorted = [...filtered].sort((a, b) => {
      if (sortField === "name") {
        return sortDirection === "asc"
          ? a.name.localeCompare(b.name)
          : b.name.localeCompare(a.name);
      } else if (sortField === "price") {
        return sortDirection === "asc"
          ? parseFloat(a.price) - parseFloat(b.price)
          : parseFloat(b.price) - parseFloat(a.price);
      }
      return 0;
    });
    setFilteredProducts(sorted);
  }, [searchTerm, products, sortField, sortDirection]);

  const fetchProducts = () => {
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/products/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setProducts(res.data))
      .catch((err) => console.error("Error fetching products:", err));
  };

  useEffect(() => {
    fetchTags();
    fetchCategories();
    if (editId) {
      fetchProduct(editId);
    }
  }, [editId]);

  const fetchTags = async () => {
    const token = localStorage.getItem("access");
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/tags/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAvailableTags(response.data);
    } catch (error) {
      console.error("Error fetching tags:", error);
    }
  };

  const fetchCategories = async () => {
    const token = localStorage.getItem("access");
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/categories/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAvailableCategories(response.data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  const fetchProduct = async (id) => {
    const token = localStorage.getItem("access");
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/products/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEditName(response.data.name);
      setEditPrice(response.data.price);
      setEditOldPrice(response.data.old_price || "");
      setEditDescription(response.data.description || "");
      setEditTags(response.data.tags || []);
      setEditCategory(response.data.categories && response.data.categories.length > 0 ? response.data.categories[0] : "");
      setEditPhotos(response.data.photos || []);
    } catch (error) {
      console.error("Error fetching product:", error);
    }
  };

  const fetchStats = () => {
    const token = localStorage.getItem("access");
    axios
      .get("http://127.0.0.1:8000/api/admin-dashboard-stats/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setStats({
          totalProducts: res.data.totalProducts || 0,
          totalSales: res.data.totalSales || 0,
          topSelling: res.data.topSelling || 0,
          trend: res.data.trend || { labels: [], data: [] },
          category_distribution: res.data.category_distribution || { labels: [], data: [] },
        });
      })
      .catch((err) => {
        console.error("Error fetching stats:", err);
        setStats({
          totalProducts: 0,
          totalSales: 0,
          topSelling: 0,
          trend: { labels: [], data: [] },
          category_distribution: { labels: [], data: [] },
        });
      });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("access");
    const productData = {
      name,
      price,
      old_price: oldPrice,
      description,
      tags,
      categories: category ? [category] : [],
      photos,
    };
    try {
      if (!editId) {
        await axios.post(
          "http://127.0.0.1:8000/api/products/",
          productData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
      }
      clearForm();
      fetchProducts();
      fetchStats();
    } catch (error) {
      console.error("Error submitting product:", error);
    }
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    if (!editName || !editPrice || isNaN(editPrice)) {
      alert("Please fill in all required fields correctly.");
      return;
    }
    const token = localStorage.getItem("access");
    const productData = {
      name: editName,
      price: editPrice,
      old_price: editOldPrice || null,
      description: editDescription || null,
      tags: editTags || [],
      categories: editCategory ? [editCategory] : [],
      photos: editPhotos || [],
    };
    try {
      await axios.put(
        `http://127.0.0.1:8000/api/products/${editId}/`,
        productData,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setEditId(null);
      setEditName("");
      setEditPrice("");
      setEditOldPrice("");
      setEditDescription("");
      setEditTags([]);
      setEditCategory("");
      setEditPhotos([]);
      fetchProducts();
      fetchStats();
    } catch (error) {
      console.error("Error editing product:", error);
      if (error.response) {
        console.error("Response error data:", error.response.data);
        alert("Error: " + error.response.data.detail || "Unknown error");
      } else {
        alert("Unknown error occurred.");
      }
    }
  };

  const clearForm = () => {
    setName("");
    setPrice("");
    setOldPrice("");
    setDescription("");
    setTags([]);
    setCategory("");
    setPhotos([]);
  };

  const handleDelete = async (productId) => {
    if (!window.confirm("Czy na pewno chcesz usunąć ten produkt?")) return;
    const token = localStorage.getItem("access");
    try {
      await axios.delete(`http://127.0.0.1:8000/api/products/${productId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProducts((prev) => prev.filter((p) => p.id !== productId));
      fetchStats();
    } catch (error) {
      console.error("Error deleting product:", error);
    }
  };

  const startEdit = (prod) => {
    setEditId(prod.id);
    fetchProduct(prod.id);
  };

  const cancelEdit = () => {
    setEditId(null);
    setEditName("");
    setEditPrice("");
    setEditOldPrice("");
    setEditDescription("");
    setEditTags([]);
    setEditCategory("");
    setEditPhotos([]);
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const indexOfLastProduct = currentPage * productsPerPage;
  const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
  const currentProducts = filteredProducts.slice(indexOfFirstProduct, indexOfLastProduct);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);
  const nextPage = () => {
    if (currentPage < Math.ceil(filteredProducts.length / productsPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };
  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const renderSortIcon = (field) => {
    if (sortField !== field) return null;
    return sortDirection === "asc" ? <ChevronUp size={14} /> : <ChevronDown size={14} />;
  };

  return (
    <div className="admin-content">
      <main className="admin-products">
        <motion.div
          className="stat_Cards"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <StatCard name="All Products" icon={Package} value={stats.totalProducts} color="#6366F1" />
          <StatCard name="Best Selling" icon={TrendingUp} value={stats.topSelling} color="#10B981" />
          <StatCard name="Total Sales" icon={DollarSign} value={`$${stats.totalSales.toLocaleString('pl-PL', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`} color="#EF4444" />
        </motion.div>

        {/* FORMULARZ DODAWANIA PRODUKTU */}
        <motion.div
          className="product-form"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <h4 className="product-form__title">Add new product</h4>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Price</label>
                <input
                  type="number"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label>Old Price</label>
                <input
                  type="number"
                  value={oldPrice}
                  onChange={(e) => setOldPrice(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Description</label>
              <textarea
                rows={3}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label>Tags</label>
              <select
                multiple
                value={tags}
                onChange={(e) =>
                  setTags(Array.from(e.target.selectedOptions, (option) => option.value))
                }
              >
                {availableTags.map((tag) => (
                  <option key={tag.id} value={tag.id}>
                    {tag.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option value="">Select category</option>
                {availableCategories.map((cat) => (
                  <option key={cat.name} value={cat.name}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Photos</label>
              <input
                type="text"
                value={photos.join(", ")}
                onChange={(e) => setPhotos(e.target.value.split(",").map(photo => photo.trim()))}
              />
            </div>

            <button type="submit" className="btn-primary">
              Add Product
            </button>
          </form>
        </motion.div>

        {/* TABELA PRODUKTÓW */}
        <motion.div
          className="product-table-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="product-table-header">
            <h2>All Products</h2>
            <div className="search-container">
              <input
                type="text"
                placeholder="Search products..."
                onChange={(e) => setSearchTerm(e.target.value)}
                value={searchTerm}
              />
              <Search className="search-icon" size={18} />
            </div>
          </div>

          <div className="table-wrapper">
            <table className="product-table">
              <thead>
                <tr>
                  <th onClick={() => handleSort("name")} className="sortable-header">
                    <div className="header-content">
                      <span>Name</span>
                      {renderSortIcon("name")}
                    </div>
                  </th>
                  <th onClick={() => handleSort("price")} className="sortable-header">
                    <div className="header-content">
                      <span>Price</span>
                      {renderSortIcon("price")}
                    </div>
                  </th>
                  <th>Old Price</th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {currentProducts.map((prod) =>
                  editId === prod.id ? (
                    <motion.tr
                      key={prod.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                      className="edit-row"
                    >
                      <td>
                        <input
                          type="text"
                          value={editName}
                          onChange={(e) => setEditName(e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          value={editPrice}
                          onChange={(e) => setEditPrice(e.target.value)}
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          value={editOldPrice}
                          onChange={(e) => setEditOldPrice(e.target.value)}
                        />
                      </td>
                      <td className="description-cell">
                        <textarea
                          value={editDescription}
                          onChange={(e) => setEditDescription(e.target.value)}
                          className="edit-description"
                        />
                      </td>
                      <td className="action-cell">
                        <button onClick={handleEditSubmit} className="btn-save">
                          Save
                        </button>
                        <button onClick={cancelEdit} className="btn-cancel">
                          Cancel
                        </button>
                      </td>
                    </motion.tr>
                  ) : (
                    <motion.tr
                      key={prod.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ duration: 0.3 }}
                    >
                      <td>{prod.name}</td>
                      <td>${parseFloat(prod.price).toFixed(2)}</td>
                      <td>{prod.old_price ? `$${parseFloat(prod.old_price).toFixed(2)}` : "-"}</td>
                      <td className="description-cell">
                        <div className="description-content">{prod.description}</div>
                      </td>
                      <td className="action-cell">
                        <button onClick={() => startEdit(prod)} className="btn-edit">
                          <Edit size={18} />
                        </button>
                        <button onClick={() => handleDelete(prod.id)} className="btn-delete">
                          <Trash2 size={18} />
                        </button>
                      </td>
                    </motion.tr>
                  )
                )}
              </tbody>
            </table>
          </div>

          <div className="pagination-container">
            <div className="pagination-info">
              <p className="pagination-text">
                Displaying {indexOfFirstProduct + 1} to {Math.min(indexOfLastProduct, filteredProducts.length)} from {filteredProducts.length} products
              </p>
            </div>
            <div className="pagination-controls">
              <button
                onClick={prevPage}
                disabled={currentPage === 1}
                className={`pagination-button ${currentPage === 1 ? "disabled" : ""}`}
              >
                <ChevronLeft size={16} />
                <span>&lt;</span>
              </button>
              {Array.from({ length: Math.ceil(filteredProducts.length / productsPerPage) }).map((_, index) => (
                <button
                  key={index}
                  onClick={() => paginate(index + 1)}
                  className={`pagination-number ${currentPage === index + 1 ? "active" : ""}`}
                >
                  {index + 1}
                </button>
              )).slice(
                Math.max(0, currentPage - 3),
                Math.min(Math.ceil(filteredProducts.length / productsPerPage), currentPage + 2)
              )}
              <button
                onClick={nextPage}
                disabled={currentPage >= Math.ceil(filteredProducts.length / productsPerPage)}
                className={`pagination-button ${currentPage >= Math.ceil(filteredProducts.length / productsPerPage) ? "disabled" : ""}`}
              >
                <ChevronRight size={16} />
                <span>&gt;</span>
              </button>
            </div>
          </div>
        </motion.div>

        <div className="chart-container-products">
          {stats.trend && stats.trend.labels && stats.trend.labels.length > 0 && (
            <div className="chart-item">
              <SalesTrendChart trend={stats.trend} />
            </div>
          )}
          <div className="chart-item">
            <CategoryDistributionChart category_distribution={stats.category_distribution} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default AdminProducts;
