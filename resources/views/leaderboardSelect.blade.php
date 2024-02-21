
<x-layout>


    <!-- "Select a Category" inline with "Upload a Score" -->
    <div class="flex justify-center items-center mt-14 table-auto py-4 px-12 ">

        <div class="border-4 border-slate-500 shadow-lg p-2 rounded-xl bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover text-white">

            <h1 class="text-center font-semibold text-xl pb-1"><u>Select a Category</u></h1>
            <h1 class="text-center sm:text-left" >Current Category : {{$currentcategory}}</h1>

            <div class="flex items-center justify-center">
                <div class=" text-center py-2 overflow-y-scroll max-h-20 w-40 z-4">
                    @foreach ($categories as $c)
                        <h1 class="p-1"> </h1>
                        <a href="/records/{{$c->category}}" class="text-center border border-grey-700 rounded-xl p-1 shadow-lg bg-FoozbotDBlue inline hover:bg-FoozbotLBlue">{{$c->category}}</a>
                        <h1 class="p-1"> </h1>
                    @endforeach
                </div>

            </div>
        </div>

    </div>

    <!-- Table of Scores/ the Leaderboard -->

    <div class="flex justify-center items-center mb-14 table-auto py-4 px-12">

        <table class="border-separate bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover rounded-xl border-4 border-slate-500 shadow-lg p-2 text-white">
            <tr>
                <th class="border-2 border-gray-200 p-2 rounded-lg">Holder</th>
                <td class="px-2"></td>
                <th class="border-2 border-gray-200 p-2 rounded-lg">Score</th>
                <td class="px-2"></td>
                <th class="border-2 border-gray-200 p-2 rounded-lg">Time(Seconds)</th>
                <td class="px-2 hidden sm:block"></td>
                <th class="border-2 border-gray-200 p-2 rounded-lg hidden sm:block">Category</th>
            </tr>

            <tr>
                <td class="py-1"></td>
            </tr>

            @foreach ($scores as $score)

                @if($loop->even)
                    <tr>
                        <td class="border-x-2 border-gray-200 p-1">{{$score->username}}</td>
                        <td class="px-2"></td>
                        <td class="border-x-2 border-gray-200 p-1">{{$score->score}}</td>
                        <td class="px-2"></td>
                        <td class="border-x-2 border-gray-200 p-1">{{$score->time}}</td>
                        <td class="px-2hidden sm:block"></td>
                        <td class="border-x-2 border-gray-200 p-1 hidden sm:block">{{$score->category}}</td>
                    </tr>
                @else
                    <tr>
                        <td class="border-x-2 border-gray-200 p-1 text-gray-300">{{$score->username}}</td>
                        <td class="px-2"></td>
                        <td class="border-x-2 border-gray-200 p-1 text-gray-300">{{$score->score}}</td>
                        <td class="px-2"></td>
                        <td class="border-x-2 border-gray-200 p-1 text-gray-300">{{$score->time}}</td>
                        <td class="px-2 hidden sm:block"></td>
                        <td class="border-x-2 border-gray-200 p-1 text-gray-300 hidden sm:block">{{$score->category}}</td>
                    </tr>
                @endif

            @endforeach
        </table>


    </div>

</x-layout>
