/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand': '#F5A623',
        'brand-dark': '#E09612',
        'sidebar': '#1B2129',
        'panel': '#212833',
        'border': '#2E3844',
        'danger': '#E74C3C',
        'success': '#2ECC71',
        'warning': '#F1C40F',
        'info': '#3498DB',

        // Heinrich Pyramid Colors
        'hp-blue': '#00AEEF',
        'hp-pink': '#EC008C',
        'hp-teal': '#00BFA5',
        'hp-yellow': '#FFB300',
        'hp-purple': '#6A1B9A',
      }
    },
  },
  plugins: [],
}
