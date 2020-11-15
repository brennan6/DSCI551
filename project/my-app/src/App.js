import React, { Component } from 'react';
import SearchPage from './SearchPage';
import Title from './Title';
import firebase from 'firebase';
import config from "./config";

class App extends Component {
  constructor(props){
    super(props);
    firebase.initializeApp(config);

    this.state = {
      developers: []
    }
  }
  componentDidMount() {
    this.getUserData();
  }

  getUserData() {
    let ref = firebase.database().ref("songs");
    ref.on('value', snapshot => {
      console.log("FireB ",snapshot)
      console.log(snapshot.val())
      const state = snapshot.val();
      this.setState(state);
    });
    console.log('DATA RETRIEVED');
  }

  render() {
    return (
        <div className = "App">
            <SearchPage />
        </div>
    )
  }
}
export default App;