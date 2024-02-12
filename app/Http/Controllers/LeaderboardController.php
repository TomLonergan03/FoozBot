<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class LeaderboardController extends Controller
{

    public function displayInitial(): View
    {
        return $this->displayAll("HighestScore");
    }

    //
    public function store(Request $request): RedirectResponse
    {
        //Validate the new leaderboard item
        $validated = $request->validate([
            'message' => 'required|string|max:255|alpha_dash',
        ]);

        $request->user()->leaderboard()->create($validated);

        return redirect(route('chirps.index'));
    }

    public function displayAll($category):View{

        //Get all categories for the dropdown
        $categories = DB::table('leaderboards')->select('category')->orderBy('category', 'desc')->groupBy('category')->get();


        if(!empty($category)){
            $scores = DB::table('leaderboards')->join('users', 'users.id', '=', 'user_id')->where('category', $category)->orderBy('score', 'desc')->get();
            return view('leaderboardSelect', ['scores' => $scores, 'categories' => $categories, 'currentcategory' => $category]);
        }

        $scores = DB::table('leaderboards')->join('users', 'user_id', '=', 'user_id')->where('category', $category)->orderBy('score', 'desc')->get();
        return view('leaderboardSelect', ['scores' => $scores, 'categories' => $categories, 'currentcategory' => $category]);

    }

}
