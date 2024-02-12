<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class RegisterController extends Controller
{
    //register/create a new user
    public function create(){
        return view('register');
    }

    //store the details of a new user
    public function store(){

        $attributes1 = request()->validate([
            'username' => ['required', 'max:20', 'min:2', 'alpha_dash'],
            'email' => ['required', 'max:30', 'min:2', 'unique:users', 'email'],
            'password' => ['required', 'min:8'],
        ]);

        //Verify email here if we have time

        //mass assignment might/will stop the user_type_id
        $user = User::create([
            'username' => $attributes1['username'],
            'email' => $attributes1['email'],
            'password' => bcrypt($attributes1['password']),
            'type' => 'user'
        ]);


        auth()->login($user);
        return redirect('/')->with('passed', 'Account Created Successfully, and Logged In');

    }

}
