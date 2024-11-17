// src/frontend/src/api.js

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const fetchDepthMap = async (data) => {
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  return response.json();
};
