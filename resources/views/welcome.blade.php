
<x-layout>

    <!-- Info Bubbles-->
    <div class="mx-8 p-4">

        <!-- Main Buy Bubble-->
        <div class="flex justify-center items-center my-14">
            <div class="py-4 px-12 bg-foozbotmain bg-cover rounded-xl border-4 border-slate-500 shadow-lg w-3/5 h-64 flex items-center justify-center">
                <h1 class=" z-2 justify-center py-4 px-12 rounded-xl border border-slate-500 shadow-lg bg-gradient-to-bl from-stone-300 to-stone-400 font-bold font-sans text-red-800 text-xl md:text-4xl opacity-90 text-center">
                    Affordable Robot-Powered Foozball!
                </h1>
            </div>
        </div>

        <!-- Grid of Aux Bubbles -->
        <div class="flex justify-center items-center">
            <div class="grid lg:grid-cols-2 lg:grid-rows-2 grid-cols-1 grid-rows-4 gap-y-16 gap-x-16 mx-60 max-w-6xl lg:shrink-0 lg:size-11/12 min-w-64 md:text-base lg:text-xl">

                <!-- Layer One -->
                <div class="basis-1/2 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover rounded-xl border-4 border-slate-500 shadow-lg shrink-0 text-white">
                    <h1 class="pt-4 text-center text-4xl font-bold">What Is Foozbot?</h1>
                    <p class="p-4 text-left lg:text-center overflow-scroll">
                        <b>Robot-Powered Foozball</b> – What could be more cool? Gone are the days of wishing you had someone to play foozball with, as Foozbot will be your new friend, rival, and coach! <br><br> Featuring <i><b>Detachable cameras and motors</b></i>, Foozbot can be quickly configured for all manner of difficulties and game modes from our mobile app!                      </p>
                </div>

                <div class=" bg-red-500 rounded-xl border-4 border-slate-500 shadow-lg flex justify-center align-middle overflow-hidden w-full">
                    <img class="rounded-xl shrink-0 min-w-full min-h-full w-full" src="images/demo-one-model.jpg">
                </div>


                <!-- Layer Two -->
                <div class="bg-red-500 rounded-xl border-4 border-slate-500 shadow-lg flex justify-center align-middle overflow-hidden lg:block hidden bg-foozbotmain bg-[length:550px_500px]">
<!--                    <img class="rounded-xl shrink-0 min-w-full min-h-full size-fit" src="images/motors.jpg">-->
                </div>

                <div class="basis-1/2 bg-gradient-to-bl from-stone-500 to-stone-800 bg-cover rounded-xl border-4 border-slate-500 shadow-lg shrink-0 text-white">
                    <h1 class="pt-4 text-center text-4xl font-bold">Still Not Convinced?</h1>
                    <p class="p-4 text-left lg:text-center overflow-scroll"> Would any of these features change your mind? </p>
                    <ul class="pl-8 list-disc font-semibold text-yellow-300">
                        <li>Single-Player Foozball For all skill levels</li><br>
                        <li>Detachable Components for playing normally</li><br>
                        <li>Mobile App for Configuration</li><br>
                        <li>Global, Competitive Leaderboards</li><br>
                        <li>And Much More...</li><br>
                    </ul>
                </div>

                <div class=" bg-red-500 rounded-xl border-4 border-slate-500 shadow-lg flex justify-center align-middle overflow-hidden lg:hidden block bg-foozbotmain bg-[length:550px_500px]">
<!--                    <img class="rounded-xl shrink-0 min-w-full min-h-full" src="images/motors.jpg">-->
                </div>

            </div>
        </div>

    </div>


</x-layout>
