import { StyleSheet, Text, View, ImageBackground, Image, TextInput, Button, TouchableOpacity} from 'react-native';
import React, { useState } from 'react'
import { StatusBar } from 'expo-status-bar';
import RNPickerSelect from 'react-native-picker-select';

export default function Setup({route, navigation}) {

    const [name, setName] = useState(null)
    const [gamemode, setGamemode] = useState(null)
    const [difficulty, setDifficulty] = useState(null)
    const {sessionID, ip} = route.params;

  return (
      <View>

        {/* Logo Title */}
        <View style={styles.logoSection}>
            <Image style={styles.logo} source={require('../assets/images/FoozBotLogo.png')}/>
        </View>

        {/* Text Component */}
        <View style={styles.TextSection}>

            <Text style={styles.TextHeader}>Set up a Game!</Text>
            <Text style={styles.TextParagraph}>Enter your name, then select your favourite gamemode and difficulty setting. After pressing the start button, you can begin the game on your foozbot!</Text>

        </View>


        {/* Connect and User Guide Buttons */}
        <View style={styles.buttonWrapper}>

            <TextInput 
                style={styles.textInput} 
                maxLength={10}
                onChangeText={text => setName(text)}
                placeholder='Enter Your Name'

            />
        </View>

            <View style={styles.dropdownContainer}>

            <RNPickerSelect
            style={{inputAndroid: styles.dropdown}}
            placeholder={{label: "Difficulty", value: null}}
            onValueChange={(value) => setDifficulty(value)}
            items={[
                { label: "Easy", value: "Easy" },
                { label: "Medium", value: "Medium" },
                { label: "Hard", value: "Hard" },
                { label: "Insane", value: "Insane" },
            ]}
            />
            
            </View>

            <View style={styles.dropdownContainer}>

                <RNPickerSelect
                style={{inputAndroid: styles.dropdown}}
                placeholder={{label: "Gamemode", value: null}}
                items={[
                    { label: "Highest Score", value: "Highest Score" },
                    { label: "Lowest Time", value: "Lowest Time" },
                ]}
                onValueChange={(value) => setGamemode(value)}
                />
            
            </View>

            <ConnectButton navigation={navigation} title="Start Game!" name={name} difficulty={difficulty} gamemode={gamemode} sessionID={sessionID} ip={ip}/>




      <StatusBar />
    </View>
  )
}


const ConnectButton = ({navigation, title, name, difficulty, gamemode, sessionID, ip}) => (
    <TouchableOpacity style={styles.button}           
        onPress={() => {

          //Make sure a name, diff, and Gamemode are set
          if (name == null){
            alert("Please Set a name (up to 10 characters)")
          }
          else if (difficulty == null){
            alert("Please Set a Difficulty Level")
          }
          else if (gamemode == null){
            alert("Please Set a Gamemode")
          }
          else{
            const response = fetch(ip, {
              method: 'POST',
              body: JSON.stringify({
                name: name,
                difficulty: difficulty,
                gamemode: gamemode,
                sessionID: sessionID,
                stop:false,
              })
              })
            .then( (response) => response.json())
            .then(json => {
                if (json.start){
                    alert("Game Beginning!")
                    navigation.navigate('gameInProgress', {name: name, difficulty: difficulty, gamemode: gamemode, sessionID: sessionID, ip:ip})
                }

                else{
                    alert("Someone Else has started a game on this Foozbot, Try Again Later")
                }

            })
            .catch(error => { 
              console.error(error);
            });

        }}
      }
    >
        <Image style={styles.icon} source={require('../assets/images/Football.png')}/>
        <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>
);

const SelectButtons = ({navigation, title }) => (

    <TouchableOpacity style={styles.selectButton} onPress={ () => {navigation.navigate('userGuide')}}>

      <Text style={styles.smallButtonText}>{title}</Text>
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
        resizeMode: 'contain',
        
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

    textInput: {
        backgroundColor: "grey",
        paddingVertical: 10,
        paddingHorizontal: 12,
        margin: 10,
        minHeight: 60, 

        borderStyle: 'solid',
        borderColor: 'white',
        borderRadius: 5,
        borderWidth: 5,

        textAlign:'center'
      },

    /* Button Styles */

    button: {
        elevation: 8,
        backgroundColor: "#007dff",
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
      },

      selectButton:{
        elevation: 8,
        backgroundColor: "#007dff",
        paddingVertical: 5,
        paddingHorizontal: 6,
        margin: 10,
        minHeight: 60, 

        borderStyle: 'solid',
        borderColor: 'white',
        borderRadius: 5,
        borderWidth: 5,

        flex: 5,
        flexDirection: 'row',
      },
      smallButtonText: {
        fontSize: 15,
        color: "#fff",
        fontWeight: "bold",
        alignSelf: 'center',
        textTransform: "uppercase",
        padding: 8,
      },
      smallIcon: {
        width: 50,
        height: 50,
        alignSelf: 'center'
      },
      dropdownContainer: {

        backgroundColor: "#6ab3ff",
        borderStyle: 'solid',
        borderColor: 'white',
        borderRadius: 10,
        borderWidth: 5,
        alignSelf: 'center',
        margin:6
  
      },
  
      dropdown: {
        margin: 10,
        minHeight: 40, 
        minWidth: 300,
        color: 'white',
        fontWeight: '800',
        textTransform: "uppercase",
        fontSize: 30,
      },
  
  });
