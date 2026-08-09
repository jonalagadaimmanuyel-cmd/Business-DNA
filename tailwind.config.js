export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f7faf6',
          100: '#eef6eb',
          200: '#d7ebd4',
          300: '#b8ddaf',
          400: '#8fc17e',
          500: '#62a651',
          600: '#4e843f',
          700: '#3e6934',
          800: '#335427',
          900: '#2a4620'
        },
        warning: '#f7b84b',
        orange: '#f29f49',
        signal: {
          good: '#28a745',
          watch: '#f0b429',
          alert: '#f97316',
          bad: '#ef4444'
        }
      },
      boxShadow: {
        soft: '0 18px 45px rgba(15, 23, 42, 0.08)',
        card: '0 10px 30px rgba(15, 23, 42, 0.08)'
      },
      borderRadius: {
        xl: '1.25rem'
      }
    }
  },
  plugins: []
}
