import React, { Component } from 'react';
import SearchPage from './SearchPage';
import firebase from 'firebase';
import config from "./config";

class App extends Component {
  constructor(props){
    super(props);
    firebase.initializeApp(config);
    this.state = {};
  }

  render() {
    return (
        <div className = "App">
            <SearchPage/>
        </div>
    )
  }
}
export default App;