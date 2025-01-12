import React, { useEffect, useState } from "react";
import axios from "axios";
import "./AdminPanel.scss";

const AdminProducts = () => {
  const [products, setProducts] = useState([]);
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [oldPrice, setOldPrice] = useState("");
  const [description, setDescription] = useState("");

  const [editId, setEditId] = useState(null);
  const [editName, setEditName] = useState("");
  const [editPrice, setEditPrice] = useState("");
  const [editOldPrice, setEditOldPrice] = useState("");
  const [editDescription, setEditDescription] = useState("");

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = () => {
    axios
      .get("http://127.0.0.1:8000/api/products/")
      .then((res) => setProducts(res.data))
      .catch((err) => console.error("Error fetching products:", err));
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/api/products/", {
        name,
        price,
        old_price: oldPrice,
        description,
      });
      fetchProducts();
      setName("");
      setPrice("");
      setOldPrice("");
      setDescription("");
    } catch (error) {
      console.error("Error creating product:", error);
    }
  };

  const handleDelete = async (productId) => {
    if (!window.confirm("Are you sure you want to delete this product?"))
      return;
    try {
      await axios.delete(`http://127.0.0.1:8000/api/products/${productId}/`);
      setProducts((prev) => prev.filter((p) => p.id !== productId));
    } catch (error) {
      console.error("Error deleting product:", error);
    }
  };

  const startEdit = (prod) => {
    setEditId(prod.id);
    setEditName(prod.name);
    setEditPrice(prod.price);
    setEditOldPrice(prod.old_price || "");
    setEditDescription(prod.description || "");
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`http://127.0.0.1:8000/api/products/${editId}/`, {
        name: editName,
        price: editPrice,
        old_price: editOldPrice,
        description: editDescription,
      });
      fetchProducts();
      setEditId(null);
      setEditName("");
      setEditPrice("");
      setEditOldPrice("");
      setEditDescription("");
    } catch (error) {
      console.error("Error editing product:", error);
    }
  };

  const cancelEdit = () => {
    setEditId(null);
  };

  return (
    <div className="container">
      <h2>Products</h2>

      <form onSubmit={handleCreate} style={{ margin: "2rem 0" }}>
        <h4>Add new product</h4>
        <div className="mb-2">
          <label>Name</label>
          <input
            className="form-control"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="mb-2">
          <label>Price</label>
          <input
            type="number"
            className="form-control"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </div>
        <div className="mb-2">
          <label>Old Price</label>
          <input
            type="number"
            className="form-control"
            value={oldPrice}
            onChange={(e) => setOldPrice(e.target.value)}
          />
        </div>
        <div className="mb-2">
          <label>Description</label>
          <textarea
            className="form-control"
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        <button className="btn btn-primary">Add Product</button>
      </form>

      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Price</th>
              <th>Old Price</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((prod) => {
              if (prod.id === editId) {
                return (
                  <tr key={prod.id}>
                    <td>{prod.id}</td>
                    <td>
                      <input
                        className="form-control"
                        value={editName}
                        onChange={(e) => setEditName(e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        className="form-control"
                        value={editPrice}
                        onChange={(e) => setEditPrice(e.target.value)}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        className="form-control"
                        value={editOldPrice}
                        onChange={(e) => setEditOldPrice(e.target.value)}
                      />
                    </td>
                    <td>
                      <textarea
                        className="form-control"
                        rows={2}
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                      />
                    </td>
                    <td>
                      <button
                        className="btn btn-success"
                        onClick={handleEditSubmit}>
                        Save
                      </button>{" "}
                      <button
                        className="btn btn-secondary"
                        onClick={cancelEdit}>
                        Cancel
                      </button>
                    </td>
                  </tr>
                );
              } else {
                return (
                  <tr key={prod.id}>
                    <td>{prod.id}</td>
                    <td>{prod.name}</td>
                    <td>{prod.price}</td>
                    <td>{prod.old_price}</td>
                    <td>{prod.description}</td>
                    <td>
                      <button
                        className="btn btn-warning"
                        onClick={() => startEdit(prod)}>
                        Edit
                      </button>{" "}
                      <button
                        className="table-button table-button--delete btn btn-danger"
                        onClick={() => handleDelete(prod.id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                );
              }
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminProducts;
