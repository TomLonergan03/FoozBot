import { StyleSheet, Text, View, Image, Button, TouchableOpacity, ScrollView, FlatList } from 'react-native'
import React, {useState} from 'react'
import { StatusBar } from 'expo-status-bar';
import RNPickerSelect from 'react-native-picker-select';

import AsyncStorage from '@react-native-async-storage/async-storage';

export default function Leaderboard({navigation}) {

  const [entries, setEntries] = useState([])

  const [gamemode, setGamemode] = useState("")
  const [difficulty, setDifficulty] = useState("")
  const [sort, setSort] = useState("")

  return (
      <View>

        {/* Logo Title */}
        <View style={styles.logoSection}>
            <Image style={styles.logo} source={require('../assets/images/FoozBotLogoTwo.png')}/>
        </View>


        {/* Category Selection */}
        <View style={styles.dropdowns}>

        {/* Gamemode */}
        <View style={styles.dropdownContainer}>
          <RNPickerSelect
            style={{inputAndroid: styles.dropdown, placeholder: styles.dropdown}}
            placeholder={{label: "Gamemode", value: ""}}
            onValueChange={(value) => {
              GetData(value, difficulty, sort, entries, setEntries)
              setGamemode(value)
            }}
            items={[
              { label: "Highest Score", value: "Highest Score" },
              { label: "Lowest Time", value: "Lowest Time" },
            ]}
          />  
        </View>
 
        {/* Difficulty */}
        <View style={styles.dropdownContainer}>
          <RNPickerSelect
            style={{inputAndroid: styles.dropdown, placeholder: styles.dropdown}}
            placeholder={{label: "Difficulty", value: ""}}
            onValueChange={(value) => {
              GetData(gamemode, value, sort, entries, setEntries)
              setDifficulty(value)
            }}
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
            style={{inputAndroid: styles.dropdown, placeholder: styles.dropdown}}
            placeholder={{label: "Sort By", value: ""}}
            onValueChange={(value) => {
              GetData(gamemode, difficulty, value, entries, setEntries)
              setSort(value)
            }}
            items={[
              { label: "Score", value: "score" },
              { label: "Date (newest)", value: "newest" },
              { label: "Date (oldest)", value: "oldest" },
            ]}
          />  
        </View>
               
        </View>


        {/* Scrollable Table */}
        <List entries={entries} setEntries={setEntries}/>

        {/* <Button title="Clear" onPress={() => clearData()}/> */}


      <StatusBar />

      </View>

  )
}

const List = ({entries}) => {

  var rank = 0

  const items = entries.map(entry =>
    <View key={entry.id} style={styles.tableEntry}>

      <Text style={styles.tableRank}>#{rank += 1}</Text>
      <Text style={styles.tableText}>{entry.name}</Text>
      <Text style={styles.tableText}>{entry.p1Score} : {entry.p2Score}</Text>
      <Text style={styles.tableText}>{entry.arcadeScore}</Text>

    </View>
  )

  return(
    <ScrollView style={styles.table}>
      {items}
    </ScrollView>
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
      minWidth: '90%',
      minHeight: '80%',
      maxHeight: '80%',
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

      height:30,
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

    tableRank: {
      flex:1,
      alignSelf: 'center',
      padding:1,
      margin: 1,
      overflow: 'hidden',
      justifyContent:'center',

      height:30,
      color: '#f66628',
      fontWeight: '500',
      textAlign: 'center',
      paddingHorizontal: 0,
      padding: 5,

      borderStyle: 'solid',
      borderColor: 'black',
      borderRadius: 5,
      borderWidth: 2,

      maxWidth: 20,

      color: '#f66628',
    },

});

const storeData = async () => {

  const id = "17"

  let data = {
    id: id,
    name: "Elias",
    p1Score: "300",
    p2Score: "2",
    arcadeScore: 1111,
    gamemode: "Highest Score",
    difficulty: "Hard",
    date: new Date()
  }


  try {
    const jsonValue = JSON.stringify(data);
    await AsyncStorage.setItem(id, jsonValue);

  } catch (e) {
    console.log(e)
  }
};

const GetData = async (gamemode, difficulty, sort, entries, setEntries) => {

  let x = [];

  try {
    const keys = await AsyncStorage.getAllKeys();
    const results = await AsyncStorage.multiGet(keys);


    for (const result of results){
      const entry = JSON.parse(result[1])
      
      //if the selected value isnt set, or the stored matches the selected, then it can be displayed.  
      if (!gamemode || entry.gamemode == gamemode){
        if (!difficulty || entry.difficulty == difficulty)
          x.push(entry)
      }
    }

    //Now, sort by the given sort option. Default is by newest
    if (sort == "score"){
      setEntries(x.sort((a, b) => b.arcadeScore - a.arcadeScore))
    }
    else if (sort == "oldest"){
      setEntries(x.sort((a, b) => new Date(a.date) - new Date(b.date)))
    }
    else{
      setEntries(x.sort((a, b) => new Date(b.date) - new Date(a.date)))
    }


  } catch (e) {
    // error reading value
    console.log(e)
  }
};


const clearData = async() => {
  AsyncStorage.clear();
}