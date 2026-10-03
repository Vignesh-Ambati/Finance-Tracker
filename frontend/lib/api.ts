// Normalize API_BASE so that it safely handles missing https:// and appends '/api'
let rawBase = (process.env.NEXT_PUBLIC_API_URL || '').trim().replace(/\/+$/, '');
if (rawBase && !rawBase.startsWith('http://') && !rawBase.startsWith('https://')) {
  rawBase = `https://${rawBase}`;
}
const API_BASE = rawBase ? (rawBase.endsWith('/api') ? rawBase : `${rawBase}/api`) : '/api';

async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...(options.headers as Record<string, string> || {}),
  };
  
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const res = await fetch(`${API_BASE}${cleanEndpoint}`, { ...options, headers });
  
  if (res.status === 401 && !endpoint.includes('/auth/login') && !endpoint.includes('/auth/verify-2fa')) {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
  }
  
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || data.message || 'Something went wrong');
  return data;
}

export const api = {
  auth: {
    register: (data: any) => fetchAPI('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
    login: (data: any) => fetchAPI('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
    verify2FA: (data: any) => fetchAPI('/auth/verify-2fa', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: data.temp_token ? { Authorization: `Bearer ${data.temp_token}` } : {},
    }),
    forgotPassword: (email: string) => fetchAPI('/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) }),
    resetPassword: (token: string, password: string) => fetchAPI(`/auth/reset-password/${token}`, { method: 'POST', body: JSON.stringify({ password }) }),
    getProfile: () => fetchAPI('/auth/profile'),
    updateProfile: (data: any) => fetchAPI('/auth/profile', { method: 'PUT', body: JSON.stringify(data) }),
    setup2FA: () => fetchAPI('/auth/setup-2fa'),
    enable2FA: (code: string) => fetchAPI('/auth/enable-2fa', { method: 'POST', body: JSON.stringify({ totp_code: code }) }),
    disable2FA: (password: string, code: string) => fetchAPI('/auth/disable-2fa', { method: 'POST', body: JSON.stringify({ password, totp_code: code }) }),
  },
  loans: {
    getAll: async () => {
      const res = await fetchAPI('/loans');
      return Array.isArray(res) ? res : (res.loans || []);
    },
    getById: async (id: string) => {
      const res = await fetchAPI(`/loans/${id}`);
      return res.loan ? { ...res.loan, ...res } : res;
    },
    create: (data: any) => {
      const payload = {
        ...data,
        principal_amount: data.principal_amount ?? data.principal,
      };
      return fetchAPI('/loans', { method: 'POST', body: JSON.stringify(payload) });
    },
    update: (id: string, data: any) => fetchAPI(`/loans/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    collectInterest: (id: string, data: any) => {
      const payload = {
        ...data,
        date_collected: data.date_collected ?? data.date,
      };
      return fetchAPI(`/loans/${id}/collect`, { method: 'POST', body: JSON.stringify(payload) });
    },
    close: (id: string) => fetchAPI(`/loans/${id}/close`, { method: 'POST' }),
  },
  borrowers: {
    getAll: () => fetchAPI('/borrowers'),
    getById: (id: string) => fetchAPI(`/borrowers/${id}`),
    create: (data: any) => fetchAPI('/borrowers', { method: 'POST', body: JSON.stringify(data) }),
    update: (id: string, data: any) => fetchAPI(`/borrowers/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  },
  notifications: {
    getAll: () => fetchAPI('/notifications'),
    markRead: (id: string) => fetchAPI(`/notifications/${id}/read`, { method: 'POST' }),
    markAllRead: () => fetchAPI('/notifications/read-all', { method: 'POST' }),
  },
};