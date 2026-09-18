/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        canvas: '#0A0F1C',
        surface: '#111A2C',
        elevated: '#16213A',
        hairline: '#22314F',
        'hairline-soft': '#1B2740',
        ink: '#EEF2FA',
        muted: '#8C9AB8',
        faint: '#5E6C8C',
        india: {
          DEFAULT: '#EE9B3A',
          soft: 'rgba(238,155,58,0.14)',
          line: 'rgba(238,155,58,0.35)',
        },
        malaysia: {
          DEFAULT: '#2FBF9F',
          soft: 'rgba(47,191,159,0.14)',
          line: 'rgba(47,191,159,0.35)',
        },
        signal: '#7C9CFF',
      },
      fontFamily: {
        display: ['"Sora"', 'system-ui', 'sans-serif'],
        body: ['"Inter"', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        sm: '6px',
        md: '10px',
        lg: '16px',
        xl: '22px',
      },
      boxShadow: {
        subtle: '0 1px 0 rgba(255,255,255,0.03) inset',
      },
    },
  },
  plugins: [],
}
