import { useState } from 'react';
import axios from 'axios';

interface ChatMessage {
  text: string;
  isUser: boolean;
}

interface UseDepthGPTReturn {
  sendDepthGPTRequest: (file: File, prompt: string) => Promise<void>;
  depthMap: string | null;
  rgbImage: string | null;
  lvlmResponse: string | null;
  chatHistory: ChatMessage[];
  loading: boolean;
  error: string | null;
}

export function useDepthGPT(): UseDepthGPTReturn {
  const [depthMap, setDepthMap] = useState<string | null>(null);
  const [rgbImage, setRgbImage] = useState<string | null>(null);
  const [lvlmResponse, setLvlmResponse] = useState<string | null>(null);
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const sendDepthGPTRequest = async (file: File, prompt: string) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('prompt', prompt);

      // Update chat history with user's message
      setChatHistory((prev) => [...prev, { text: prompt, isUser: true }]);

      const response = await axios.post('/depthgpt', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const data = response.data;
      setDepthMap(data.depth_map);
      setRgbImage(data.rgb_image);
      setLvlmResponse(data.lvlm_response);

      // Update chat history with LVLM's response
      setChatHistory((prev) => [...prev, { text: data.lvlm_response, isUser: false }]);
    } catch (err: any) {
      console.error('Error in sendDepthGPTRequest:', err);
      setError(err.response?.data?.detail || 'Error processing the request.');
    } finally {
      setLoading(false);
    }
  };

  return {
    sendDepthGPTRequest,
    depthMap,
    rgbImage,
    lvlmResponse,
    chatHistory,
    loading,
    error,
  };
}
