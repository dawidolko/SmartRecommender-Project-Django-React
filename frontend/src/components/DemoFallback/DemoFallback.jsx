/**
 * DemoFallback Component - GitHub Pages Demo Fallback Content
 *
 * Authors: Dawid Olko & Piotr Smoła
 * Date: 2026-02-13
 * Version: 1.0
 *
 * Displays informative content when demo/mock data fails to load on GitHub Pages.
 * Provides users with clear explanation and guidance for full functionality.
 *
 * @component
 * @returns {React.ReactElement} Demo fallback content with call-to-action
 */
import React from "react";
import { useNavigate } from "react-router-dom";
import "./DemoFallback.scss";

const DemoFallback = ({
  title = "Demo Content Unavailable",
  message = "This feature requires database connectivity and is not available in the static demo version.",
  showBackButton = true,
  showHomeButton = true,
}) => {
  const navigate = useNavigate();

  return (
    <div className="demo-fallback">
      <div className="demo-fallback__container">
        <div className="demo-fallback__icon">📦</div>
        <h2 className="demo-fallback__title">{title}</h2>
        <p className="demo-fallback__message">{message}</p>

        <div className="demo-fallback__info">
          <p>
            <strong>🔧 Want to see the full functionality?</strong>
          </p>
          <p>
            Clone the repository and run the complete application with database
            support:
          </p>
        </div>

        <div className="demo-fallback__code">
          <code>
            git clone
            https://github.com/dawidolko/SmartRecommender-Project-Django-React
            <br />
            cd SmartRecommender-Project-Django-React
            <br />
            docker compose -f .tools/docker/docker-compose.yml up --build
          </code>
        </div>

        <div className="demo-fallback__actions">
          {showBackButton && (
            <button
              className="demo-fallback__btn demo-fallback__btn--secondary"
              onClick={() => navigate(-1)}>
              ← Go Back
            </button>
          )}
          {showHomeButton && (
            <button
              className="demo-fallback__btn demo-fallback__btn--primary"
              onClick={() => navigate("/home")}>
              🏠 Go Home
            </button>
          )}
          <a
            href="https://github.com/dawidolko/SmartRecommender-Project-Django-React"
            target="_blank"
            rel="noopener noreferrer"
            className="demo-fallback__btn demo-fallback__btn--github">
            📂 View Repository
          </a>
        </div>
      </div>
    </div>
  );
};

export default DemoFallback;
