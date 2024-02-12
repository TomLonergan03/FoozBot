<?php

namespace App\Http\Controllers;

use App\Models\Guide;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class GuideController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index($filter):View{

        #Featured Guides - I.E made by developers

        $featured = DB::table('guides')->where('featured', 1)->orderBy('posted', 'desc')->get();

        #All Guides
        $guides = DB::table('guides')->where('featured', 0)->orderBy('posted', 'desc')->get();

        #Return
        return view('guidesLanding', ['featured' => $featured, 'guides' => $guides]);

    }



    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $attributes1 = request()->validate([
            'title' => ['required', 'max:20', 'min:3', 'alpha_dash', 'unique:guides'],
            'text' => ['required', 'max:500', 'min:10'],
        ]);


        //mass assignment might/will stop the user_type_id
        $guide = Guide::create([
            'title' => $attributes1['title'],
            'text' => $attributes1['text'],
        ]);


        return redirect('/guides/none')->with('passed', 'Post Created!');

    }

    /**
     * Display the specified resource.
     */
    public function show(Guide $guideName): View
    {
        //get the guide
        $guide = DB::table('Guides')->join('users', 'users.id', '=', 'user_id')->where('title', $guideName)->paginate(20)->get();

        $id = $guide[0]->id;

        //get the comment(s)
        $comments = DB::table('Comments')->join('guides', 'users.id', '=', 'user_id')->where('guide_id', $id)->get();

        //return the view with the one guide, and its comments
        return view('individualGuide', ['featured' => $guide, 'comments' => $comments]);

    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Guide $guide)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, Guide $guide)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Guide $guide)
    {
        //
    }
}
