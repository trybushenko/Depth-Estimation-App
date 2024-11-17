// src/components/ErrorMessage.tsx

import React from 'react';
import styled from 'styled-components';

const ErrorText = styled.p`
  color: red;
  margin-top: 20px;
`;

interface ErrorMessageProps {
  children: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ children }) => {
  return <ErrorText>{children}</ErrorText>;
};

export default ErrorMessage;
