// src/components/DepthMapDisplay.tsx

import React from 'react';
import styled from 'styled-components';

const ImageContainer = styled.div`
  margin-top: 30px;
`;

const DepthImage = styled.img`
  width: 480px;
  height: 360px;
  border: 2px solid #ff9800;
  border-radius: 4px;

  @media (max-width: 768px) {
    width: 100%;
    height: auto;
  }
`;

interface DepthMapDisplayProps {
  depthMap: string;
}

const DepthMapDisplay: React.FC<DepthMapDisplayProps> = ({ depthMap }) => {
  return (
    <ImageContainer>
      <h3>Depth Map</h3>
      <DepthImage src={`data:image/png;base64,${depthMap}`} alt="Depth Map" />
    </ImageContainer>
  );
};

export default DepthMapDisplay;
