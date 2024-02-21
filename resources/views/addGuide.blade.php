
<x-layout>

    <!-- Featured Posts, With comments on Click. This is like Forums. -->
    <section>

        <!-- add a comment -->
        <div class = 'flex items-center justify-center p-2' >
            <form method = 'POST' action ='/posts/show/add' onsubmit="submit.disabled = true; return true;" class="p-2 mb-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white rounded-xl border border-slate-500 shadow-lg">
                @csrf
                <label for='title' class = 'text-left'> Post Title </label><br>
                <input type = 'text' value = "{{old('title')}}" name = 'title' id = 'title'  required class = 'p-0 px-6 border-2 border-gray-500 rounded-xl shadow-lg text-black'></input><br>
                @error('text')
                <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
                @enderror
                <br>

                <label for='text' class = 'text-left'> What do you want to say? </label><br>
                <textarea type = 'text' value = "{{old('text')}}" name = 'text' id = 'text'  required class = 'p-0 px-6 border-2 border-gray-500 rounded-xl shadow-lg text-black'></textarea><br>
                @error('text')
                <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
                @enderror
                <br>

                <button name = 'submit' class = 'p-1 bg-FoozbotDBlue hover:bg-FoozbotLBlue shadow-lg border-2 border-slate-500 rounded-xl shadow-lg'>Submit</button><br><br>
            </form>
        </div>
    </section>

</x-layout>
