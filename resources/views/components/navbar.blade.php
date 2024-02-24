<!-- Bar-->
<div class="rounded-3xl  border border-2 border-black  m-1 sticky inset-x-0 top-0 max-h-36 sm:max-h-44 md:max-h-52 bg-gradient-to-bl from-blue-900 to-FoozbotLBlue font-semibold font-serif z-10">

    <div class="grid gap-x-2 gap-y-1 lg:grid-cols-8 grid-cols-5 lg:grid-rows-2 grid-rows-2 m-2">
        <!-- You must be the change you wish to see in the world. - Mahatma Gandhi -->

        <!-- Row 1-->
        <!-- 1-->
        <div class="lg:col-span-2 col-span-5 place-self-center">
            <a href="/"><img class="min-h-20 min-w-80 " src="/images/FoozBotLogo.png"></a>
        </div>

        <!-- 2, 3, 4, 5 -->
        <div id="title" class="col-span-4 justify-center w-5/6 place-self-center lg:block hidden">
            <h1 class="lg:text-center p-4 overflow-hidden  border border-4 border-black rounded-2xl shadow-lg bg-FoozbotDBlue">Welcome To Foozbot</h1>
        </div>

        <!-- 6,7 -->
        @auth
            <div class="lg:place-self-center lg:col-span-2 col-span-1 max-h-1">
                <a href="/myAccount" class="text-center p-1 md:p-4 overflow-hidden  border border-4 border-black  rounded-2xl shadow-lg bg-FoozbotDBlue lg:inline hover:bg-FoozbotLBlue block">{{auth()->user()->username}}</a>
                <form method="post" action="/logout" class="inline">@csrf<input class=" text-center p-3 overflow-hidden border border-4 border-black rounded-2xl shadow-xl bg-FoozbotDBlue lg:block hover:cursor-pointer hover:bg-FoozbotLBlue lg:inline hidden" type="submit" value="logout"></form>
            </div>
        @endauth

        @guest
            <div class="lg:place-self-center lg:col-span-2 col-span-1 max-h-1">
                <a href="/login" class="text-center p-1 md:p-4 overflow-hidden border border-4 border-black rounded-2xl shadow-lg bg-FoozbotDBlue block lg:inline hover:bg-FoozbotLBlue">Log In</a>
                <a href="/register" class="text-center p-1 md:p-4 overflow-hidden  border border-4 border-black rounded-2xl shadow-lg bg-FoozbotDBlue block lg:inline hover:bg-FoozbotLBlue hidden">Register</a>
            </div>
        @endguest

        <!-- Row 2-->
        <!-- 1, 2 -->
        <div id="logo" class="lg:col-span-2 lg:block hidden ">
        </div>

        <!-- 3 -->
        <a href="/aboutUs" class="max-h-1">
            <h1 class="text-center p-1 md:p-4 overflow-hidden  border border-4 border-black  rounded-2xl shadow-lg bg-FoozbotDBlue hover:bg-FoozbotLBlue min-w-16">About</h1>
        </a>

        <!-- 4 -->
        <a href="/records" class="max-h-1">
            <h1 class="text-center p-1 md:p-4 overflow-hidden  border border-4 border-black rounded-2xl shadow-lg bg-FoozbotDBlue hover:bg-FoozbotLBlue min-w-16">Records</h1>
        </a>

        <!-- 5 -->
        <a href="/posts" class="max-h-1">
            <h1 class="text-center p-1 md:p-4 overflow-hidden  border border-4 border-black rounded-2xl shadow-lg bg-FoozbotDBlue hover:bg-FoozbotLBlue min-w-16">Posts</h1>
        </a>

        <!-- 6 -->
        <a href="/buy" class="max-h-1">
            <h1 class="text-center p-1 md:p-4 overflow-hidden  border border-4 border-black rounded-2xl shadow-lg bg-FoozbotDBlue hover:bg-FoozbotLBlue min-w-16">Buy</h1>
        </a>

        <!-- 7, 8 -->
        <div class="lg:col-span-2 lg:block hidden">
        </div>

    </div>
</div>
