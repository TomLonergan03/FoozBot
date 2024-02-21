
<x-layout>

    <!-- Featured Posts, With comments on Click. This is like Forums. -->
    <section>


        <!-- the post -->
        <div class="flex justify-center items-center mt-14 table-auto px-12 ">
            <div class="basis-4/5 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover rounded-xl border-4 border-slate-500 shadow-lg shrink-0 text-white min-h-40">

                    <div class="pt-4 text-center text-4xl font-bold sticky inset-x-0 top-0 bg-gradient-to-bl from-stone-500 to-stone-800 pb-4 border-1 border-black">
                        <h1 class="">{{$guide->title}}</h1>
                        <p class="text-xs">By: {{$guide->username}}</p>
                        <p class="text-xs">Posted: {{$guide->created_at}}</p>
                        <p class="text-xs">Comments: {{count($comments)}}</p>
                    </div>

                    <p class="p-4 text-left lg:text-center overflow-scroll">
                        {{$guide->text}}
                    </p>
            </div>


        </div>

        @auth
        <!-- add a comment -->
        <div class = 'flex items-center justify-center p-2' >
            <form method = 'POST' action ='/posts/show/{{$guide->post_id}}/leaveComment' onsubmit="submit.disabled = true; return true;" class="p-2 mb-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white rounded-xl border border-slate-500 shadow-lg">
                @csrf
                <label for='text' class = 'text-left'> Leave a Comment </label><br>
                <textarea type = 'text' value = "{{old('text')}}" name = 'text' id = 'text'  required class = 'p-0 px-6 border-2 border-gray-500 rounded-xl shadow-lg text-black'></textarea><br>
                @error('text')
                <p class = 'text-red-500 text-xs mt-1'>{{$message}}</p>
                @enderror
                <br>

                <input type = "hidden" id="guide_id" name="guide_id" value="{{$guide->post_id}}">

                <button name = 'submit' class = 'p-1 bg-FoozbotDBlue hover:bg-FoozbotLBlue shadow-lg border-2 border-slate-500 rounded-xl shadow-lg'>Submit</button><br><br>
            </form>
        </div>
        @endauth

        @guest
        <!-- the post -->
        <div class="flex justify-center items-center mt-14 table-auto px-12 pb-4">
            <div class="p-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl">
                <h1 class="text-center font-semibold text-xl pb-1">Comments</h1>
                <h1 class="text-center font-semibold text-sm pb-1">Log-in to leave a comment</h1>
            </div>
        </div>
        @endguest





        <!-- all comments -->
        <div>
            <!-- Grid of Aux Bubbles -->
            <div class="flex justify-center items-center">
                <div class="grid grid-cols-1 gap-y-4 gap-x-20 mx-60 max-w-6xl shrink-0 size-11/12 min-w-64 md:text-base lg:text-xl mb-12">

                    @foreach($comments as $comment)
                    <!-- Layer One -->
                    <div class=" bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover rounded-xl border-4 border-slate-500 shadow-lg shrink-0 text-white overflow-y-scroll max-h-64 ">

                        <p class="p-4 text-left lg:text-center overflow-scroll">
                            {{$comment->text}}
                        </p>

                        <div class="p-2 text-left bg-gradient-to-bl from-stone-500 to-stone-800 border-1 border-black">
                            <p class="text-xs">By {{$comment->username}} at {{date('H:i d-m-y',strtotime($comment->created_at))}}</p>
                        </div>

                    </div>
                    @endforeach
                </div>
            </div>
        </div>
    </section>

</x-layout>
