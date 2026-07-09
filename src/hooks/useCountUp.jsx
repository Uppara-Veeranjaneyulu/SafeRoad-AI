import { useState, useEffect, useRef } from 'react';

export default function CountUp({ end, start = 0, duration = 2, decimals = 0, prefix = '', suffix = '' }) {
  const [count, setCount] = useState(start);
  const countRef = useRef(start);
  const startTimeRef = useRef(null);
  const rafRef = useRef(null);
  const hasStarted = useRef(false);

  const elementRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasStarted.current) {
          hasStarted.current = true;
          const animate = (timestamp) => {
            if (!startTimeRef.current) startTimeRef.current = timestamp;
            const elapsed = timestamp - startTimeRef.current;
            const progress = Math.min(elapsed / (duration * 1000), 1);
            // Easing: ease-out-expo
            const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
            countRef.current = start + (end - start) * eased;
            setCount(countRef.current);
            if (progress < 1) {
              rafRef.current = requestAnimationFrame(animate);
            } else {
              setCount(end);
            }
          };
          rafRef.current = requestAnimationFrame(animate);
        }
      },
      { threshold: 0.3 }
    );
    if (elementRef.current) observer.observe(elementRef.current);
    return () => {
      observer.disconnect();
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [end, start, duration]);

  const display = decimals > 0
    ? count.toFixed(decimals)
    : Math.floor(count).toLocaleString();

  return (
    <span ref={elementRef}>
      {prefix}{display}{suffix}
    </span>
  );
}
