
;(async () => {
    if(!localStorage.getItem("last_channel")) return;
    const channel = localStorage.getItem("last_channel");
    const res = fetch("/getchannel/" + channel);
    if(res.status === 404) return
    window.open("/channels/" + channel, "_self");
});

/*if (localStorage.getItem('last_channel')) {
    let channel = localStorage.getItem('last_channel');
    window.location.replace('/channels/' + channel);
}*/
