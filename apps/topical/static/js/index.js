"use strict";

// Complete. 
let app = {};

app.data = {
    data: function() {
        return {
            posts: [],
            tags: [],
            potential_post: ''
        };
    },
    methods: {
        make_post(){
            console.log("You are making a post: ", this.potential_post);

            this.potential_post = '';
        }
    }
};

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