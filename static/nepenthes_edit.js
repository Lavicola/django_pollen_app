function include(file) {
    var script = document.createElement('script');
    script.src = file;
    script.type = 'text/javascript';
    script.defer = true;
    document.getElementsByTagName('head').item(0).appendChild(script);
}

include("https://cdn.jsdelivr.net/npm/vue@2.5.13/dist/vue.js");
include("https://cdnjs.cloudflare.com/ajax/libs/axios/0.21.1/axios.js");
include("https://unpkg.com/v-tooltip@2.0.2");

new Vue({
    el: '#nepenthes_search',
    delimiters: ['{[', ']}'],
    data: {
        csrfTokenName: "csrftoken",
        current_page: 0,
        perPage: 10,
        pages: [],
        all_nepenthes: [],
        nepenthes: [],
        filtert_nepenthes: [],
        widht_limit: 991, // if it is equal smaller we use mobile filter bad solution!
    },
    mounted: function () {
        this.getNepenthes();
    },
    methods: {
        getToken: function (name) {
            // https://stackoverflow.com/a/15724300
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        },
                getNepenthes: function () {
            let api_base_url = '/api/nepenthes/edit';
            axios.get(api_base_url)
                .then((response) => {


                }).catch(error => {
                console.log(error);
            })
        },
}});




