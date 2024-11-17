// src/components/CameraStreamPage.tsx

import React from 'react';
import styled from 'styled-components';
import CameraStream from './CameraStream';
import DepthMapDisplay from './DepthMapDisplay'; // Ensure this component exists
import { useDepthPrediction } from '../hooks/useDepthPrediction'; // Correct import
import ErrorMessage from './ErrorMessage'; // Ensure this component exists

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
  const {
    predictDepthFromBase64,
    depthMap,
    loading,
    error,
  } = useDepthPrediction();

  return (
    <PageContainer>
      <Title>Real-Time Camera Stream for Depth Prediction</Title>
      
      <CameraStream
        predictDepthFromBase64={predictDepthFromBase64}
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
