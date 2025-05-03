import { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import config from "../config/config";

export const AuthContext = createContext();

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
