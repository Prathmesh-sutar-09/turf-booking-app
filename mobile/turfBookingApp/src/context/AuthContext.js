import React, { createContext, useEffect, useState } from "react";
import api from "../services/api";
import { saveToken, getToken, removeToken } from "../utils/storage";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [userToken, setUserToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // restore token on app start
  useEffect(() => {
    const loadToken = async () => {
      const token = await getToken();
      if (token) setUserToken(token);
      setLoading(false);
    };
    loadToken();
  }, []);

  const login = async (email, password) => {
    const res = await api.post("/login", { email, password });
    const token = res.data.access_token;
    await saveToken(token);
    setUserToken(token);
  };

  const register = async (email, password) => {
    await api.post("/register", { email, password });
  };

  const logout = async () => {
    await removeToken();
    setUserToken(null);
  };

  return (
    <AuthContext.Provider value={{ userToken, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
