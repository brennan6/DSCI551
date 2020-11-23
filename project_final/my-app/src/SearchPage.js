import React, { useState, useEffect } from 'react';
import SearchBar from './SearchBar';
import SongList from './SongList';
import firebase from 'firebase';
import Title from './Title';

const SearchPage = (props) => {
  var [input, setInput] = useState('');
  var [songListDefault, setSongListDefault] = useState();
  var [songList, setSongList] = useState();
  var dataInput = []

  const fetchSongData = () => {
    let ref = firebase.database().ref("songs/songs");
    ref.on('value', snapshot => {
      var arr = [];
      for (var i=0; i < 200; i++) {
        const state = snapshot.child(i).val();
        arr.push(state)
      } 
      dataInput = {data: arr}
      songListDefault = dataInput
      setSongListDefault(songListDefault)
    });
  }

  const updateInput = (input) => {

    const filtered = songListDefault["data"].filter(song => {
     return song.title.toLowerCase().includes(input)
    })
    setInput(input);
    songList = {data: filtered}
    setSongList(songList)
  }

  useEffect( () => {fetchSongData()});
	
  return (
    <>
      <h1>Song List</h1>
      <SearchBar 
       input={input}
       onChange={updateInput}
      />
      <SongList songList={songList}/>
      <Title/>
    </>
   );
}

export default SearchPage