const styles = {
  info: "color: #3b82f6; font-weight: bold;",
  success: "color: #22c55e; font-weight: bold;",
  warn: "color: #eab308; font-weight: bold;",
  error: "color: #ef4444; font-weight: bold;",
};

function timestamp() {
  return new Date().toLocaleTimeString();
}

export const logger = {
  info: (label, ...args) => {
    console.log(`%c[${timestamp()}] ℹ ${label}`, styles.info, ...args);
  },
  success: (label, ...args) => {
    console.log(`%c[${timestamp()}] ✅ ${label}`, styles.success, ...args);
  },
  warn: (label, ...args) => {
    console.warn(`%c[${timestamp()}] ⚠ ${label}`, styles.warn, ...args);
  },
  error: (label, ...args) => {
    console.error(`%c[${timestamp()}] ❌ ${label}`, styles.error, ...args);
  },
  group: (label, fn) => {
    console.groupCollapsed(`%c[${timestamp()}] ${label}`, styles.info);
    fn();
    console.groupEnd();
  },
};