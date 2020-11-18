
const RankDB = () => {
    fetch('http://localhost:8080/ranks', {
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            song: "Up Down",
            score: "4"
        })
    }).then(response => {
        const songs = response
        console.log(songs);
    })
    return (
        <ul></ul>
        );
}
export default RankDB