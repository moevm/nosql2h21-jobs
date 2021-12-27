import { css, Global } from '@emotion/react';
import styled from '@emotion/styled';
import { Router } from '@reach/router';

import { Helmet } from 'react-helmet';

import { GlobalStyles, WrapperStyled } from './styles';

export function Wrapper({ children }) {
  return (
    <>
      <Helmet>
        <link href="https://fonts.googleapis.com" rel="preconnect" />
        <link crossOrigin href="https://fonts.gstatic.com" rel="preconnect" />
        <link
          href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </Helmet>
      <Global styles={GlobalStyles} />
      <WrapperStyled>{children}</WrapperStyled>
    </>
  );
}
