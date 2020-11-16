import React from 'react';



const SongList = ({songList=[]}) => {
  var clicked = false
  const [showResults, setShowResults] = React.useState(false)
  const onClick = () => setShowResults(true)
  /*console.log(songList)*/
  /*console.log(Object.keys(songList).length)*/
  if (Object.keys(songList).length) {
    /*console.log(Object.keys(songList["data"]).length)*/
    if (Object.keys(songList["data"]).length) {
      /* console.log(songList["data"]) */
      return (
        <ul>
          {songList["data"].map((song,index)=>{
              return <li key={index}><button onClick={onClick}>{song.title}
              </button>
              {showResults ? <p>{"album: " + song.album} </ p> : <p/>}
              {showResults ? <p>{"artist: " + song.artist} </ p> : <p/>}
              {showResults ? <p>{"year: " + song.year} </ p> : <p/>}
              {showResults ? <p>{"lyrics: " + song.lyrics} </ p> : <p/>}
              </li>
          })}
        </ul>
      )
    }
  }
  return null;

}
export default SongList