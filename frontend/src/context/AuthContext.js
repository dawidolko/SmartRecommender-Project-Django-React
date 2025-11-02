import { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import config from "../config/config";

/**
 * AuthContext - Authentication state management for SmartRecommender
 *
 * Provides global authentication state using React Context API.
 * Manages JWT tokens, user session, and authentication lifecycle.
 *
 * Features:
 *   - JWT token management with expiration checking
 *   - Automatic token validation on mount
 *   - User data persistence in localStorage
 *   - Automatic logout on token expiration
 *   - User profile fetching from API
 *
 * Context Values:
 *   - user: Current user object (decoded JWT + API data)
 *   - token: JWT access token
 *   - login(token): Store token and authenticate user
 *   - logout(): Clear session and remove tokens
 *   - setUser(user): Update user state manually
 *
 * Token Structure (JWT):
 *   - exp: Expiration timestamp
 *   - user_id: User database ID
 *   - email: User email address
 *   - role: User role ('admin' or 'client')
 *
 * @context
 */
export const AuthContext = createContext();

/**
 * AuthProvider Component
 *
 * Wraps application with authentication context provider.
 * Automatically validates JWT tokens and manages user session.
 *
 * @component
 * @param {Object} props
 * @param {React.ReactNode} props.children - Child components
 * @returns {React.ReactElement} Context provider with auth state
 */
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("loggedUser");
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [token, setToken] = useState(localStorage.getItem("access") || null);

  useEffect(() => {
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const currentTime = Date.now() / 1000;

        if (decoded.exp < currentTime) {
          logout();
        } else if (!user) {
          setUser(decoded);
          fetchUserData(token);
        }
      } catch (error) {
        console.error("Błąd dekodowania tokena:", error);
        logout();
      }
    }
  }, [token, user]);

  const fetchUserData = async (authToken) => {
    try {
      const response = await fetch(`${config.apiUrl}/api/user/`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authToken}`,
        },
      });
      if (!response.ok) {
        throw new Error("Failed to fetch user data");
      }
      const data = await response.json();
      setUser(data);
      localStorage.setItem("loggedUser", JSON.stringify(data));
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  };

  const login = (newToken) => {
    localStorage.setItem("access", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("loggedUser");
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};
