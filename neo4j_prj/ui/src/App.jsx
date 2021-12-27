import { ChakraProvider } from '@chakra-ui/react';

import { Wrapper } from './components';
import { List, Main } from './pages';

export function App() {
  return (
    <ChakraProvider>
      <Wrapper>
        <List path="/list" />
        <Main path="/" />
      </Wrapper>
    </ChakraProvider>
  );
}
