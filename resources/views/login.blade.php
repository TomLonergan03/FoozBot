
<x-layout>

    <!-- Main Buy Bubble-->
    <div class="flex justify-center mt-16 mb-6">
        <div class="py-4 px-12 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg">
            <h1 class="text-center">
                Log-In to Foozbot
            </h1>
        </div>
    </div>

    <div class = 'flex items-center justify-center' >
        <form method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg text-center">
            @csrf

            <label for='email' class = ''> Email: </label><br>
            <input type = 'text' value = "{{old('last_name')}}" name = 'email' id = 'email'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg'><br>
            @error('email')
            <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
            @enderror
            <br>

            <label for='password' class = ''> Password: </label><br>
            <input type = 'password' name = 'password' id = 'password'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg'><br>
            @error('password')
            <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
            @enderror
            <br>

            <button name = 'submit' class = 'p-4 bg-FoozbotLBlue border-2 border-slate-500 rounded-xl shadow-lg'>Submit</button><br><br>

            <a href="/register" class="text-slate-700 border border-slate-500 p-2 rounded-xl text-xs bg-FoozbotLBlue shadow-lg"><i>Or register here</i></a>

        </form>
    </div>

</x-layout>
