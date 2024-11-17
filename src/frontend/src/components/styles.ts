// src/components/styles.ts

import styled from 'styled-components';

export const PageContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
`;

export const Title = styled.h1`
  text-align: center;
  color: #333;
`;

export const Input = styled.input`
  display: block;
  margin: 20px auto;
  padding: 10px;
  font-size: 16px;
`;

export const Button = styled.button`
  display: block;
  margin: 10px auto;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;

  &:disabled {
    background-color: #9e9e9e;
    cursor: not-allowed;
  }
`;

export const ErrorMessage = styled.p`
  color: red;
  text-align: center;
`;

export const ImageContainer = styled.div`
  text-align: center;
  margin: 20px 0;
`;

export const DepthImage = styled.img`
  max-width: 100%;
  height: auto;
  border: 2px solid #2196f3;
  border-radius: 4px;
`;

export const WebcamContainer = styled.div`
  display: flex;
  justify-content: center;
  margin: 20px 0;
`;

export const NavbarContainer = styled.nav`
  background-color: #333;
  padding: 10px;
`;

export const StyledLink = styled.a<{ active?: boolean }>`
  color: #fff;
  margin-right: 10px;
  text-decoration: none;
  font-weight: ${(props) => (props.active ? 'bold' : 'normal')};

  &:hover {
    text-decoration: underline;
  }
`;
