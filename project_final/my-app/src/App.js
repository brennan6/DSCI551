import React, { Component } from 'react';
import SearchPage from './SearchPage';
import Title from './Title';
import firebase from 'firebase';
import config from "./config";

class App extends Component {
  constructor(props){
    super(props);
    firebase.initializeApp(config);
    this.state = {};
  }

  /*componentDidMount() {
    this.getUserData();
  }

  getUserData() {
    let ref = firebase.database().ref("songs/songs");
    ref.on('value', snapshot => {
      var arr = [];
      console.log(snapshot.child("0").val())
      for (var i=0; i < 200; i++) {
        const state = snapshot.child(i).val();
        arr.push(state)
      } 
      this.setState({data: arr});
    });
    console.log('DATA RETRIEVED');
  }*/

  render() {
    var dataInput = this.state
    return (
        <div className = "App">
            <SearchPage/>
        </div>
    )
  }
}
export default App;