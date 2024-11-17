// src/components/LoadingSpinner.tsx

import React from 'react';
import { ClipLoader } from 'react-spinners';
import styled from 'styled-components';

const SpinnerContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
`;

interface LoadingSpinnerProps {
  loading: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ loading }) => {
  return (
    <SpinnerContainer>
      <ClipLoader color="#2196f3" loading={loading} size={50} />
    </SpinnerContainer>
  );
};

export default LoadingSpinner;
