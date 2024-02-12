
<x-layout>

    <!-- Main Buy Bubble-->
    <div class="flex justify-center mt-16 mb-6">
        <h1 class="py-4 px-12 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg">
            Upload a Foozbot Hightscore!
        </h1>
    </div>

    <div class = 'flex items-center justify-center' >
        <form method = 'POST' action ='/newScore' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg text-center">
            @csrf

            <label for='category' class = ''> Category: </label><br>
            <input type = 'text' value = "{{old('category')}}" name = 'category' id = 'category'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg'><br>
            @error('category')
            <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
            @enderror
            <br>

            <label for='score' class = ''> Score: </label><br>
            <input type = 'text' value = "{{old('score')}}" name = 'score' id = 'score'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg'><br>
            @error('score')
            <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
            @enderror
            <br>

            <label for='time' class = ''> Password: </label><br>
            <input type = 'text' name = 'time' id = 'time'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg'><br>
            @error('time')
            <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
            @enderror
            <br>

            <button name = 'submit' class = 'p-4 bg-FoozbotLBlue border-2 border-slate-500 rounded-xl shadow-lg'>Submit</button><br><br>
        </form>
    </div>

</x-layout>
