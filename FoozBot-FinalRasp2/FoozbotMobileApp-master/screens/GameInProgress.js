import { StyleSheet, Text, View, Alert, Image, BackHandler, Button, TouchableOpacity} from 'react-native';
import React, { useEffect, useState } from 'react'
import { StatusBar } from 'expo-status-bar';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function GameInProgress({route, navigation}) {

    const [scoreOne, setScoreOne] = useState(0)
    const [scoreTwo, setScoreTwo] = useState(0)
    const [arcScore, setArcScore] = useState(0)

    const { name, difficulty, gamemode, sessionID, ip} = route.params;

    useEffect(() => {
      const intervalId = setInterval(() => getScore(), 1000);
      console.log(ip);
      return () => clearInterval(intervalId);
    }, [])

    const getScore = () => {

      const response = fetch(ip, { method: 'GET'})
      .then( (response) => response.json())
      .then(json => {
        setScoreOne(JSON.parse(json.p1Score))
        setScoreTwo(JSON.parse(json.p2Score))
        setArcScore(JSON.parse(json.arcScore))

        if(! JSON.parse(json.gameEnded)){
          endGame(navigation, sessionID, ip, name, JSON.parse(json.p1Score), JSON.parse(json.p2Score), gamemode, difficulty, JSON.parse(json.arcScore))
        }

      })
      .catch(error => { 
        console.log(error);

      });

    }

  return (
    <View style={styles.container}>
      <View style={styles.mainContainer}>

  
        {/* Game In Progress Info */}
        <View style={styles.logoSection}>
            <Image style={styles.icon} source={require('../assets/images/FoozBotIcon.png')}/>
            <Text style={styles.TextHeader}>Game In Progress</Text>
        </View>

        {/* Scores Display */}

          {/* Score Boxes */}

          <View style={styles.TextSection}>
            <ScoreBox scoreOne={scoreOne} scoreTwo={scoreTwo}  />
          </View>


          {/* Table */}
          <View style={styles.TextSection}>
            <Image style={styles.foozballImage} source={require('../assets/images/foozballTable.png')}/>
          </View>



        {/* End Game */}
        <View style={styles.Button}>

            <ConnectButton 
              navigation={navigation} 
              title="Finish Game Early" 
              sessionID={sessionID}
              name= {name}
              scoreOne= {scoreOne}
              scoreTwo={scoreTwo}
              difficulty={difficulty}
              gamemode={gamemode}
              ip={ip}
              arcScore={arcScore}
              />

        </View>

      </View>
      <StatusBar />
    </View>
  )
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



//End Game Early
const ConnectButton = ({navigation, sessionID, name, scoreOne, scoreTwo, gamemode, difficulty, ip, arcScore}) => {

  return (
    <TouchableOpacity style={styles.button}           
        onPress={() => {endGame(navigation, sessionID, ip, name, scoreOne, scoreTwo, gamemode, difficulty, arcScore)}}
    >
        <Image style={styles.icon} source={require('../assets/images/Football.png')}/>
        <Text style={styles.buttonText}>{"End Game "}</Text>
    </TouchableOpacity>
)};

const endGame = (navigation, sessionID, ip, name, scoreOne, scoreTwo, gamemode, difficulty, arcScore) => {

  const response = fetch(ip, {
    method: 'POST',
    body: JSON.stringify({
      sessionID: sessionID,
      stop:true,
    })
    })
  .catch(error => { 
    console.error(error);
  });

  storeData(name, scoreOne, scoreTwo, gamemode, difficulty, arcScore)

  navigation.navigate('connect')
  navigation.navigate('gameOver', {name: name, scoreOne, scoreTwo,  difficulty: difficulty, gamemode: gamemode, arcScore})
}








const storeData = async (name, scoreOne, scoreTwo, gamemode, difficulty, arcScore) => {
  try {
    const keys = await AsyncStorage.getAllKeys();
    const results = await AsyncStorage.multiGet(keys);
    id = results.length.toString() + 1

    let data = {
      id: id,
      name: name,
      p1Score: scoreOne,
      p2Score: scoreTwo,
      arcadeScore: arcScore,
      gamemode: gamemode,
      difficulty: difficulty,
      date: new Date()
    }

    const jsonValue = JSON.stringify(data);
    await AsyncStorage.setItem(id, jsonValue);

  } catch (e) {
    // error reading value
    console.log(e)
    alert("There was a Problem saving the game")
  }
};













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
        color: '#007dff',
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
        resizeMode: 'contain',
        borderColor: 'white',
        borderRadius: 1,
        borderWidth: 5,
        
      }

  });
