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
    public function index():View{

        #Featured Guides - I.E made by developers
        $featured = DB::table('guides')->where('featured', 1)->orderBy('posted', 'desc')->get();

        #All Guides
        $guides = DB::table('guides')
            ->join('users', 'users.id', '=', 'user_id')
            ->where('featured', 0)
            ->select('*', 'guides.id as post_id')
            ->orderBy('posted', 'desc')
            ->groupBy("guides.id")
            ->limit(4)
            ->get();

        #Return
        return view('guidesLanding', ['featured' => $featured, 'posts' => $guides, 'keys' => $guides->keys()]);
    }



    /**
     * Display a listing of the resource.
     */
    public function indexBy($filter):View{


        if ($filter == "oldest"):
            #All Guides
            $guides = DB::table('guides')
                ->join('users', 'users.id', '=', 'user_id')
                ->where('featured', 0)
                ->select('*', 'guides.id as post_id')
                ->orderBy('guides.updated_at', 'asc')
                ->groupBy("guides.id")
                ->get();

        else:
            $guides = DB::table('guides')
                ->join('users', 'users.id', '=', 'user_id')
                ->where('featured', 0)
                ->select('*', 'guides.id as post_id')
                ->orderBy('guides.updated_at', 'desc')
                ->groupBy("guides.id")
                ->get();

        endif;

        #Return
        return view('allGuides', ['orderBy' => $filter, 'posts' => $guides]);
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
    public function show($guideid): View
    {

        $guide = DB::table('guides')
            ->join('users', 'users.id', '=', 'user_id')
            ->where('guides.id', $guideid)
            ->select('*', 'guides.id as post_id')
            ->groupBy("guides.id")
            ->first();

        $comments = DB::table('comments')
            ->join('users', 'users.id', '=', 'user_id')
            ->where('comments.id', $guideid)
            ->select('*', 'comments.id as comment_id')
            ->orderBy("comments.created_at", "desc")
            ->groupBy("comments.id")
            ->get();

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
