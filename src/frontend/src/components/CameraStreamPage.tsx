// src/frontend/pages/CameraStreamPage.tsx
import styled from 'styled-components';
import React from 'react';
import CameraStream from '../components/CameraStream';
import { useDepthPrediction } from '../hooks/useDepthPrediction';
import ErrorMessage from './ErrorMessage'; // Ensure this component exists
import DepthMapDisplay from './DepthMapDisplay'; // Ensure this component exists

const PageContainer = styled.div`
  max-width: 1000px;
  margin: 40px auto;
  padding: 20px;
  text-align: center;
  font-family: Arial, sans-serif;
`;

const Title = styled.h1`
  color: #333;
  margin-bottom: 20px;
`;

const CameraStreamPage: React.FC = () => {
  const { predictDepthFromFile, depthMap, loading, error } = useDepthPrediction();

  return (
    <PageContainer>
      <Title>Real-Time Camera Stream for Depth Prediction</Title>
      
      <CameraStream
        predictDepthFromFile={predictDepthFromFile}
        loading={loading}
        error={error}
      />
      
      {/* Remove the loading spinner from the stream page */}
      
      {error && <ErrorMessage>{error}</ErrorMessage>}
      
      {depthMap && (
        <DepthMapDisplay depthMap={depthMap} />
      )}
    </PageContainer>
  );
};

export default CameraStreamPage;
