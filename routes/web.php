<?php

use App\Http\Controllers\GuideController;
use App\Http\Controllers\LeaderboardController;
use App\Http\Controllers\RegisterController;
use App\Http\Controllers\SessionsController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

//register
Route::get('/register', [RegisterController::class, 'create'])->middleware('guest');
Route::post('/register', [RegisterController::class, 'store'])->middleware('guest');

//login
Route::get('/login', [SessionsController::class, 'create'])->middleware('guest')->name('login');
Route::post('/sessions', [SessionsController::class, 'store'])->middleware('guest');
Route::post('/logout', [SessionsController::class, 'destroy'])->middleware('auth');

//Account Page
Route::get('/myAccount', function () {
    return view('myAccount');
})->middleware('auth');

//AboutUs
Route::get('/aboutUs', function () {
    return view('aboutUs');
});

//Guides
Route::get('/posts', [GuideController::class, 'index']);
Route::get('/posts/{filter}', [GuideController::class, 'indexBy'])->where(['filter' => '[a-zA-Z0-9]+']);
Route::post('/posts/show/add', [GuideController::class, 'store'])->middleware('auth');
Route::get('/posts/show/{guideName}', [GuideController::class, 'show'])->where(['guideName' => '[a-zA-Z0-9]+']);
Route::post('/posts/show/{guideName}/leaveComment', [GuideController::class, 'store'])->where(['guideName' => '[a-zA-Z0-9]+'])->middleware('auth');


//Buy Foozbot
Route::get('/buy', function () {
    return view('buyPage');
});

//Records
Route::get('/records', [LeaderboardController::class, 'displayInitial']);
Route::get('/records/{category}', [LeaderboardController::class, 'displayAll'])->where(['category' => '[a-zA-Z0-9]+']);




