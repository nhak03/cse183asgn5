"use strict";

// Complete. 
let app = {};

app.data = {
    data: function() {
        return {
            posts: [],
            tags: [],
            potential_post: '',
            post_owner: false,
            filtered_by: []
        };
    },
    methods: {
        make_post(){
            const post = this.potential_post
            console.log("You are making a post: ", post);
            axios.post('/make_post', { post_content: post })
            .then(response => {
                if(response.status === 200){
                    console.log("Backend fulfilled our request to make a new post.")
                    this.potential_post = '';

                    app.load_data();
                }
                else{
                    console.log("error on making post");
                }
            
            })
        },
        filterBy(tag){
            const inverted = !tag.toggle;
            console.log("Toggling ", tag.name, " to: ", inverted);
            tag.toggle = inverted;
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