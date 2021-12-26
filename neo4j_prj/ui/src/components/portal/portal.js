import { useLayoutEffect, useMemo } from 'react';
import ReactDOM from 'react-dom';

export function Portal({ children }) {
  const el = useMemo(() => document.createElement('div'), []);

  useLayoutEffect(() => {
    const target = document.body;

    target.appendChild(el);

    return () => {
      target.removeChild(el);
    };
  }, [el]);

  return ReactDOM.createPortal(children, el);
}
