import { useEffect, useRef, useState } from 'react';

const ROOT_ELEMENT = 'app';

export function usePortal({ open, onClose }) {
  const [active, setActive] = useState(false);
  const backdrop = useRef(null);

  useEffect(() => {
    const { current } = backdrop;
    const transitionEnd = () => setActive(open);
    const keyHandler = (e) => {
      if (e.code === 'Escape' && open && onClose) {
        onClose();
      }
    };

    const clickHandler = (e) => {
      if (e.target === current && onClose) {
        onClose();
      }
    };

    current?.addEventListener('transitionend', transitionEnd);

    current?.addEventListener('click', clickHandler);

    window.addEventListener('keyup', keyHandler);

    let timeout = -1;

    if (open) {
      timeout = window.setTimeout(() => {
        setActive(open);
      }, 10);
    }

    return () => {
      current?.removeEventListener('transitionend', transitionEnd);

      current?.removeEventListener('click', clickHandler);

      timeout && clearTimeout(timeout);

      window.removeEventListener('keyup', keyHandler);
    };
  }, [open, onClose, backdrop]);

  return {
    ref: backdrop,
    active,
  };
}
