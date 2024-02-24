<?php

namespace App\Http\Controllers;

use App\Models\Comment;
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
                ->simplePaginate(8);

        else:
            $guides = DB::table('guides')
                ->join('users', 'users.id', '=', 'user_id')
                ->where('featured', 0)
                ->select('*', 'guides.id as post_id')
                ->orderBy('guides.updated_at', 'desc')
                ->groupBy("guides.id")
                ->simplePaginate(8);

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
            'title' => ['required', 'max:20', 'min:3'],
            'text' => ['required', 'max:500', 'min:10'],
        ]);


        //
        $request->user()->guides()->create($attributes1);



        return redirect('/posts/newest')->with('passed', 'Post Created!');

    }

    /**
     * Store a newly created resource in storage.
     */
    public function storeComment(Request $request)
    {
        $validated = request()->validate([
            'text' => ['required', 'max:500', 'string'],
            'guide_id' => ['required', 'numeric']
        ]);

        $request->user()->comments()->create(['text'=>$validated['text'], 'guide_id'=>$validated['guide_id']]);

        return redirect('/posts/show/' . $validated['guide_id'])->with('passed', 'Comment Created!');

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
            ->where('comments.guide_id', $guideid)
            ->select('*', 'comments.id as comment_id')
            ->orderBy("comments.created_at", "desc")
            ->get();

        //return the view with the one guide, and its comments
        return view('individualGuide', ['guide' => $guide, 'comments' => $comments]);

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
