// src/components/ImageUploadPage.tsx

import React, { useState } from 'react';
import styled from 'styled-components';
import { useDepthPrediction } from '../hooks/useDepthPrediction';
import LoadingSpinner from './LoadingSpinner';
import DepthMapDisplay from './DepthMapDisplay'; // Ensure this component exists
import ErrorMessage from './ErrorMessage'; // Ensure this component exists

const PageContainer = styled.div`
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  text-align: center;
  font-family: Arial, sans-serif;
`;

const Title = styled.h1`
  color: #333;
  margin-bottom: 20px;
`;

const FileInput = styled.input`
  margin-bottom: 20px;
`;

const ProcessButton = styled.button<{ disabled: boolean }>`
  padding: 10px 20px;
  font-size: 16px;
  background-color: ${({ disabled }) => (disabled ? '#9e9e9e' : '#4caf50')};
  color: white;
  border: none;
  border-radius: 4px;
  cursor: ${({ disabled }) => (disabled ? 'not-allowed' : 'pointer')};
  
  &:hover {
    background-color: ${({ disabled }) => (disabled ? '#9e9e9e' : '#45a049')};
  }
`;

const ImageUploadPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const { predictDepthFromFile, depthMap, loading, error } = useDepthPrediction();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];

      // Validate file type
      if (!['image/jpeg', 'image/png', 'image/jpg'].includes(file.type)) {
        alert('Unsupported file type. Please upload a JPEG or PNG image.');
        setSelectedFile(null);
        setPreviewUrl(null);
        return;
      }

      // Validate file size (e.g., max 5MB)
      const maxSizeMB = 5;
      if (file.size > maxSizeMB * 1024 * 1024) {
        alert(`File size exceeds ${maxSizeMB}MB.`);
        setSelectedFile(null);
        setPreviewUrl(null);
        return;
      }

      setSelectedFile(file);

      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    } else {
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  };

  const handleProcessClick = async () => {
    if (selectedFile) {
      await predictDepthFromFile(selectedFile);
    }
  };

  return (
    <PageContainer>
      <Title>Upload Image for Depth Prediction</Title>
      
      <FileInput
        type="file"
        accept="image/*"
        onChange={handleFileChange}
      />
      
      <br />
      
      <ProcessButton
        onClick={handleProcessClick}
        disabled={!selectedFile || loading}
      >
        {loading ? 'Processing...' : 'Process'}
      </ProcessButton>
      
      {/* Display Loading Spinner Only Here */}
      {loading && <LoadingSpinner loading={loading} />}
      
      {/* Display Error Message Only Here */}
      {error && <ErrorMessage>{error}</ErrorMessage>}
      
      {/* Display Depth Map Only Here */}
      {depthMap && <DepthMapDisplay depthMap={depthMap} />}
    </PageContainer>
  );
};

export default ImageUploadPage;
