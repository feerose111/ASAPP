const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8088';

const api = {
  createProject: async (data) => {
    const response = await fetch(`${API_URL}/create_project`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create project');
    return response.json();
  },

  sendMessage: async (message) => {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  },
};

export default api;