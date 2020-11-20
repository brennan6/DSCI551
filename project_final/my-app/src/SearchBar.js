import React from 'react';

const SearchBar = ({input:keyword, onChange:updateInput}) => {
  const BarStyling = {width:"20rem",background:"#F2F1F9", border:"none", padding:"0.5rem"};
  /*console.log(updateInput)*/
  /*console.log(keyword)*/
  return (
    <input 
     style={BarStyling}
     key="random1"
     defaultValue={keyword}
     placeholder={"search song title"}
     onChange={(e) => updateInput(e.target.value)}
    />
  );
}

export default SearchBar