
<x-layout>


    <!-- "Select a Category" inline with "Upload a Score" -->
    <div class="flex justify-center items-center mt-14 table-auto py-4 px-12 ">

        <div class="border border-slate-600 p-2 rounded-xl bg-gradient-to-bl from-stone-300 to-stone-400 bg-cover">

            <h1 class="text-center font-semibold text-xl pb-1">Select a Category</h1>
            <h1>Current Category : {{$currentcategory}}</h1>

            <div class=" text-center py-2 overflow-y-scroll max-h-20 w-40">
                @foreach ($categories as $c)
                    <a href="/records/{{$c->category}}" class="text-center border border-grey-700 rounded-xl p-1 shadow-lg bg-FoozbotLBlue inline hover:bg-FoozbotDBlue">{{$c->category}}</a>
                <h1 class="p-1"> </h1>
                @endforeach
            </div>

        </div>

    </div>

    <!-- Table of Scores/ the Leaderboard -->

    <div class="flex justify-center items-center mb-14 table-auto py-4 px-12">

        <table class="border-separate bg-gradient-to-bl from-stone-300 to-stone-400 bg-cover rounded-xl border-4 border-slate-500 shadow-lg p-2">
            <tr>
                <th class="border border-slate-600 p-2 rounded-xl">Holder</th>
                <td class="px-2"></td>
                <th class="border border-slate-600 p-2 rounded-xl">Score</th>
                <td class="px-2"></td>
                <th class="border border-slate-600 p-2 rounded-xl">Time(Seconds)</th>
                <td class="px-2"></td>
                <th class="border border-slate-600 p-2 rounded-xl">Category</th>
            </tr>

            <tr>
                <td class="py-1"></td>
            </tr>

            @foreach ($scores as $score)
            <tr>
                <td class="border border-slate-600 p-2">{{$score->username}}</td>
                <td class="px-2"></td>
                <td class="border border-slate-600 p-2">{{$score->score}}</td>
                <td class="px-2"></td>
                <td class="border border-slate-600 p-2">{{$score->time}}</td>
                <td class="px-2"></td>
                <td class="border border-slate-600 p-2">{{$score->category}}</td>
            </tr>
            @endforeach
        </table>


    </div>

</x-layout>
