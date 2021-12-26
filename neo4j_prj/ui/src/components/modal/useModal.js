import { useCallback, useState } from 'react';

export function useModal() {
  const [isModalOpened, setModalOpened] = useState(false);

  const handleModalOpen = useCallback(() => setModalOpened(true), []);
  const handleModalClose = useCallback(() => setModalOpened(false), []);

  return {
    isModalOpened,
    handleModalOpen,
    handleModalClose,
  };
}
