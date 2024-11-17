// src/hooks/useDepthPrediction.ts

import { useState } from 'react';
import axios from 'axios';
import imageCompression from 'browser-image-compression';

interface UseDepthPredictionReturn {
  predictDepthFromFile: (file: File) => Promise<void>;
  predictDepthFromBase64: (base64Image: string) => Promise<void>;
  depthMap: string;
  loading: boolean;
  error: string | null;
}

export function useDepthPrediction(): UseDepthPredictionReturn {
  const [depthMap, setDepthMap] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Function to handle file uploads (used in ImageUploadPage)
  const predictDepthFromFile = async (file: File) => {
    setLoading(true);
    setError(null);
    try {
      // Compress the image file to reduce payload size
      const options = {
        maxSizeMB: 1, // Maximum size in MB
        maxWidthOrHeight: 800, // Max width or height
        useWebWorker: true, // Use Web Workers for better performance
      };
      const compressedFile = await imageCompression(file, options);

      const formData = new FormData();
      formData.append('file', compressedFile);

      // Adjust the baseURL if your backend is hosted elsewhere
      const response = await axios.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.depth_map) {
        setDepthMap(response.data.depth_map);
      } else {
        setError('No depth map returned from the server.');
      }
    } catch (err: any) {
      console.error('Error in predictDepthFromFile:', err);
      setError(err.response?.data?.detail || 'Error processing the image.');
    } finally {
      setLoading(false);
    }
  };

  // Function to handle base64-encoded image uploads (used in CameraStreamPage)
  const predictDepthFromBase64 = async (base64Image: string) => {
    setLoading(true);
    setError(null);
    try {
      const payload = { image: base64Image };

      // Adjust the baseURL if your backend is hosted elsewhere
      const response = await axios.post('/predict', payload, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.data.depth_map) {
        setDepthMap(response.data.depth_map);
      } else {
        setError('No depth map returned from the server.');
      }
    } catch (err: any) {
      console.error('Error in predictDepthFromBase64:', err);
      setError(err.response?.data?.detail || 'Error processing the image.');
    } finally {
      setLoading(false);
    }
  };

  return {
    predictDepthFromFile,
    predictDepthFromBase64,
    depthMap,
    loading,
    error,
  };
}
