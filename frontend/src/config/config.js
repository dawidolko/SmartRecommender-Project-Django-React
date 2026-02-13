const isProduction =
  typeof window !== "undefined" &&
  (window.location.hostname.includes("github.io") ||
    window.location.hostname.includes("project.dawidolko.pl") ||
    window.location.hostname.includes("githubpages") ||
    (window.location.protocol === "https:" &&
      !window.location.hostname.includes("localhost") &&
      !window.location.hostname.includes("127.0.0.1") &&
      !window.location.hostname.includes("0.0.0.0")));

const config = {
  apiUrl: process.env.REACT_APP_API_URL || "http://localhost:8000",
  useMockData: isProduction || process.env.REACT_APP_USE_MOCK_DATA === "true",
};

if (typeof window !== "undefined") {
  console.log("Config Debug:", {
    hostname: window.location.hostname,
    isProduction: isProduction,
    useMockData: config.useMockData,
    apiUrl: config.apiUrl,
  });
}

export default config;
