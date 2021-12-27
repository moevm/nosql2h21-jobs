import { createContext, useContext } from 'react';

import { Portal, usePortal } from '../portal';
import { ModalBackdrop, ModalContent } from './styles';

const ModalContext = createContext(undefined);

export function useModalProps() {
  const context = useContext(ModalContext);

  if (!context) {
    throw new Error();
  }

  return context;
}

export function Modal({ open, onClose, children, big = false }) {
  const { ref, active } = usePortal({ open, onClose });

  return (
    <ModalContext.Provider value={{ open, onClose }}>
      {(open || active) && (
        <Portal>
          <ModalBackdrop ref={ref} isActive={active && open}>
            <ModalContent big={big}>{children}</ModalContent>
          </ModalBackdrop>
        </Portal>
      )}
    </ModalContext.Provider>
  );
}
