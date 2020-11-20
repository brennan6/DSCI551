
const RankDB =  async () => {
    /*await fetch('http://localhost:8080/ranks', {
        method: 'GET'
    }).then(function(response) {
        const items = response.json()
        console.log(items)
    }).then((items) => {
        return items.song;
      });*/
      
    fetch('http://localhost:8080/ranks/posts', {
        method: 'POST',
        headers: {'Content-Type': 'application/json',
        'Accept': 'application/json'},
        body: JSON.stringify({
            song: "Up Down",
            score: "5"
        })
    }).then(function(response) {
        const items = response.json()
        console.log(items)
    })
    
    return (
        <ul></ul>
        );
}
export default RankDB