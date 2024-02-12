<!-- Bar-->
<div class="rounded-3xl border border-black border-1 m-1 sticky inset-x-0 top-0 max-h-52 bg-gradient-to-bl from-stone-300 to-stone-400 font-semibold font-serif z-10">

    <div class="grid gap-x-2 gap-y-1 grid-cols-8 grid-rows-2 m-2">
        <!-- You must be the change you wish to see in the world. - Mahatma Gandhi -->

        <!-- Row 1-->
        <!-- 1-->
        <div class="col-span-2">
            <a href="/"><img class="min-h-20 min-w-80 " src="/images/FoozBotLogo.png"></a>
        </div>

        <!-- 2, 3, 4, 5 -->
        <div id="title" class="col-span-4 justify-center w-5/6 place-self-center">
            <h1 class="text-center p-4 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-lg bg-FoozbotLBlue">Welcome To Foozbot</h1>
        </div>

        <!-- 6,7 -->
        @auth
            <div class="place-self-center col-span-2 ">
                <a href="/myAccount" class="text-center p-4 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-lg bg-FoozbotLBlue inline hover:bg-FoozbotDBlue">Welcome {{auth()->user()->username}}</a>
                <form method="post" action="/logout" class="inline">@csrf<input class=" text-center p-3 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-xl bg-FoozbotLBlue hover:cursor-pointer hover:bg-FoozbotDBlue inline" type="submit" value="logout"></form>
            </div>
        @endauth

        @guest
        <div class="place-self-center col-span-2 ">
            <a href="/login" class="text-center p-4 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-lg bg-FoozbotLBlue inline hover:bg-FoozbotDBlue">Log In</a>
            <a href="/register" class="text-center p-4 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-lg bg-FoozbotLBlue inline hover:bg-FoozbotDBlue">Register</a>
        </div>
        @endguest

        <!-- Row 2-->
        <!-- 1, 2 -->
        <div id="logo" class="col-span-2">
        </div>

        <!-- 3 -->
        <a href="/aboutUs">
            <h1 class="text-center p-4 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-lg bg-FoozbotLBlue hover:bg-FoozbotDBlue">About Us</h1>
        </a>

        <!-- 4 -->
        <a href="/records">
            <h1 class="text-center p-4 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-lg bg-FoozbotLBlue hover:bg-FoozbotDBlue">Records</h1>
        </a>

        <!-- 5 -->
        <a href="/guides/none">
            <h1 class="text-center p-4 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-lg bg-FoozbotLBlue hover:bg-FoozbotDBlue">Guides</h1>
        </a>

        <!-- 6 -->
        <a href="/buy">
            <h1 class="text-center p-4 overflow-hidden border-double border-2 border-stone-500 rounded-2xl shadow-lg bg-FoozbotLBlue hover:bg-FoozbotDBlue">Buy</h1>
        </a>

        <!-- 7, 8 -->
        <div class="col-span-2">
        </div>

    </div>
</div>

