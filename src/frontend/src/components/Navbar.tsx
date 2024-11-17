// src/components/Navbar.tsx

import React from 'react';
import { NavLink } from 'react-router-dom';
import styled from 'styled-components';

const Nav = styled.nav`
  background-color: #333;
  padding: 10px 20px;
`;

const NavList = styled.ul`
  list-style: none;
  display: flex;
  gap: 20px;
`;

const NavItem = styled.li``;

const StyledNavLink = styled(NavLink)`
  color: white;
  text-decoration: none;
  font-weight: bold;
  
  &.active {
    text-decoration: underline;
  }
  
  &:hover {
    color: #ddd;
  }
`;

const Navbar: React.FC = () => {
  return (
    <Nav>
      <NavList>
        <NavItem>
          <StyledNavLink to="/" end>
            Image Upload
          </StyledNavLink>
        </NavItem>
        <NavItem>
          <StyledNavLink to="/camera-stream">
            Camera Stream
          </StyledNavLink>
        </NavItem>
        {/* Add more navigation links here if needed */}
      </NavList>
    </Nav>
  );
};

export default Navbar;
