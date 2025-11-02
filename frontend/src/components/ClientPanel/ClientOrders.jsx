/**
 * ClientOrders Component
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2025-11-02
 * Version: 2.0
 *
 * Client panel component for viewing order history and managing product reviews.
 * Displays user's orders with detailed information and review submission functionality.
 *
 * Features:
 *   - Order history list with status tracking
 *   - Search functionality (by order ID, status, date)
 *   - Sorting by date, status, total amount
 *   - Pagination (10 orders per page)
 *   - Order details modal with product list
 *   - Product review submission
 *   - Star rating system
 *   - Status color coding
 *   - Date formatting
 *   - Total amount calculation per order
 *   - Expandable order items view
 *
 * Order Status Types:
 *   - Pending - Order created, awaiting processing
 *   - Processing - Order being prepared
 *   - Shipped - Order dispatched
 *   - Delivered - Order received by customer
 *   - Cancelled - Order cancelled
 *
 * Review System:
 *   - 5-star rating scale
 *   - Text review (optional)
 *   - One review per product per user
 *   - Submit from order details modal
 *
 * State Management:
 *   - orders: Array of user's orders
 *   - filteredOrders: Orders after search/filter/sort
 *   - sortKey: Field to sort by (date, status, total)
 *   - sortOrder: Sort direction ('asc' or 'desc')
 *   - searchTerm: Current search query
 *   - currentPage: Active pagination page
 *   - isModalOpen: Order details modal visibility
 *   - isReviewModalOpen: Review submission modal visibility
 *   - selectedOrder: Order currently viewed in modal
 *   - selectedProduct: Product selected for review
 *   - loading: Loading state for async operations
 *
 * API Endpoints:
 *   - GET /api/orders/ - Fetch user's orders
 *   - GET /api/client/orders/:id/ - Fetch specific order details
 *   - POST /api/products/:id/reviews/ - Submit product review
 *
 * Calculations:
 *   - Order Total = Σ(product_price × quantity) for all products
 *   - Date Formatting: "MMM dd, yyyy" format
 *
 * @component
 * @returns {React.ReactElement} Client orders page with history and reviews
 */
/* eslint-disable react-hooks/exhaustive-deps */
import React, { useEffect, useState } from "react";
import axios from "axios";
import { format } from "date-fns";
import {
  ChevronUp,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  Search,
} from "lucide-react";
import config from "../../config/config";
import "./ClientPanel.scss";
import Modal from "./Modal";
import ReviewForm from "./ReviewForm";

