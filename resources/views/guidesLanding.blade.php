
<x-layout>


    <!-- "Select a Category" inline with "Upload a Score" -->
    <div class="flex justify-center items-center mt-14 table-auto py-4 px-12 ">

        <div class="border border-slate-600 p-2 rounded-xl bg-gradient-to-bl from-stone-300 to-stone-400 bg-cover">

            <h1 class="text-center font-semibold text-xl pb-1">Featured</h1>

        </div>

    </div>

    <!-- add a guide -->
    <div class="flex justify-center items-center mt-14 table-auto py-4 px-12 ">

        <div class="border border-slate-600 p-2 rounded-xl bg-gradient-to-bl from-stone-300 to-stone-400 bg-cover">

            <h1 class="text-center font-semibold text-xl pb-1">Create a Post</h1>

            <div class = 'flex items-center justify-center' >
                <form method = 'POST' action ='/guides/add' onsubmit="submit.disabled = true; return true;" class="p-4 bg-gradient-to-bl from-stone-300 to-stone-400 rounded-xl border border-slate-500 shadow-lg text-center">
                    @csrf

                    <label for='title' class = ''> Title: </label><br>
                    <input type = 'text' value = "{{old('title')}}" name = 'title' id = 'title'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg'><br>
                    @error('title')
                    <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
                    @enderror
                    <br>

                    <label for='text' class = ''> Text: </label><br>
                    <textarea  value = "{{old('text')}}" name = 'text' id = 'text'  required class = 'p-2 px-6 border-2 border-gray-500 rounded-xl shadow-lg'></textarea><br>
                    @error('text')
                        <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
                    @enderror
                    <br>

                    <button name = 'submit' class = 'p-4 bg-FoozbotLBlue border-2 border-slate-500 rounded-xl shadow-lg'>Submit</button><br><br>
                </form>
            </div>

        </div>

    </div>

    <!-- Grid of Aux Bubbles -->
    <div class="flex justify-center items-center">
        <div class="grid grid-cols-2 gap-y-16 gap-x-16 mx-60 max-w-6xl shrink-0">

            @foreach ($guides as $guide)
            <div class=" bg-red-500 rounded-xl border-4 border-slate-500 shadow-lg justify-center align-middle h-20">
                <h1 class="text-center font-semibold text-xl">{{$guide->title}}</h1>
                <p class="overflow-hidden max-h-20">{{$guide->text}}</p>

            </div>
            @endforeach

        </div>
    </div>




</x-layout>
