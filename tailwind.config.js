/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        // Primary brand colors
        primary: '#ffb3fd',
        'primary-dark': '#e89dd8',

        // Accent colors
        accent: {
          DEFAULT: '#4d1849',
          secondary: '#e8a4d8',
          hover: '#5d1e59',
        },

        // Background colors
        bg: {
          primary: '#0d0d0d',
          secondary: '#2a0d29',
          tertiary: '#1e1e1e',
        },

        // Text colors
        text: {
          primary: '#e8d4f0',
          secondary: '#ffbffd',
          tertiary: 'rgba(232, 212, 240, 0.6)',
        },

        // Border colors
        border: {
          primary: 'rgba(255, 179, 253, 0.3)',
          hover: 'rgba(255, 179, 253, 0.5)',
          light: 'rgba(255, 255, 255, 0.2)',
          subtle: 'rgba(255, 255, 255, 0.15)',
          focus: 'rgba(255, 255, 255, 0.3)',
        },

        // Overlay colors
        overlay: {
          dark: 'rgba(42, 13, 41, 0.7)',
          darker: 'rgba(42, 13, 41, 0.5)',
        },

        // Input colors
        input: {
          bg: 'rgba(61, 35, 82, 0.4)',
          focus: 'rgba(61, 35, 82, 0.6)',
        },

        // Status colors
        success: '#4ade80',
        error: '#ef4444',
      },

      fontFamily: {
        display: ['Instrument Serif', 'serif'],
        body: ['Fustat', 'sans-serif'],
        code: ['Roboto Mono', 'monospace'],
      },

      fontSize: {
        'xs': '13px',
        'sm': '14px',
        'base': '16px',
        'md': '17px',
        'lg': '18px',
        'xl': '22px',
        '2xl': '24px',
        '3xl': '32px',
        '4xl': '36px',
        '5xl': '48px',
      },

      spacing: {
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '7': '28px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
      },

      borderRadius: {
        'sm': '4px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        'full': '9999px',
      },

      boxShadow: {
        'sm': '0 1px 2px rgba(0, 0, 0, 0.1)',
        'md': '0 4px 6px rgba(0, 0, 0, 0.2)',
        'lg': '0 10px 20px rgba(0, 0, 0, 0.3)',
        'glow': '0 0 20px rgba(232, 164, 216, 0.4)',
        'glow-strong': '0 8px 24px rgba(232, 164, 216, 0.5)',
        'focus': '0 0 0 3px rgba(232, 164, 216, 0.15)',
      },

      transitionDuration: {
        'fast': '150ms',
        'base': '300ms',
        'slow': '500ms',
      },

      animation: {
        'fade-in': 'fadeIn 0.4s ease-in',
        'float': 'float 3s ease-in-out infinite',
        'spin': 'spin 1s linear infinite',
      },

      keyframes: {
        fadeIn: {
          'from': { opacity: '0', transform: 'translateY(15px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
}
