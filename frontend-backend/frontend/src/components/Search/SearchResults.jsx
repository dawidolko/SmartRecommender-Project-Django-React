import React from "react";
import "./SearchResults.scss";
import ShopProduct from "../ShopContent/ShopProduct";

const SearchResults = ({ searchResults }) => {
  return (
    <div className="search-results">
      <h2 className="search-results__title">Search Results</h2>
      <div className="search-results__products">
        {searchResults.length > 0 ? (
          searchResults.map((product) => (
            <ShopProduct
              key={product.id}
              id={product.id}
              name={product.name}
              price={product.price}
              old_price={product.old_price}
              imgs={product.photos.map((photo) => photo.path)}
              category={product.categories[0] || "N/A"}
            />
          ))
        ) : (
          <p>No products found.</p>
        )}
      </div>
    </div>
  );
};

export default SearchResults;
