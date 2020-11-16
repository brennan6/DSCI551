import React from 'react';
import {View} from 'react'



const SongList = ({songList=[]}) => {
  var clicked = false
  const [showResultsSong, setShowResultsSong] = React.useState(false)
  const [showResultsRank, setShowResultsRank] = React.useState(false)
  const onClickSong = () => setShowResultsSong(true)
  const onClickRank = () => setShowResultsRank(true)
  /*console.log(songList)*/
  /*console.log(Object.keys(songList).length)*/
  if (Object.keys(songList).length) {
    /*console.log(Object.keys(songList["data"]).length)*/
    if (Object.keys(songList["data"]).length) {
      /* console.log(songList["data"]) */
      return (
        <ul>
          {songList["data"].map((song,index)=>{
              return <li key={index}><button onClick={onClickSong}>{song.title}
              </button>
              {showResultsSong ? <p>{"album: " + song.album} </ p> : <p/>}
              {showResultsSong ? <p>{"artist: " + song.artist} </ p> : <p/>}
              {showResultsSong ? <p>{"year: " + song.year} </ p> : <p/>}
              {showResultsSong ? <p>{"lyrics: " + song.lyrics} </ p> : <p/>}
              {showResultsSong ? <button onClick={onClickRank}>Rank</button> : <p/>}
              
              {showResultsRank ? <div>
                                    <button>1 </button>
                                    <button>2 </button>
                                    <button>3 </button>
                                    <button>4 </button>
                                    <button>5 </button>
                                 </div> : <p/>}
              </li>
          })}
        </ul>
      )
    }
  }
  return null;

}
export default SongList