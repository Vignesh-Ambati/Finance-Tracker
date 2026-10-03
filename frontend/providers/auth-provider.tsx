'use client'
import React, { createContext, useContext, useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { getToken, setToken, removeToken, isAuthenticated as checkIsAuth } from '@/lib/auth';

type AuthContextType = {
  user: any;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
};

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    const initAuth = async () => {
      const authStatus = checkIsAuth();
      setIsAuth(authStatus);
      if (authStatus) {
        try {
          const res = await api.auth.getProfile();
          setUser(res);
        } catch (e) {
          removeToken();
          setIsAuth(false);
        }
      }
      setIsLoading(false);
    };
    initAuth();
  }, []);

  const login = (token: string) => {
    setToken(token);
    window.location.href = '/dashboard';
  };

  const logout = () => {
    removeToken();
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, token: getToken(), isLoading, isAuthenticated: isAuth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}