<?php

namespace Database\Seeders;

// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use App\Models\Guide;
use App\Models\Leaderboard;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {

        //default users
        \App\Models\User::factory(20)->has(Leaderboard::factory(1)->sequence(['category' => 'HighestScore'],['category' => 'LowestTime'],['category' => 'Doubles']))->create();

        //2 "admins" with guides
        \App\Models\User::factory(1)->has(Guide::factory(1))->create();

        // \App\Models\User::factory()->create([
        //     'name' => 'Test User',
        //     'email' => 'test@example.com',
        // ]);
    }
}
