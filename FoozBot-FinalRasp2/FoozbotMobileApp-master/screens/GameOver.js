import { StyleSheet, Text, View, Alert, Image, BackHandler, Button, TouchableOpacity} from 'react-native';
import React, { useEffect, useState } from 'react'
import { StatusBar } from 'expo-status-bar';

export default function GameOver({route, navigation}) {

    const { name, scoreOne, scoreTwo, difficulty, gamemode, arcScore} = route.params;

  return (
    <View style={styles.container}>
      <View style={styles.mainContainer}>

  
        {/* Game In Progress Info */}
        <View style={styles.logoSection}>
            <Image style={styles.icon} source={require('../assets/images/FoozBotIcon.png')}/>
            <Text style={styles.TextHeader}>Game Over!</Text>
        </View>

        {/* Scores Display */}

          {/* Score Boxes */}

          <View style={styles.TextSection}>
            <ScoreBox scoreOne={scoreOne} scoreTwo={scoreTwo}  />
          </View>


          {/* Table */}
          <View style={styles.TextSection}>


            <WinnerPOV scoreOne= {scoreOne} scoreTwo={scoreTwo} />

            <Text style={styles.TextParagraph}>Name of Player: {name}</Text>
            <Text style={styles.TextParagraph}>Score: {arcScore}</Text>
            <Text style={styles.TextParagraph}>Gamemode: {gamemode}</Text>
            <Text style={styles.TextParagraph}>Difficulty: {difficulty}</Text>

          </View>



        {/* End Game */}
        <View style={styles.Button}>

            <ConnectButton 
              navigation={navigation} 
              title="Finish Game Early" 
              />

        </View>

      </View>
      <StatusBar />
    </View>
  )
}

//End Game Early
const ConnectButton = ({navigation}) => {

    return (
      <TouchableOpacity style={styles.button}           
          onPress={() => {
  
              navigation.navigate('connect')
  
          }}
      >
          <Image style={styles.icon} source={require('../assets/images/Football.png')}/>
          <Text style={styles.buttonText}>{"Return To Menu"}</Text>
      </TouchableOpacity>
  )};
  

//Changes based on who won the game
const WinnerPOV = scores =>{

  const one = scores.scoreOne
  const two = scores.scoreTwo

  if (one > two) {
    return(
      <Text style={styles.TextHeader}>Player One Wins!</Text>
    )
  }
  else if (one < two){
    return(
      <Text style={styles.TextHeader}>Player Two Wins!</Text>
    )
  }
  else{
    return(
      <Text style={styles.TextHeader}>Its A Draw!</Text>
    )
  }

}

//Score Display Boxes
const ScoreBox = scores =>{

  const one = scores.scoreOne
  const two = scores.scoreTwo

  
  //If Equal, then boxes are same color
  if (one == two){
    return (
      <View style={styles.scoreSection}>

        {/* Boxone */}
        <View style={styles.scoreBoxLoss}>
          <Text style={styles.scoreNumberLoss}>{scores.scoreOne}</Text>
        </View>
    
    
        {/* BoxTwo */}
        <View style={styles.scoreBoxLoss}>
          <Text style={styles.scoreNumberLoss}>{scores.scoreTwo}</Text>
        </View>
    </View>
    )
  }
  //If One > Two, one is orange
  else if (one > two){
    return (
      <View style={styles.scoreSection}>

      {/* Boxone */}
      <View style={styles.scoreBoxWin}>
        <Text style={styles.scoreNumberWin}>{scores.scoreOne}</Text>
      </View>
  
  
      {/* BoxTwo */}
      <View style={styles.scoreBoxLoss}>
        <Text style={styles.scoreNumberLoss}>{scores.scoreTwo}</Text>
      </View>
  
    </View>
    )
  }
  //If Equal, then boxes are same color
  return (
    <View style={styles.scoreSection}>

      {/* Boxone */}
      <View style={styles.scoreBoxLoss}>
        <Text style={styles.scoreNumberLoss}>{scores.scoreOne}</Text>
      </View>
  
  
      {/* BoxTwo */}
      <View style={styles.scoreBoxWin}>
        <Text style={styles.scoreNumberWin}>{scores.scoreTwo}</Text>
      </View>

  </View>
  )
}


const styles = StyleSheet.create({
    container: {
        backgroundColor: "black",
    },

    /* Logo Styles */

    logoSection:{
        flex: 2,
        minHeight: 100,
        flexDirection: 'row',
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
        fontSize: 30,
        fontWeight: '500',
        margin: 2,
        marginTop: 10,
        alignSelf:'center'
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
        fontSize: 25,
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

      //Scores
      scoreSection:{
        alignItems: 'center',
        color: 'blue',
        flex: 1,
        minHeight: 150,
        flexDirection:'row',
      },
      scoreBoxLoss:{
        borderStyle: 'solid',
        borderColor: 'white',
        borderRadius: 1,
        borderWidth: 5,
        width:100,
        height:100,
        margin:3,
        backgroundColor:'white',
        justifyContent:'center',
      },
      scoreNumberLoss:{
        color: 'black',
        fontSize: 60,
        fontWeight: '500',
        alignSelf:'center',
      },
      scoreBoxWin:{
        borderStyle: 'solid',
        borderColor: 'white',
        borderRadius: 1,
        borderWidth: 5,
        width:100,
        height:100,
        margin:3,
        backgroundColor:'#f66628',
        justifyContent:'center',
      },
      scoreNumberWin:{
        color: 'white',
        fontSize: 60,
        fontWeight: '500',
        alignSelf:'center',
      },
  
      foozballImage:{
        height: '100',
        width:'500',
        transform: [{rotate: '45deg'}],
      }

  });
