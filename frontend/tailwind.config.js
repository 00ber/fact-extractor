/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    colors: {
		  transparent: 'transparent',
		  current: 'currentColor',
		  steelblue: {
			50: '#f4f8fb',
			100: '#e8eff6',
			200: '#cbdfec',
			300: '#9dc5dc',
			400: '#69a5c7',
			500: '#468ab1',
			600: '#346f95',
			700: '#2b5979',
			800: '#274c65',
			900: '#254055',
			950: '#111d27',
		  },    
		},
		extend: {
		  ringColor: {
			steelblue: {
				200: '#cbdfec',
				950: '#111d27'
			}
		  },
		  fontFamily: {
			silkscreen: ["Silkscreen"],
			spacemono: ["Space Mono"],
			montseratt: ["Montserrat"]
		  },
		}
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

