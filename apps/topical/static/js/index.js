"use strict";

// Complete. 
let app = {};

app.data = {
    data: function() {
        return {
            posts: [],
            org_posts: [], // array used to contain a copy of the entire posts, and then we put the filtered ones into posts[]
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
        filter(){
            console.log("filtering by: ", this.filtered_by);
            this.posts = [];
            for(let i=0; i < this.org_posts.length; i++){
                // for each post, check if their tag list contains all elements of the filtered_by list
                let post = this.org_posts[i];
                // console.log("Analyzing post: ", post);
                // console.log("Tag List: ", post.tags);

                let put_in = true;
                for(let tag_num in this.filtered_by){
                    let tag_name = this.filtered_by[tag_num];
                    console.log("Enforcing the ", tag_name, " filter");
                    const index = (post.tags).indexOf(tag_name);
                    if(index > -1){
                        put_in = true;
                    }
                    else{
                        put_in = false;
                        break;
                    }
                }

                if (put_in){
                    this.posts.push(post);
                }
            }
        },
        filterBy(tag){
            const inverted = !tag.toggle;
            console.log("Toggling ", tag.name, " to: ", inverted);
            tag.toggle = inverted;
            if (inverted){
                // if true, filter by this tag
                this.filtered_by.push(tag.name);
                this.filter();
            }
            else{
                // else, remove the filter
                const index = this.filtered_by.indexOf(tag.name);
                if (index > -1) {
                    // Remove the element at the found index
                    this.filtered_by.splice(index, 1);
                    this.filter();
                }
            }
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
            app.vue.org_posts = response.data.posts;
            app.vue.tags = response.data.tags;
            console.log("Backend YAY");
        }
        else{
            alert("Backend NAY");
        }
    })
}

app.load_data();