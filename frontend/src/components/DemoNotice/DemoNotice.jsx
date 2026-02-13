import React from "react";
import { useLocation } from "react-router-dom";
import "./DemoNotice.scss";

const DemoNotice = () => {
  const location = useLocation();

  const backendRoutes = [
    "/admin",
    "/client-panel",
    "/cart",
    "/shop",
    "/product",
    "/search",
    "/category",
  ];

  const isGitHubPages =
    typeof window !== "undefined" &&
    (window.location.hostname.includes("github.io") ||
      window.location.hostname.includes("project.dawidolko.pl") ||
      window.location.hostname.includes("githubpages") ||
      (window.location.protocol === "https:" &&
        !window.location.hostname.includes("localhost") &&
        !window.location.hostname.includes("127.0.0.1") &&
        !window.location.hostname.includes("0.0.0.0")));

  const requiresBackend =
    backendRoutes.some((route) => location.pathname.startsWith(route)) ||
    location.pathname.includes("/product/") ||
    location.pathname.includes("/search/") ||
    location.pathname.includes("/category/");

  if (!isGitHubPages || !requiresBackend) {
    return null;
  }

  return (
    <div className="demo-notice">
      <div className="demo-notice__container">
        <div className="demo-notice__icon">ℹ️</div>
        <div className="demo-notice__content">
          <strong>Demo Version Notice:</strong> This is a static preview
          version. Features requiring database connectivity (shopping cart, user
          accounts, search, etc.) are not available. For the full experience,
          please visit the
          <a
            href="https://github.com/dawidolko/SmartRecommender-Project-Django-React"
            target="_blank"
            rel="noopener noreferrer"
            className="demo-notice__link">
            GitHub repository
          </a>
          and follow the installation guide.
        </div>
      </div>
    </div>
  );
};

export default DemoNotice;
