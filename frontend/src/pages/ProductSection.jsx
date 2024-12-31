import React from "react";
import Hero from "../components/Hero/Hero";
import ProductPage from "../components/ProductSection/ProductPage";

const ProductSection = () => {
  return (
    <div>
      {/* Banner hero */}
      <Hero title="DETAILS" cName="hero__img" />

      {/* Komponent właściwy z logiką produktu */}
      <ProductPage />
    </div>
  );
};

export default ProductSection;
