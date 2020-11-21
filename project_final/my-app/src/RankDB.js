
const RankDB = ({song:title, score:rank}) => {
    /*await fetch('http://localhost:8080/ranks', {
        method: 'GET'
    }).then(function(response) {
        const items = response.json()
        console.log(items)
    }).then((items) => {
        return items.song;
      });*/
    console.log(title)
    console.log(rank)

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
    
    return (
        <ul></ul>
        );
}
export default RankDB