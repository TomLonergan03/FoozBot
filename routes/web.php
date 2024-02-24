<?php

use App\Http\Controllers\GuideController;
use App\Http\Controllers\LeaderboardController;
use App\Http\Controllers\RegisterController;
use App\Http\Controllers\SessionsController;
use Illuminate\Support\Facades\Route;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;

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
Route::get('/posts/show/add', function (){return view('addGuide');})->middleware('auth');
Route::post('/posts/show/add', [GuideController::class, 'store'])->middleware('auth');
Route::get('/posts/show/{guideid}', [GuideController::class, 'show'])->where(['guideid' => '[a-zA-Z0-9]+']);
Route::post('/posts/show/{guideid}/leaveComment', [GuideController::class, 'storeComment'])->where(['guideid' => '[0-9]'])->middleware('auth');


//Buy Foozbot
Route::get('/buy', function () {
    return view('buyPage');
});

//Records
Route::get('/records', [LeaderboardController::class, 'displayInitial']);
Route::get('/records/{category}', [LeaderboardController::class, 'displayAll'])->where(['category' => '[a-zA-Z0-9]+']);

//Privacy and TC and User Guides
Route::get('/privacyPolicy', function () {
    return view('privacyPolicy');
});
Route::get('/termsConditions', function () {
    return view('termsAndConditions');
});
Route::get('/userInfo', function () {
    return view('userInfo');
});



//Password Reset
Route::get('/emailNewPassword', function () {
    return view('requestNewPassword');
})->middleware('guest')->name('password.request');

Route::post('/emailNewPassword', function (Request $request) {
    $request->validate(['email' => 'required|email']);

    $status = Password::sendResetLink(
        $request->only('email')
    );

    return $status === Password::RESET_LINK_SENT
        ? back()->with(['status' => __($status)])
        : back()->withErrors(['email' => __($status)]);
})->middleware('guest')->name('password.email');



Route::get('/newPassword/{token}', function (string $token) {
    return view('passwordReset', ['token' => $token]);
})->middleware('guest')->name('password.reset');


Route::post('/newPassword', function (Request $request) {
    $request->validate([
        'token' => 'required',
        'email' => 'required|email',
        'password' => 'required|min:8|confirmed',
    ]);

    $status = Password::reset(
        $request->only('email', 'password', 'password_confirmation', 'token'),
        function (User $user, string $password) {
            $user->forceFill([
                'password' => Hash::make($password)
            ])->setRememberToken(Str::random(60));

            $user->save();

            event(new PasswordReset($user));
        }
    );

    return $status === Password::PASSWORD_RESET
        ? redirect()->route('login')->with('status', __($status))
        : back()->withErrors(['email' => [__($status)]]);
})->middleware('guest')->name('password.update');







