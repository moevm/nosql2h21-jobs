import { css } from '@emotion/react';
import styled from '@emotion/styled';
import { Router } from '@reach/router';

import { background } from '../../../assets/background';

export const WrapperStyled = styled(Router)`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const GlobalStyles = css`
  * {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    font-family: 'Roboto', sans-serif !important;
    font-size: 14px;
    font-weight: 400;
  }

  body {
    width: 100%;
    font-family: 'Roboto', sans-serif !important;

    background-image: url(${background});
    background-size: auto 100%;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-color: #f8d297;
  }

  @media only screen and (min-width: 1921px) {
    body {
      display: flex;
      justify-content: center;
      background-size: contain;
    }
  }
`;
