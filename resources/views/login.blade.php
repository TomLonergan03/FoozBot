
<x-layout>

    <!-- Main Buy Bubble-->
    <div class="flex justify-center mt-16 mb-6">
        <div class="py-4 px-12 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl text-2xl">
            <h1 class="text-center">
                Log-In to Foozbot
            </h1>
        </div>
    </div>

    <div class = 'flex items-center justify-center' >
        <form method = 'POST' action ='/sessions' onsubmit="submit.disabled = true; return true;" class="mb-16 p-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl text-center">
            @csrf

            <label for='email' class = ''> Email: </label><br>
            <input type = 'text' value = "{{old('last_name')}}" name = 'email' id = 'email'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg text-black'><br>
            @error('email')
            <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
            @enderror
            <br>

            <label for='password' class = ''> Password: </label><br>
            <input type = 'password' name = 'password' id = 'password'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg text-black'><br>
            @error('password')
            <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
            @enderror
            <br>

            <button name = 'submit' class = 'p-4 border-2 border-gray-500 border-slate-500 rounded-2xl shadow-xl bg-FoozbotDBlue hover:cursor-pointer hover:bg-FoozbotLBlue'>Submit</button><br><br>

            <a href="/register" class="text-slate-100 border border-slate-500 p-2 rounded-xl text-xs bg-FoozbotDBlue hover:bg-FoozbotLBlue shadow-lg"><i>Or register here</i></a>

        </form>
    </div>

</x-layout>
