import React, { createContext, useState, useEffect } from 'react';
import authService from '../services/authService';

export const AuthContext = createContext({
  user: null,
  login: async () => {},
  register: async () => {},
  logout: async () => {},
  updateProfile: async () => {},
  changePassword: async () => {},
  loading: true,
});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      authService.getCurrentUser()
        .then(userData => setUser(userData))
        .catch(() => logout())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    const data = await authService.login(email, password);
    localStorage.setItem('access_token', data.access_token);
    setUser(data.user);
    return data;
  };

  const register = async (name, email, password, confirmPassword, role) => {
    const data = await authService.register(name, email, password, confirmPassword, role);
    return data;
  };

  const logout = async () => {
    await authService.logout();
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const updateProfile = async (profileData) => {
    const data = await authService.updateProfile(profileData);
    setUser(data.user);
    return data;
  };

  const changePassword = async (currentPassword, newPassword, confirmPassword) => {
    const data = await authService.changePassword(currentPassword, newPassword, confirmPassword);
    return data;
  };

  return (
    <AuthContext.Provider value={{
      user,
      login,
      register,
      logout,
      updateProfile,
      changePassword,
      loading,
    }}>
      {children}
    </AuthContext.Provider>
  );
};
