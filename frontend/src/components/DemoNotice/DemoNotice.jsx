/**
 * DemoNotice Component - GitHub Pages Demo Version Notice
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2026-02-13
 * Version: 1.0
 *
 * Displays a notice banner when the application is running on GitHub Pages
 * to inform users that this is a static preview version with limited functionality.
 *
 * Features:
 *   - Automatically detects GitHub Pages environment
 *   - Shows informative message about limited functionality
 *   - Only displays on routes that require backend connectivity
 *   - Responsive design with accessibility support
 *
 * @component
 * @returns {React.ReactElement|null} Demo notice banner or null if not on GitHub Pages
 */
import React from "react";
import { useLocation } from "react-router-dom";
import "./DemoNotice.scss";

const DemoNotice = () => {
  const location = useLocation();

  // Check if we're on GitHub Pages or production environment
  const isGitHubPages =
    typeof window !== "undefined" &&
    (window.location.hostname.includes("github.io") ||
      window.location.hostname.includes("project.dawidolko.pl") ||
      window.location.hostname.includes("githubpages") ||
      (window.location.protocol === "https:" &&
        !window.location.hostname.includes("localhost") &&
        !window.location.hostname.includes("127.0.0.1") &&
        !window.location.hostname.includes("0.0.0.0")));

  // Debug info
  if (typeof window !== "undefined") {
    console.log("DemoNotice Debug:", {
      hostname: window.location.hostname,
      protocol: window.location.protocol,
      pathname: location.pathname,
      isGitHubPages: isGitHubPages,
    });
  }
  // Check if current route requires backend
  const requiresBackend =
    backendRoutes.some((route) => location.pathname.startsWith(route)) ||
    location.pathname.includes("/product/") ||
    location.pathname.includes("/search/") ||
    location.pathname.includes("/category/");

  // Only show notice on GitHub Pages for routes that need backend
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
