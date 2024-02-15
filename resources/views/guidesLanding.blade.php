
<x-layout>


    <!-- Dev Guides, such as User Guide, and Safety Guide -->
    <section>
        <div class="flex justify-center items-center mt-14 table-auto py-4 px-12 ">
            <div class="p-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl">
                <h1 class="text-center font-semibold text-xl pb-1">Developer Guides:</h1>
            </div>
        </div>

        <div>
            @foreach($featured as $feat)

            @endforeach
        </div>

    </section>

    <!-- Featured Posts, With comments on Click. This is like Forums. -->
    <section>
        <div class="flex justify-center items-center mt-14 table-auto px-12 ">
            <div class="p-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl">
                <h1 class="text-center font-semibold text-xl pb-1">Community Posts:</h1>
            </div>
        </div>
        <div class="flex justify-center items-center mb-4">
            <a href="/posts/newest">
            <div class="p-2 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl">
                <h1 class="text-center font-semibold text-xl pb-1 text-gray-300 text-xs"><i>See All</i></h1>
            </div>
            </a>
        </div>

        <div>
            <!-- Grid of Aux Bubbles -->
            <div class="flex justify-center items-center">
                <div class="grid lg:grid-cols-2 lg:grid-rows-2 grid-cols-1 grid-rows-4 gap-y-16 gap-x-16 mx-60 max-w-6xl lg:shrink-0 lg:size-11/12 min-w-64 md:text-base lg:text-xl">

                    @foreach($posts as $post)
                    <!-- Layer One -->
                    <div class="basis-1/2 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover rounded-xl border-4 border-slate-500 shadow-lg shrink-0 text-white overflow-y-scroll max-h-64">

                        <a href="/posts/show/{{$post->post_id}}">
                        <div class="pt-4 text-center text-4xl font-bold sticky inset-x-0 top-0 bg-gradient-to-bl from-stone-500 to-stone-800 pb-4 border-1 border-black">
                            <h1 class="">{{$post->title}}</h1>
                            <p class="text-xs">By: {{$post->username}}</p>
                            <p class="text-xs">Posted: {{$post->created_at}}</p>
                        </div>

                        <p class="p-4 text-left lg:text-center overflow-scroll">
                            {{$post->text}}
                        </p>
                        </a>
                    </div>
                    @endforeach
                </div>
            </div>
        </div>

    </section>

</x-layout>
