"use strict";

// Complete. 
let app = {};

app.data = {
    data: function() {
        return {
            posts: [],
            tags: []
        };
    },
    methods: {

    }
}

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    // Complete.
    console.log("Called load data:");
    axios.get('/get_home').then(response => {
        if(response.status === 200){
            app.vue.posts = response.data.posts;
            app.vue.tags = response.data.tags;
            console.log("Backend YAY");
        }
        else{
            alert("Backend NAY");
        }
    })
}

app.load_data();