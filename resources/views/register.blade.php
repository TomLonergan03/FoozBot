
<x-layout>

    <!-- Main Buy Bubble-->
    <div class="flex justify-center mt-16 mb-6">
        <h1 class="py-4 px-12 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white rounded-xl border border-slate-500 shadow-lg text-2xl">
            Register For A Foozbot Account
        </h1>
    </div>

    <div class = 'flex items-center justify-center' >
        <form method = 'POST' action ='/register' onsubmit="submit.disabled = true; return true;" class="p-4 mb-16 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white rounded-xl border border-slate-500 shadow-lg text-center">
            @csrf

            <label for='first_name' class = ''> Username: </label><br>
            <input type = 'text' value = "{{old('first_name')}}" name = 'username' id = 'username'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg text-black'><br>
            @error('username')
                <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
            @enderror
            <br>

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

            <button name = 'submit' class = 'p-4 bg-FoozbotDBlue hover:bg-FoozbotLBlue shadow-lg border-2 border-slate-500 rounded-xl shadow-lg'>Submit</button><br><br>

            <a href="/login" class="text-slate-100 border border-slate-500 p-2 rounded-xl text-xs bg-FoozbotDBlue hover:bg-FoozbotLBlue shadow-lg"><i>Or sign-in here</i></a>

        </form>
    </div>

</x-layout>
