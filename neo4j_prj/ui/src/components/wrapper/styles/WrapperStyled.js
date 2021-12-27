import { css } from '@emotion/react';
import styled from '@emotion/styled';
import { Router } from '@reach/router';

import { background } from '../../../assets/background';

export const WrapperStyled = styled(Router)`
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;

  max-height: 1080px;
  max-width: 1920px;
`;

export const GlobalStyles = css`
  * {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    font-family: inherit !important;
  }

  body {
    width: 100%;
    font-family: 'Bitter', serif !important;

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
