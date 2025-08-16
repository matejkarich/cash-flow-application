import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth tokens (if needed)
api.interceptors.request.use((config) => {
  // Add auth token if available
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Visualization endpoints
  getDashboardData: async (params: any) => {
    const response = await api.get('/api/v1/visualizations/dashboard', { params });
    return response.data;
  },

  getSankeyDiagram: async (params: any) => {
    const response = await api.get('/api/v1/visualizations/sankey-diagram', { params });
    return response.data;
  },

  getSpendingPieChart: async (params: any) => {
    const response = await api.get('/api/v1/visualizations/spending-pie-chart', { params });
    return response.data;
  },

  getMonthlyTrends: async (params: any) => {
    const response = await api.get('/api/v1/visualizations/monthly-trends', { params });
    return response.data;
  },

  getCreditCardUsage: async (params: any) => {
    const response = await api.get('/api/v1/visualizations/credit-card-usage', { params });
    return response.data;
  },

  // Import endpoints
  importFromGoogleSheets: async (data: FormData) => {
    const response = await api.post('/api/v1/imports/google-sheets', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  importFromCSV: async (data: FormData) => {
    const response = await api.post('/api/v1/imports/csv-upload', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  validateImportFormat: async (data: FormData) => {
    const response = await api.post('/api/v1/imports/validate-format', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getCSVTemplate: async () => {
    const response = await api.get('/api/v1/imports/templates/csv');
    return response.data;
  },

  // Transaction endpoints
  getTransactions: async (params: any) => {
    const response = await api.get('/api/v1/transactions', { params });
    return response.data;
  },

  createTransaction: async (transaction: any) => {
    const response = await api.post('/api/v1/transactions', transaction);
    return response.data;
  },

  updateTransaction: async (id: string, transaction: any) => {
    const response = await api.put(`/api/v1/transactions/${id}`, transaction);
    return response.data;
  },

  deleteTransaction: async (id: string) => {
    const response = await api.delete(`/api/v1/transactions/${id}`);
    return response.data;
  },

  // Category endpoints
  getCategories: async (params: any) => {
    const response = await api.get('/api/v1/categories', { params });
    return response.data;
  },

  createCategory: async (category: any) => {
    const response = await api.post('/api/v1/categories', category);
    return response.data;
  },

  updateCategory: async (id: string, category: any) => {
    const response = await api.put(`/api/v1/categories/${id}`, category);
    return response.data;
  },

  deleteCategory: async (id: string) => {
    const response = await api.delete(`/api/v1/categories/${id}`);
    return response.data;
  },

  getCategoryTree: async (params: any) => {
    const response = await api.get('/api/v1/categories/tree', { params });
    return response.data;
  },

  // Credit Card endpoints
  getCreditCards: async (params: any) => {
    const response = await api.get('/api/v1/credit-cards', { params });
    return response.data;
  },

  createCreditCard: async (card: any) => {
    const response = await api.post('/api/v1/credit-cards', card);
    return response.data;
  },

  updateCreditCard: async (id: string, card: any) => {
    const response = await api.put(`/api/v1/credit-cards/${id}`, card);
    return response.data;
  },

  deleteCreditCard: async (id: string) => {
    const response = await api.delete(`/api/v1/credit-cards/${id}`);
    return response.data;
  },

  calculateRewards: async (params: any) => {
    const response = await api.get('/api/v1/credit-cards/calculate-rewards', { params });
    return response.data;
  },

  compareCards: async (params: any) => {
    const response = await api.get('/api/v1/credit-cards/compare', { params });
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService;