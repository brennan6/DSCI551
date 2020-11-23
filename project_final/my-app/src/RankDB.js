import React, { useState } from 'react';

const RankDB = ({song:title, score:rank}) => {
    const [allowRank, setAllowRank] = React.useState(false)
    const [allowRecommend, setAllowRecommend] = React.useState(false)
    const [songRec, setSongRec] = useState("");
    const onPost = () => setAllowRank(true)
    const onGet = () => setAllowRecommend(true)

    if (!allowRank) {
        onPost()
        fetch('http://localhost:8080/ranks/posts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json',
            'Accept': 'application/json'},
            body: JSON.stringify({
                song: title,
                score: rank
            })
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            const items = data;
            console.log(items)
        })
    }
    if (!allowRecommend) {
        onGet()
        fetch('http://localhost:8080/ranks', {
        method: 'GET'
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            const rec_song = data;
            console.log(rec_song)
            setSongRec(rec_song["song"]);
        })
    }
    
    return (
        <p>{"Recommended Next: " + songRec}</p>
        );
}
export default RankDB