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
<body class="bg-gradient-to-l from-FoozbotDBlue to-FoozbotLBlue font-serif font-semibold">

<!-- Bar-->
<div class="rounded-3xl border border-black border-1 m-1 static inset-x-0 top-0 max-h-52 bg-gradient-to-bl from-stone-300 to-stone-400 p-6">
    <img class="border static m-12" src="images/FoozBotLogo.png">
</div>

    {{ $slot }}

<x-footer/>

@if (session()->has('passed'))
<div class = 'bg-blue-500 fixed text-white py-2 px-4 rounded-xl bottom-3 right-3 text-sm'>
    <p> {{session()->get('passed')}} </p>
</div>
@endif

</body>
</html>
