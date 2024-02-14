
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
        <div class="flex justify-center items-center mt-14 table-auto py-4 px-12 ">
            <div class="p-4 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white border-4 border-slate-500 shadow-lg rounded-xl">
                <h1 class="text-center font-semibold text-xl pb-1">Community Posts:</h1>
            </div>
        </div>

        <div>
            @foreach($posts as $post)

            @endforeach
        </div>

    </section>


</x-layout>
