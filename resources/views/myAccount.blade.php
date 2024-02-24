
<x-layout>

    <!-- Main Buy Bubble-->
    <div class="flex justify-center mt-16 mb-2">
        <div class="py-4 px-12 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl">
            <h1 class="text-center">
                Your Foozbot Account
            </h1>
        </div>
    </div>


    <div class="flex justify-center items-center mb-4">
            <div class="p-1 border border-4 border-black m-1 rounded-2xl shadow-lg bg-FoozbotDBlue hover:bg-FoozbotLBlue">
                <form method="post" action="/logout" class="inline">@csrf<input class="text-center font-semibold text-xl text-gray-300 text-xs" type="submit" value="Log Out"></form>
            </div>
            <div class="p-1 border border-4 border-black  rounded-2xl shadow-lg bg-FoozbotDBlue hover:bg-FoozbotLBlue">
                <button href="/"><h1 class="text-center font-semibold text-xl text-gray-300 text-xs "><i>Reset Password</i></h1></button>
            </div>

    </div>


    <div class = 'flex items-center justify-center m-4' >
        <div method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl text-center">
            <h1>Username: {{auth()->user()->username}}</h1>
        </div>
    </div>

    <div class = 'flex items-center justify-center m-4' >
        <div method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl text-center">
            <h1>Email: {{auth()->user()->email}}</h1>
        </div>
    </div>

<!--    <div class = 'flex items-center justify-center m-4' >-->
<!--        <div method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl text-center">-->
<!--            <h1>Foozbot Purchased: {{auth()->user()->userType}}</h1>-->
<!--        </div>-->
<!--    </div>-->


</x-layout>
