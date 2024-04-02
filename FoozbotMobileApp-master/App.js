import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ImageBackground, Image, TextInput, Button } from 'react-native';
import React, {useState} from 'react';
import {NavigationContainer} from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack';


//Screens
import Connect from './screens/Connect'
import Setup from './screens/Setup'
import GameInProgress from './screens/GameInProgress'
import GameOver from './screens/GameOver'

import Leaderboard from './screens/Leaderboard'
import UserGuide from './screens/UserGuide';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{
        contentStyle: {
          backgroundColor: "black",
          
        },
        headerStyle: {
          backgroundColor: 'black',
          headerBackVisible: false,
        }
      }}>

        <Stack.Screen name="connect" component={Connect} options={{title:" "}}/>
        <Stack.Screen name="setup" component={Setup} options={{title:" ", headerTintColor: 'white'}}/>
        <Stack.Screen name="gameInProgress" component={GameInProgress} options={{title:" ", headerTintColor: 'white'}}/>
        <Stack.Screen name="gameOver" component={GameOver} options={{title:" ", headerTintColor: 'white'}}/>

        <Stack.Screen name="leaderboard" component={Leaderboard} options={{title:" Leaderboard", headerTintColor: 'white'}}/>
        <Stack.Screen name="userGuide" component={UserGuide} options={{title:"User Guide", headerTintColor: 'white'}}/>

      </Stack.Navigator>
    </NavigationContainer>
  );
}





const styles = StyleSheet.create({
  container: {
  },
  ImageBackground:{
    width: '100%',
    height: '100%',
  },
  header:{
    flex: 1,
    padding: 40,
    maxHeight: "20%",
    alignItems: 'center',
    borderStyle: 'solid',
    borderColor: 'red',
    borderWidth: 5,
  },
  Logo:{
    height: '130%',
    width:'120%',
  },
  mainContainer:{
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    borderStyle: 'solid',
    borderColor: 'red',
    borderWidth: 5,
  },
  bodyText:{
  },
  footer:{
    height:"15%",
    width:"100%",
    borderStyle: 'solid',
    borderColor: 'blue',
    borderWidth: 5,
  },

  button: {
    padding: 4,
    borderStyle: 'solid',
    borderColor: 'red',
    borderWidth: 5,
  },


});
