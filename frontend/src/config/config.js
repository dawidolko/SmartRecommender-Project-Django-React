// Automatycznie wykrywaj czy jesteśmy na produkcji (nie localhost)
const isProduction =
  typeof window !== "undefined" &&
  !window.location.hostname.includes("localhost") &&
  !window.location.hostname.includes("127.0.0.1");

const config = {
  apiUrl: process.env.REACT_APP_API_URL || "http://localhost:8000",
  useMockData: isProduction || process.env.REACT_APP_USE_MOCK_DATA === "true",
};

export default config;
