import React, { useState } from 'react';
import RankDB from './RankDB';

const SongList = ({songList=[]}) => {
  const [showResultsSong, setShowResultsSong] = React.useState(false)
  const [showResultsRank, setShowResultsRank] = React.useState(false)
  const [reset, setReset] = React.useState(false)
  const [count, setCount] = useState(0);
  const onClickSong = () => setShowResultsSong(true)
  const onClickSongNegate = () => setShowResultsSong(false)
  const onClickRank = () => setShowResultsRank(true)
  /*const onClickReset = () => setReset(true)*/
  const resetBools = () => {
    setShowResultsRank(false);
    setShowResultsSong(false);
    setCount(0)
  }

  if (Object.keys(songList).length) {
    if (Object.keys(songList["data"]).length) {
      return (
        <ul>
          {songList["data"].map((song,index)=>{
              return <li key={index}>
              <button onClick={onClickSong}>{song.title}</button>
              {showResultsSong ? <p>{"album: " + song.album} </ p> : <p/>}
              {showResultsSong ? <p>{"artist: " + song.artist} </ p> : <p/>}
              {showResultsSong ? <p>{"year: " + song.year} </ p> : <p/>}
              {showResultsSong ? <p>{"lyrics: " + song.lyrics} </ p> : <p/>}
              {showResultsSong ? <p>{"average rank: " + song.avg_rank} </ p> : <p/>}
              {showResultsSong ? <p>{"count ranks: " + song.count_ranks} </ p> : <p/>}
              {showResultsSong ? <button onClick={onClickRank}>Rank</button> : <p/>}
              
              {showResultsRank ? <div>
                                    <button onClick={() => setCount(1)}>1 </button>
                                    <button onClick={() => setCount(2)}>2 </button>
                                    <button onClick={() => setCount(3)}>3 </button>
                                    <button onClick={() => setCount(4)}>4 </button>
                                    <button onClick={() => setCount(5)}>5 </button>
                                 </div> : <p/>}
              {count ? <div><p>{"Ranking: " + count}</p><RankDB
                                                        song={song.title}
                                                        score={count}
                                                        /></div> : <p/>}
              {showResultsSong ? <button onClick={resetBools}>Reset</button> : <p/>}
              </li>
          })}
        </ul>
      )
    }
  }
  return null;

}
export default SongList