const ClientOrders = () => {
  const [orders, setOrders] = useState([]);
  const [sortKey, setSortKey] = useState("date");
  const [sortOrder, setSortOrder] = useState("asc");
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [ordersPerPage] = useState(10);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isReviewModalOpen, setIsReviewModalOpen] = useState(false);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [orderLoading, setOrderLoading] = useState(false);
  const [orderError, setOrderError] = useState(null);

  const getStatusClass = (status) => {
    switch (status) {
      case "Processing":
        return "status-processing";
      case "Shipped":
        return "status-shipped";
      case "Delivered":
        return "status-delivered";
      case "Cancelled":
        return "status-cancelled";
      case "Pending":
      default:
        return "status-pending";
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("access");
    setLoading(true);
    axios
      .get(`${config.apiUrl}/api/orders/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setOrders(res.data);
        setFilteredOrders(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching orders:", err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    handleFilteringAndSorting();
  }, [searchTerm, sortKey, sortOrder, orders]);

  const handleFilteringAndSorting = () => {
    if (!orders.length) return;

    let data = [...orders];

    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      data = data.filter((order) => {
        const idMatch = order.id.toString().includes(term);
        const statusMatch = order.status?.toLowerCase().includes(term);

        const orderDate = format(
          new Date(order.date_order),
          "dd MMM yyyy, HH:mm"
        ).toLowerCase();
        const dateMatch = orderDate.includes(term);

        return idMatch || statusMatch || dateMatch;
      });
    }

    data.sort((a, b) => {
      let comp = 0;
      if (sortKey === "date") {
        comp = new Date(a.date_order) - new Date(b.date_order);
      } else if (sortKey === "status") {
        comp = a.status.localeCompare(b.status);
      } else if (sortKey === "id") {
        comp = a.id - b.id;
      }
      return sortOrder === "asc" ? comp : -comp;
    });

    setFilteredOrders(data);
    setCurrentPage(1);
  };

  const handleViewDetails = (orderId) => {
    const token = localStorage.getItem("access");
    setOrderLoading(true);
    setOrderError(null);

    axios
      .get(`${config.apiUrl}/api/client/orders/${orderId}/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setSelectedOrder(res.data);
        setOrderLoading(false);
        setIsModalOpen(true);
      })
      .catch((err) => {
        console.error("Error fetching order details:", err);
        setOrderError("Failed to fetch order details");
        setOrderLoading(false);
      });
  };

  const handleAddReview = (product) => {
    if (product && product.id) {
      setSelectedProduct(product);
      setIsReviewModalOpen(true);
    } else {
      console.error("Invalid product object:", product);
    }
  };

  const handleReviewSubmitted = (reviewData) => {
    setIsReviewModalOpen(false);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedOrder(null);
  };

  const handleCloseReviewModal = () => {
    setIsReviewModalOpen(false);
    setSelectedProduct(null);
  };

  const handleSort = (column) => {
    if (sortKey === column) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortKey(column);
      setSortOrder("asc");
    }
  };

  const handleSearch = (value) => {
    setSearchTerm(value);
  };

  const renderSortIcon = (column) => {
    if (sortKey !== column) return null;
    return sortOrder === "asc" ? (
      <ChevronUp size={14} />
    ) : (
      <ChevronDown size={14} />
    );
  };

  const indexOfLast = currentPage * ordersPerPage;
  const indexOfFirst = indexOfLast - ordersPerPage;
  const currentOrders = filteredOrders.slice(indexOfFirst, indexOfLast);

  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  const nextPage = () => {
    if (currentPage < Math.ceil(filteredOrders.length / ordersPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  if (loading) {
    return <div className="loading-spinner"></div>;
  }

  const tableCellStyle = {
    textAlign: "center",
    verticalAlign: "middle",
  };

  const renderOrderDetails = () => {
    if (orderLoading) return <div className="loading-spinner"></div>;
    if (orderError) return <div>{orderError}</div>;
    if (!selectedOrder) return <div>No order found.</div>;

    return (
      <div className="order-detail-modal">
        <p>
          <strong>Date: </strong>
          {format(new Date(selectedOrder.date_order), "dd MMM yyyy, HH:mm")}
        </p>
        <p>
          <strong>Status: </strong>
          <span className={getStatusClass(selectedOrder.status)}>
            {selectedOrder.status}
          </span>
        </p>
        <p>
          <strong>Total:</strong> ${parseFloat(selectedOrder.total).toFixed(2)}
        </p>

        <h3 style={{ marginTop: "1rem" }}>Ordered Products:</h3>
        <div className="table-responsive">
          <table className="modal-table">
            <thead>
              <tr>
                <th style={{ textAlign: "center" }}>Image</th>
                <th style={{ textAlign: "center" }}>Name</th>
                <th style={{ textAlign: "center" }}>Quantity</th>
                <th style={{ textAlign: "center" }}>Price (each)</th>
                <th style={{ textAlign: "center" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {selectedOrder.order_products.map((op) => {
                const product = op.product;

                const imgSrc =
                  product.photos && product.photos.length > 0
                    ? `${config.apiUrl}/media/${product.photos[0].path}`
                    : `${config.apiUrl}/media/placeholder-product.png`;

                const price =
                  product.price &&
                  !isNaN(parseFloat(product.price)) &&
                  parseFloat(product.price) > 0
                    ? parseFloat(product.price)
                    : 0;

                return (
                  <tr key={op.id || `${selectedOrder.id}-${product.id}`}>
                    <td
                      style={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        border: "none",
                      }}>
                      <img
                        src={imgSrc}
                        alt={product.name}
                        style={{ width: "100px" }}
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.src = `${config.apiUrl}/media/placeholder-product.png`;
                        }}
                      />
                    </td>
                    <td c style={{ textAlign: "center" }}>
                      {product.name}
                    </td>
                    <td style={{ textAlign: "center" }}>{op.quantity}</td>
                    <td style={{ textAlign: "center", width: "85px" }}>
                      ${price.toFixed(2)}
                    </td>
                    <td style={{ textAlign: "center" }}>
                      <button
                        className="btn-primary review-btn2"
                        onClick={() => handleAddReview(product)}>
                        Add Review
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    );
  };

  return (
    <div className="client-main">
      <div className="product-table-container2">
        <div className="product-table-header2">
          <h2>Your Orders</h2>
          <div className="search-container2">
            <input
              type="text"
              placeholder="Search orders... (ID, Status, Date)"
              onChange={(e) => handleSearch(e.target.value)}
              value={searchTerm}
            />
            <Search className="search-icon" size={18} />
          </div>
        </div>

        <div className="table-wrapper">
          <table className="product-table2">
            <thead>
              <tr>
                <th
                  style={tableCellStyle}
                  onClick={() => handleSort("id")}
                  className="sortable-header">
                  <div className="header-content">
                    <span>Order ID</span>
                    {renderSortIcon("id")}
                  </div>
                </th>
                <th
                  style={tableCellStyle}
                  onClick={() => handleSort("date")}
                  className="sortable-header">
                  <div className="header-content">
                    <span>Date</span>
                    {renderSortIcon("date")}
                  </div>
                </th>
                <th
                  style={tableCellStyle}
                  onClick={() => handleSort("status")}
                  className="sortable-header">
                  <div className="header-content">
                    <span>Status</span>
                    {renderSortIcon("status")}
                  </div>
                </th>
                <th style={tableCellStyle}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {currentOrders.length > 0 ? (
                currentOrders.map((order) => (
                  <tr key={order.id}>
                    <td style={tableCellStyle}>{order.id}</td>
                    <td style={tableCellStyle}>
                      {format(new Date(order.date_order), "dd MMM yyyy, HH:mm")}
                    </td>
                    <td style={tableCellStyle}>
                      <span
                        className={`status-badge ${getStatusClass(
                          order.status
                        )}`}>
                        {order.status}
                      </span>
                    </td>
                    <td style={tableCellStyle}>
                      <button
                        className="btn-primary"
                        onClick={() => handleViewDetails(order.id)}>
                        View Details
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="no-results">
                    No orders found matching your search criteria
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {filteredOrders.length > 0 && (
          <div className="pagination-container">
            <div className="pagination-info">
              <p className="pagination-text">
                Displaying {indexOfFirst + 1} to{" "}
                {Math.min(indexOfLast, filteredOrders.length)} of{" "}
                {filteredOrders.length} orders
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
                length: Math.ceil(filteredOrders.length / ordersPerPage),
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
                    Math.ceil(filteredOrders.length / ordersPerPage),
                    currentPage + 2
                  )
                )}
              <button
                onClick={nextPage}
                disabled={
                  currentPage >=
                  Math.ceil(filteredOrders.length / ordersPerPage)
                }
                className={`pagination-button ${
                  currentPage >=
                  Math.ceil(filteredOrders.length / ordersPerPage)
                    ? "disabled"
                    : ""
                }`}>
                <ChevronRight size={16} />
                <span>&gt;</span>
              </button>
            </div>
          </div>
        )}
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={
          selectedOrder ? `Order #${selectedOrder.id} Details` : "Order Details"
        }>
        {renderOrderDetails()}
      </Modal>

      <Modal
        isOpen={isReviewModalOpen}
        onClose={handleCloseReviewModal}
        title="Add Product Review">
        {selectedProduct && (
          <ReviewForm
            product={selectedProduct}
            onReviewSubmitted={handleReviewSubmitted}
            onClose={handleCloseReviewModal}
          />
        )}
      </Modal>
    </div>
  );
};

export default ClientOrders;
