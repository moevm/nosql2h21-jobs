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

  ${({ isActive }) =>
    isActive &&
    css`
      opacity: 1;
    `}
`;

export const ModalContent = styled.div`
  position: relative;
  height: 100%;
  width: 100%;
  padding: 50px;
`;

export const ModalBackdrop = styled(Backdrop)`
  display: flex;
  align-items: center;
  justify-content: center;

  ${ModalContent} {
    transform: translateY(-100vh);
  }

  ${({ isActive }) =>
    isActive &&
    css`
      ${ModalContent} {
        transform: translateY(0);
      }
    `}
`;

export const ModalTitle = styled.h1`
  font-family: inherit;
  padding: 0;
  margin: 0;
  font-size: 18px;
  color: #ffffff;
`;
