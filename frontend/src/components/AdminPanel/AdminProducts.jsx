import React, { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import {
  Edit,
  Trash2,
  Search,
  Package,
  DollarSign,
  TrendingUp,
  ChevronUp,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import StatCard from "./StatCard";
import SalesTrendChart from "./SalesTrendChart";
import CategoryDistributionChart from "./CategoryDistributionChart";
import ConfirmationModal from "./ConfirmationModal";
import "./AdminPanel.scss";
import config from "../../config/config";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

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
  const [uploadedImages, setUploadedImages] = useState([]);

  const [availableTags, setAvailableTags] = useState([]);
  const [availableCategories, setAvailableCategories] = useState([]);

  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editPrice, setEditPrice] = useState("");
  const [editOldPrice, setEditOldPrice] = useState("");
  const [editDescription, setEditDescription] = useState("");
  const [editTags, setEditTags] = useState([]);
  const [editCategory, setEditCategory] = useState("");
  const [editUploadedImages, setEditUploadedImages] = useState([]);

  const [searchTerm, setSearchTerm] = useState("");
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [productsPerPage] = useState(10);
  const [sortField, setSortField] = useState("name");
  const [sortDirection, setSortDirection] = useState("asc");
  const [loading, setLoading] = useState(false);

  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isAddConfirmModalOpen, setIsAddConfirmModalOpen] = useState(false);
  const [isEditConfirmModalOpen, setIsEditConfirmModalOpen] = useState(false);
  const [pendingDeleteId, setPendingDeleteId] = useState(null);

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
    setLoading(true);
    const token = localStorage.getItem("access");
    axios
      .get(`${config.apiUrl}/api/products/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setProducts(res.data);
        setFilteredProducts(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching products:", err);
        setLoading(false);
      });
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
      const response = await axios.get(`${config.apiUrl}/api/tags/`, {
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
      const response = await axios.get(`${config.apiUrl}/api/categories/`, {
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
      const response = await axios.get(`${config.apiUrl}/api/products/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEditName(response.data.name);
      setEditPrice(response.data.price);
      setEditOldPrice(response.data.old_price || "");
      setEditDescription(response.data.description || "");
      setEditTags(response.data.tags || []);
      setEditCategory(
        response.data.categories && response.data.categories.length > 0
          ? response.data.categories[0]
          : ""
      );
      setEditUploadedImages([]);
    } catch (error) {
      console.error("Error fetching product:", error);
    }
  };

  const fetchStats = () => {
    const token = localStorage.getItem("access");
    axios
      .get(`${config.apiUrl}/api/admin-dashboard-stats/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setStats({
          totalProducts: res.data.totalProducts || 0,
          totalSales: res.data.totalSales || 0,
          topSelling: res.data.topSelling || 0,
          trend: res.data.trend || { labels: [], data: [] },
          category_distribution: res.data.category_distribution || {
            labels: [],
            data: [],
          },
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

  const handleImageUpload = (e) => {
    setUploadedImages(Array.from(e.target.files));
  };

  const handleSubmitClick = (e) => {
    e.preventDefault();

    if (!name || !price || isNaN(price)) {
      toast.error("Please fill in all required fields correctly.");
      return;
    }

    setIsAddConfirmModalOpen(true);
  };

  const handleSubmit = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");

    try {
      const productData = {
        name,
        price,
        old_price: oldPrice || null,
        description: description || null,
        tags: tags,
        categories: category ? [category] : [],
      };

      const response = await axios.post(
        `${config.apiUrl}/api/products/`,
        productData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      const productId = response.data.id;

      if (uploadedImages.length > 0) {
        const formData = new FormData();
        uploadedImages.forEach((image) => {
          formData.append("images", image);
        });

        await axios.post(
          `${config.apiUrl}/api/products/${productId}/upload-images/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
      }

      try {
        await axios.post(
          `${config.apiUrl}/api/admin/update-product-similarity/`,
          { product_id: productId },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {}

      try {
        await axios.post(
          `${config.apiUrl}/api/update-association-rules/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {}

      try {
        await axios.post(
          `${config.apiUrl}/api/process-recommendations/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {}

      toast.success("Product added successfully with all integrations!");
      clearForm();
      fetchProducts();
      fetchStats();
    } catch (error) {
      console.error("Error submitting product:", error);
      toast.error(
        "Error adding product. Please check your data and try again."
      );
    } finally {
      setIsAddConfirmModalOpen(false);
      setLoading(false);
    }
  };

  const handleEditClick = (e) => {
    e.preventDefault();
    if (!editName || !editPrice || isNaN(editPrice)) {
      toast.error("Please fill in all required fields correctly.");
      return;
    }
    setIsEditConfirmModalOpen(true);
  };

  const handleEditSubmit = async () => {
    setLoading(true);
    const token = localStorage.getItem("access");

    try {
      const productData = {
        name: editName,
        price: editPrice,
        old_price: editOldPrice || null,
        description: editDescription || null,
        tags: editTags,
        categories: editCategory ? [editCategory] : [],
      };

      await axios.put(`${config.apiUrl}/api/products/${editId}/`, productData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (editUploadedImages.length > 0) {
        const formData = new FormData();
        editUploadedImages.forEach((image) => {
          formData.append("images", image);
        });

        await axios.post(
          `${config.apiUrl}/api/products/${editId}/upload-images/`,
          formData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "multipart/form-data",
            },
          }
        );
      }

      try {
        await axios.post(
          `${config.apiUrl}/api/admin/update-product-similarity/`,
          { product_id: editId },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {}

      try {
        await axios.post(
          `${config.apiUrl}/api/update-association-rules/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {}

      try {
        await axios.post(
          `${config.apiUrl}/api/process-recommendations/`,
          {},
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        );
      } catch (error) {}

      setEditId(null);
      setEditName("");
      setEditPrice("");
      setEditOldPrice("");
      setEditDescription("");
      setEditTags([]);
      setEditCategory("");
      setEditUploadedImages([]);
      fetchProducts();
      fetchStats();
      toast.success("Product updated successfully with all integrations!");
    } catch (error) {
      console.error("Error editing product:", error);
      toast.error(
        "Error updating product. Please check your data and try again."
      );
    } finally {
      setIsEditConfirmModalOpen(false);
      setLoading(false);
    }
  };

  const clearForm = () => {
    setName("");
    setPrice("");
    setOldPrice("");
    setDescription("");
    setTags([]);
    setCategory("");
    setUploadedImages([]);
  };

  const handleDeleteClick = (productId) => {
    setPendingDeleteId(productId);
    setIsDeleteModalOpen(true);
  };

  const handleDelete = async () => {
    if (!pendingDeleteId) return;
    setLoading(true);

    const token = localStorage.getItem("access");
    try {
      await axios.delete(`${config.apiUrl}/api/products/${pendingDeleteId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProducts((prev) => prev.filter((p) => p.id !== pendingDeleteId));
      fetchStats();
      toast.success("Product deleted successfully!");
    } catch (error) {
      console.error("Error deleting product:", error);
      toast.error("Error deleting product. Please try again.");
    } finally {
      setIsDeleteModalOpen(false);
      setPendingDeleteId(null);
      setLoading(false);
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
    setEditUploadedImages([]);
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
  const currentProducts = filteredProducts.slice(
    indexOfFirstProduct,
    indexOfLastProduct
  );

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
    return sortDirection === "asc" ? (
      <ChevronUp size={14} />
    ) : (
      <ChevronDown size={14} />
    );
  };

  if (loading) {
    return <div className="loading-spinner"></div>;
  }

  return (
    <div className="admin-content">
      <main className="admin-products">
        <motion.div
          className="stat_Cards"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}>
          <StatCard
            name="All Products"
            icon={Package}
            value={stats.totalProducts}
            color="#6366F1"
            variant="first"
          />
          <StatCard
            name="Best Selling"
            icon={TrendingUp}
            value={stats.topSelling}
            color="#10B981"
            variant="third"
          />
          <StatCard
            name="Total Sales"
            icon={DollarSign}
            value={`$${stats.totalSales.toLocaleString("en-US", {
              minimumFractionDigits: 2,
              maximumFractionDigits: 2,
            })}`}
            color="#EF4444"
            variant="second"
          />
        </motion.div>

        <motion.div
          className="product-form"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}>
          <h4 className="product-form__title">Add new product</h4>
          <form onSubmit={(e) => e.preventDefault()}>
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
                  setTags(
                    Array.from(
                      e.target.selectedOptions,
                      (option) => option.value
                    )
                  )
                }>
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
                onChange={(e) => setCategory(e.target.value)}>
                <option value="">Select category</option>
                {availableCategories.map((cat) => (
                  <option key={cat.name} value={cat.name}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Upload Images</label>
              <input
                type="file"
                accept="image/*"
                multiple
                onChange={handleImageUpload}
                className="file-input"
              />
              {uploadedImages.length > 0 && (
                <div className="uploaded-images-preview">
                  <p>Uploaded files: {uploadedImages.length}</p>
                  <ul>
                    {Array.from(uploadedImages).map((file, index) => (
                      <li key={index}>{file.name}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <button
              type="button"
              onClick={handleSubmitClick}
              className="btn-primary">
              Add Product
            </button>
          </form>
        </motion.div>

        <motion.div
          className="product-table-container"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}>
          <div className="product-table-header">
            <h2>All Products</h2>
            <div className="search-container">
              <input
                type="text"
                placeholder="Search products..."
                onChange={(e) => setSearchTerm(e.target.value)}
                value={searchTerm}
                style={{ color: "#000000" }}
              />
              <Search className="search-icon" size={18} />
            </div>
          </div>

          <div className="table-wrapper">
            <table className="product-table">
              <thead>
                <tr>
                  <th
                    onClick={() => handleSort("name")}
                    className="sortable-header">
                    <div className="header-content">
                      <span>Name</span>
                      {renderSortIcon("name")}
                    </div>
                  </th>
                  <th
                    onClick={() => handleSort("price")}
                    className="sortable-header">
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
                {currentProducts.length > 0 ? (
                  currentProducts.map((prod) =>
                    editId === prod.id ? (
                      <motion.tr
                        key={prod.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.3 }}
                        className="edit-row">
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
                          <button
                            onClick={handleEditClick}
                            className="btn-save">
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
                        transition={{ duration: 0.3 }}>
                        <td>{prod.name}</td>
                        <td>${parseFloat(prod.price).toFixed(2)}</td>
                        <td>
                          {prod.old_price
                            ? `$${parseFloat(prod.old_price).toFixed(2)}`
                            : "-"}
                        </td>
                        <td className="description-cell">
                          <div className="description-content">
                            {prod.description}
                          </div>
                        </td>
                        <td className="action-cell">
                          <button
                            onClick={() => startEdit(prod)}
                            className="btn-edit">
                            <Edit size={18} />
                          </button>
                          <button
                            onClick={() => handleDeleteClick(prod.id)}
                            className="btn-delete">
                            <Trash2 size={18} />
                          </button>
                        </td>
                      </motion.tr>
                    )
                  )
                ) : (
                  <tr>
                    <td colSpan="5" className="no-results">
                      No products found matching your search criteria
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {filteredProducts.length > 0 && (
            <div className="pagination-container">
              <div className="pagination-info">
                <p className="pagination-text">
                  Displaying {indexOfFirstProduct + 1} to{" "}
                  {Math.min(indexOfLastProduct, filteredProducts.length)} from{" "}
                  {filteredProducts.length} products
                </p>
              </div>
              <div className="pagination-controls">
                <button
                  onClick={prevPage}
                  disabled={currentPage === 1}
                  className={`pagination-button ${
                    currentPage === 1 ? "disabled" : ""
                  }`}>
                  <ChevronLeft size={16} />
                  <span>&lt;</span>
                </button>
                {Array.from({
                  length: Math.ceil(filteredProducts.length / productsPerPage),
                })
                  .map((_, index) => (
                    <button
                      key={index}
                      onClick={() => paginate(index + 1)}
                      className={`pagination-number ${
                        currentPage === index + 1 ? "active" : ""
                      }`}>
                      {index + 1}
                    </button>
                  ))
                  .slice(
                    Math.max(0, currentPage - 3),
                    Math.min(
                      Math.ceil(filteredProducts.length / productsPerPage),
                      currentPage + 2
                    )
                  )}
                <button
                  onClick={nextPage}
                  disabled={
                    currentPage >=
                    Math.ceil(filteredProducts.length / productsPerPage)
                  }
                  className={`pagination-button ${
                    currentPage >=
                    Math.ceil(filteredProducts.length / productsPerPage)
                      ? "disabled"
                      : ""
                  }`}>
                  <ChevronRight size={16} />
                  <span>&gt;</span>
                </button>
              </div>
            </div>
          )}
        </motion.div>

        <div className="chart-container-products">
          {stats.trend &&
            stats.trend.labels &&
            stats.trend.labels.length > 0 && (
              <div className="chart-item">
                <SalesTrendChart trend={stats.trend} />
              </div>
            )}
          <div className="chart-item">
            <CategoryDistributionChart
              category_distribution={stats.category_distribution}
            />
          </div>
        </div>
      </main>

      <ConfirmationModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={handleDelete}
        title="Confirm Deletion"
        message="Are you sure you want to delete this product? This action cannot be undone."
      />

      <ConfirmationModal
        isOpen={isEditConfirmModalOpen}
        onClose={() => setIsEditConfirmModalOpen(false)}
        onConfirm={handleEditSubmit}
        title="Confirm Update"
        message="Do you want to save changes to this product?"
      />

      <ConfirmationModal
        isOpen={isAddConfirmModalOpen}
        onClose={() => setIsAddConfirmModalOpen(false)}
        onConfirm={handleSubmit}
        title="Confirm Addition"
        message="Do you want to add this new product?"
      />
    </div>
  );
};

export default AdminProducts;
