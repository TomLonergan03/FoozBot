
<x-layout>

    <!-- Main Buy Bubble-->
    <div class="flex justify-center mt-16 mb-6">
        <div class="py-4 px-12 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg">
            <h1 class="text-center">
                Your Foozbot Account
            </h1>
        </div>
    </div>

    <div class = 'flex items-center justify-center m-4' >
        <div method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg text-center">
            <h1>Username: {{auth()->user()->username}}</h1>
        </div>
    </div>

    <div class = 'flex items-center justify-center m-4' >
        <div method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg text-center">
            <h1>Email: {{auth()->user()->email}}</h1>
        </div>
    </div>

    <div class = 'flex items-center justify-center m-4' >
        <div method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg text-center">
            <h1>Foozbot Purchased: {{auth()->user()->userType}}</h1>
        </div>
    </div>

    <div class = 'flex items-center justify-center m-4' >
        <button>
            <div method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-300 to-stone-400 border border-slate-500 shadow-lg text-center">
                Reset Password
            </div>
        </button>
    </div>


</x-layout>
