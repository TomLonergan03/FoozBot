import defaultTheme from 'tailwindcss/defaultTheme';
import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php',
        './storage/framework/views/*.php',
        './resources/views/**/*.blade.php',
    ],

    theme: {
        extend: {
            gridTemplateColumns: {
                // Simple 16 column grid
                '16': 'repeat(16, minmax(0, 1fr))',

                // Complex site-specific column configuration
                'footer': '200px minmax(900px, 1fr) 100px',
            },
            fontFamily: {
                sans: ['Comic Sans Ms', ...defaultTheme.fontFamily.sans],
                serif: ['Georgia'],
            },
            colors: {
                'FoozbotDBlue': "#007dff",
                'FoozbotLBlue': "#6ab3ff",
            },
            backgroundImage: {
              'FoozballArena': "url('/public/images/Background2.png')",
                'foozbotmain': "url('/public/images/foozbot-main.png')",
                'placeholderbg': "url('/public/images/placeholder.jpg')",
            },
        },
    },

    plugins: [forms],
};
