<!DOCTYPE html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Foozbot Website</title>

    <!-- Fonts -->

    <!-- Styles -->

    <!-- Scripts -->
    @vite(['resources/css/app.css', 'resources/js/app.js'])

</head>
<body class="bg-gradient-to-l from-FoozbotDBlue to-blue-900 font-mono lg:text-base xl:text-xl text-xs min-h-full">
<x-navbar/>

        {{ $slot }}

<x-footer/>

    @if (session()->has('passed'))
    <div class = 'bg-blue-500 fixed text-white py-2 px-4 rounded-xl bottom-3 right-3 text-sm'>
        <p> {{session()->get('passed')}} </p>
    </div>
    @endif

</body>
</html>
