import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Workflow API
export const getWorkflows = async () => {
  const response = await apiClient.get('/workflow/');
  return response.data;
};

export const getWorkflow = async (id) => {
  const response = await apiClient.get(`/workflow/${id}`);
  return response.data;
};

export const createWorkflow = async (data) => {
  const response = await apiClient.post('/workflow/', data);
  return response.data;
};

export const updateWorkflow = async (id, data) => {
  const response = await apiClient.put(`/workflow/${id}`, data);
  return response.data;
};

export const deleteWorkflow = async (id) => {
  const response = await apiClient.delete(`/workflow/${id}`);
  return response.data;
};

export const validateWorkflow = async (id) => {
  const response = await apiClient.post(`/workflow/${id}/validate`);
  return response.data;
};

// Application API
export const getApplications = async (params = {}) => {
  const response = await apiClient.get('/application/', { params });
  return response.data;
};

export const getApplication = async (id) => {
  const response = await apiClient.get(`/application/${id}`);
  return response.data;
};

export const createApplication = async (data) => {
  const response = await apiClient.post('/application/', data);
  return response.data;
};

export const executeApplication = async (id) => {
  const response = await apiClient.post(`/application/${id}/execute`);
  return response.data;
};

export const getApplicationLogs = async (id) => {
  const response = await apiClient.get(`/application/${id}/logs`);
  return response.data;
};

// Engine API
export const getRules = async () => {
  const response = await apiClient.get('/engine/rules');
  return response.data;
};

export const createRule = async (data) => {
  const response = await apiClient.post('/engine/rules', data);
  return response.data;
};

export const updateRule = async (id, data) => {
  const response = await apiClient.put(`/engine/rules/${id}`, data);
  return response.data;
};

export const deleteRule = async (id) => {
  const response = await apiClient.delete(`/engine/rules/${id}`);
  return response.data;
};

export const calculateScore = async (data) => {
  const response = await apiClient.post('/engine/score', data);
  return response.data;
};

export default apiClient;
