module.exports = {
  content: [
    './main/templates/**/*.html',
    './templates/**/*.html',
    './main/**/*.js',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'primary': {
          DEFAULT: '#2563eb',
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#2563eb',
          600: '#1d4ed8',
          900: '#1e3a8a',
        },
        'navy': {
          DEFAULT: '#1e3a8a',
          800: '#1e40af',
          900: '#1e3a8a',
        }
      },
      fontFamily: {
        'sans': ['Roboto', 'Poppins', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}