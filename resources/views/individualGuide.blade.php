
<x-layout>


    <!-- "Select a Category" inline with "Upload a Score" -->
    <div class="flex justify-center items-center mt-14 table-auto py-4 px-12 ">

        <div class="border border-slate-600 p-2 rounded-xl bg-gradient-to-bl from-stone-300 to-stone-400 bg-cover">

            <h1 class="text-center font-semibold text-xl pb-1">Select a Category</h1>
            <h1>Current Category : </h1>

            <div class=" text-center py-2 overflow-y-scroll max-h-20 w-40">
                @foreach ($comments as $comment)
                <p href="" class="text-center border border-grey-700 rounded-xl p-1 shadow-lg bg-FoozbotLBlue inline hover:bg-FoozbotDBlue">amongys</p>
                <h1 class="p-1"> </h1>
                @endforeach
            </div>

        </div>

    </div>

    <!-- Table of Scores/ the Leaderboard -->

    </div>

</x-layout>
