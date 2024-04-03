import { StyleSheet, Text, View, ImageBackground, Image, TextInput, Button, ScrollView } from 'react-native';
import React from 'react'

export default function UserGuide({navigation}) {
  return (
    <View>

        {/* Logo Title */}
        <View style={styles.logoSection}>
            <Image style={styles.logo} source={require('../assets/images/FoozBotLogoTwo.png')}/>
        </View>


      <ScrollView style={styles.table}>



        <View style={styles.helpBubble}>
          <Text style={styles.helpBubbleHeader}><Text style={styles.helpBubbleStepNumber}>Step One</Text> - Connect To The Foozbot</Text>
          <Text style={styles.helpBubbleText}>Press the connect button on the app. Make sure you're phone is connected to the same wifi as the robot.</Text>
        </View>

        <View style={styles.helpBubble}>
          <Text style={styles.helpBubbleHeader}><Text style={styles.helpBubbleStepNumber}>Step Two</Text> - Choose your Settings</Text>
          <Text style={styles.helpBubbleText}>Choose a name to be displayed in the leaderboards - please be respectful. Then choose a difficulty for the robots' AI, and a "Gamemode" - which is the rules that the robot plays by.</Text>
        </View>

        <View style={styles.helpBubble}>
          <Text style={styles.helpBubbleHeader}><Text style={styles.helpBubbleStepNumber}>Step Three</Text> - Play The Game</Text>
          <Text style={styles.helpBubbleText}>Press the connect button on the app. Make sure you're phone is connected to the same wifi as the robot.</Text>
        </View>

        <View style={styles.helpBubble}>
          <Text style={styles.helpBubbleHeader}><Text style={styles.helpBubbleStepNumber}>Step Four</Text> - End The Game</Text>
          <Text style={styles.helpBubbleText}>Press the connect button on the app. Make sure you're phone is connected to the same wifi as the robot.</Text>
        </View>



      </ScrollView>



    </View>
  )
}

const styles = StyleSheet.create({
  container: {
      backgroundColor: "black",
      minHeight: '100%',
      minWidth: '100%',
  },
  border:{
    borderStyle: 'solid',
    borderColor: 'red',
    borderRadius: 14,
    borderWidth: 5,
    width:100,
    height:100,
  },

  selector:{
    minHeight:100,
    borderStyle: 'solid',
    borderColor: 'red',
    borderRadius: 14,
    borderWidth: 5,
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
      backgroundColor: "#6ab3ff",
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

    dropdowns: {
      flex:1,
      flexDirection:'row',
      minWidth: '70%',
      maxWidth: '70%',
      minHeight:'10%',
      justifyContent: 'center',
      alignContent: 'center',
      alignItems: 'center',
      alignSelf: 'center'
    },

    dropdownContainer: {

      backgroundColor: "#6ab3ff",
      borderStyle: 'solid',
      borderColor: 'white',
      borderRadius: 10,
      borderWidth: 4,
      alignSelf: 'center',
      margin: 4,

      minWidth: '10%',
      maxWidth: '40%',
    },

    dropdown: {
      minHeight: 50, 
      minWidth: 150,
      color: 'white',
      fontWeight: '800',
      textTransform: "uppercase",
      fontSize: 30,
    },

    table: {

      backgroundColor: "#333030",
      borderStyle: 'solid',
      borderColor: '#333030',
      borderRadius: 10,
      borderWidth: 5,
      minWidth: '99%',
      minHeight: '70%',
      maxHeight: '100%',
      alignSelf: 'center',
      margin: 20,
      padding:10,

    },
    tableEntry: {
      flex:1,
      flexDirection: 'row',
      justifyContent:'center',
      alignItems:'center',
    },

    tableText: {
      flex:1,
      alignSelf: 'center',
      padding:3,
      margin: 1,
      overflow: 'hidden',
      justifyContent:'center',

      height:50,
      color: '#007dff',
      fontWeight: '500',
      textAlign: 'center',
      paddingHorizontal: 1,
      
      borderStyle: 'solid',
      borderColor: 'black',
      borderRadius: 5,
      borderWidth: 2,

      color:'white',
    },

    helpBubble:{      
      backgroundColor: "#6ab3ff",
      paddingVertical: 0,
      paddingHorizontal: 4,
      margin: 2,
      minHeight: 10, 

      borderStyle: 'solid',
      borderColor: 'white',
      borderRadius: 5,
      borderWidth: 5,

      padding: 6,

      flex: 1,
    },

    helpBubbleHeader:{
      fontSize: 20,
      color: "#fff",
      fontWeight: "bold",
      alignSelf: 'flex-start',
      textAlign: 'right',
      textTransform: "uppercase",
      padding:4,
    },

    helpBubbleText:{
      fontSize: 15,
      color: "#fff",
      fontWeight: "bold",
      alignSelf: 'center',
      padding: 8,
    },

    helpBubbleStepNumber:{
      fontSize: 20,
      color: "#f66628",
      fontWeight: "bold",
      alignSelf: 'flex-start',
      textTransform: "uppercase",
    },

});