import { StyleSheet, Text, View, ImageBackground, Image, TextInput, Button, TouchableOpacity} from 'react-native';
import React from 'react'
import { StatusBar } from 'expo-status-bar';

export default function Connect({navigation}) {
  return (
    <View style={styles.container}>
      <View style={styles.mainContainer}>

        {/* Logo Title */}
        <View style={styles.logoSection}>
            <Image style={styles.logo} source={require('../assets/images/FoozBotLogoTwo.png')}/>
        </View>

        {/* Text Component */}
        <View style={styles.TextSection}>

            <Text style={styles.TextHeader}>Connect To A Pitch</Text>
            <Text style={styles.TextParagraph}>Simply press "Connect" to connect to your Foozbot! Then, you can set your gamemode and difficulty to begin the game!</Text>

        </View>


        {/* Connect and User Guide Buttons */}
        <View style={styles.buttonWrapper}>

            <ConnectButton navigation={navigation} title="Connect" press="connectToFoozbot" ip="http://0.0.0.0:8000"/>
            <HowToPlayButton navigation={navigation} title="How To Play" dest="userGuide" img="HowToPlay.png"/>
            <LeaderboardButton navigation={navigation} title="Leaderboard" dest="leaderboard" img="Leaderboard.png" />

        </View>



      </View>
      <StatusBar />
    </View>
  )
}

const ConnectButton = ({navigation, press, title, ip}) => (
    <TouchableOpacity style={styles.button}           
        onPress={() => {

            const response = fetch(ip, { method: 'GET'})
            .then( (response) => response.json())
            .then(json => {
              
                if (!json.ongoing && !json.otherUserConnecting){
                    alert("Can Connect. Starting Game.")
                    navigation.navigate('setup', {sessionID: json.sessionID, ip:ip})
                }

                else if (!json.ongoing){
                    alert("Another user is setting up a game on this foozbot")
                }
                else{
                    alert("A game is in progress on this Foozbot")
                }

            })
            .catch(error => { 
              console.log(error);
            });


        }}
    >
        <Image style={styles.icon} source={require('../assets/images/FoozBotIcon.png')}/>
        <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>
);

const HowToPlayButton = ({navigation, title }) => (

    <TouchableOpacity style={styles.button} onPress={ () => {navigation.navigate('userGuide')}}>
      <Image style={styles.icon} source={require('../assets/images/HowToPlay.png')}/>
      <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>

);

const LeaderboardButton = ({navigation, title }) => (

    <TouchableOpacity style={styles.button} onPress={ () => {navigation.navigate('leaderboard')}}>
      <Image style={styles.icon} source={require('../assets/images/Leaderboard.png')}/>
      <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>

);


const styles = StyleSheet.create({
    container: {
        backgroundColor: "black",
    },

    /* Logo Styles */

    logoSection:{
        flex: 2,
        minHeight: 100,
    },

    logo: {
        alignSelf: "center",
        height: 100,
        width: 300,
        
    },

    /* Text Styles */

    TextSection:{
        alignItems: 'center',
        color: 'blue',
        flex: 3,
        minHeight: 150,
    },

    TextHeader:{
        color: '#6ab3ff',
        fontSize: 40,
        fontWeight: '500',
        margin: 2,
        marginTop: 10
    },

    TextParagraph:{
        color: '#6ab3ff',
        fontWeight: '500',
        textAlign: 'center',
        paddingHorizontal: 5
    },


    /* Button Styles */

    button: {
        elevation: 8,
        backgroundColor: "#6ab3ff", //007dff
        paddingVertical: 10,
        paddingHorizontal: 12,
        margin: 10,
        minHeight: 90, 

        borderStyle: 'solid',
        borderColor: 'white',
        borderRadius: 5,
        borderWidth: 5,

        flex: 5,
        flexDirection: 'row',
      },
      buttonText: {
        fontSize: 30,
        color: "#fff",
        fontWeight: "bold",
        alignSelf: 'center',
        textTransform: "uppercase",
        padding: 8,
      },
      icon: {
        width: 70,
        height: 70,
        alignSelf: 'center'
      }
  
  });
