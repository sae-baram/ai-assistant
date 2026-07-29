/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        neutral: {
          400: '#94a3b8',
          700: '#1f2937'
        }
      }
    }
  },
  plugins: []
}
