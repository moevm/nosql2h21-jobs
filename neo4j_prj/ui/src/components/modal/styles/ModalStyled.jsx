import { css } from '@emotion/react';
import styled from '@emotion/styled';

export const Backdrop = styled.div`
  z-index: 1;
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  opacity: 0;

  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(6px);

  transition: opacity 0.2s ease-in-out;

  ${({ isActive }) =>
    isActive &&
    css`
      opacity: 1;
    `}
`;

export const ModalContent = styled.div`
  position: relative;
  height: 50vh;
  width: 60vw;
  padding: 20px;
  background-color: #fff;
  border: 4px solid grey;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

export const ModalBackdrop = styled(Backdrop)`
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const ModalTitle = styled.h1`
  font-family: inherit;
  padding: 0;
  margin: 0;
  font-size: 18px;
  color: #ffffff;
`;
