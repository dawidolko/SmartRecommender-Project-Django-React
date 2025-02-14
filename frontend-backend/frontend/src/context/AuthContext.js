import { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(localStorage.getItem("token") || null);

    useEffect(() => {
        if (token) {
            try {
                const decoded = jwtDecode(token);
                setUser(decoded);
                console.log("[AuthContext] Current User:", decoded);
            } catch (error) {
                console.error("Błąd dekodowania tokena:", error);
                logout();
            }
        }
    }, [token]);

    const fetchUserData = async (authToken) => {
        console.log("[AuthContext] Fetching user data...");  
    
        try {
            const response = await fetch("http://127.0.0.1:8000/api/user/", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${authToken}`,
                },
            });
    
            console.log("[AuthContext] API Response Status:", response.status);
    
            if (!response.ok) {
                throw new Error("Failed to fetch user data");
            }
    
            const data = await response.json();
            console.log("[AuthContext] User Data:", data);
            setUser(data);
        } catch (error) {
            console.error("Error fetching user data:", error);
        }
    };
    

    const login = (newToken) => {
        localStorage.setItem("token", newToken);
        const decoded = jwtDecode(newToken);
        console.log("[AuthContext] Logged in user:", decoded);
        setUser(decoded);
        setToken(newToken);
        fetchUserData(newToken);
    };

    const logout = () => {
        console.log("[AuthContext] Logging out...");
        localStorage.removeItem("token");
        setUser(null);
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ user, token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
