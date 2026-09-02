import api from './api';

export const authService = {
  login: async (email, password) => {
    const res = await api.post('/auth/login', { email, password });
    return res.data;
  },

  register: async (name, email, password, confirmPassword, role = 'sales_rep') => {
    const res = await api.post('/auth/register', {
      name,
      email,
      password,
      confirm_password: confirmPassword,
      role,
    });
    return res.data;
  },

  logout: async () => {
    try {
      await api.post('/auth/logout');
    } catch {
      // Ignore network/server errors during logout
    }
  },

  getCurrentUser: async () => {
    const res = await api.get('/auth/me');
    return res.data;
  },

  updateProfile: async (profileData) => {
    const res = await api.put('/users/me', profileData);
    return res.data;
  },

  changePassword: async (currentPassword, newPassword, confirmPassword) => {
    const res = await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
      confirm_password: confirmPassword,
    });
    return res.data;
  },
};

export default authService;
