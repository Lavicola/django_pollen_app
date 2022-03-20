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
    el: '#table',
    delimiters: ['{[', ']}'],
    data: {
        csrfTokenName: "csrftoken",
        nepenthes: [],
        file_element: "",
        dropdown_sex_element: "dropdown_sex_",
        dropdown_shipping_element: "dropdown_shipping_",
        dropdown_flower_element: "dropdown_flower_",
        name_element: "name_",
        description_element: "description_",
        file_element: "file_",
        axios: axios,
    },
    mounted: function () {
        this.getNepenthes();

        this.axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
        this.axios.defaults.xsrfCookieName = "csrftoken";
        this.axios.defaults.withCredentials = true;

    },
    methods: {
        getToken: function (name) {
            // https://stackoverflow.com/a/15724300
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
        },
        getNepenthes: function () {
            let api_base_url = '/api/nepenthes/edit/1';
            this.axios.get(api_base_url)
                .then((response) => {
                    this.nepenthes = response.data;
                }).catch(error => {
                console.log(error);
            })
        },
        updateNepenthes: function (id) {

            let name = document.getElementById(this.name_element + id).innerText;
            let description = document.getElementById(this.description_element + id).innerText;
            let sex = document.getElementById(this.dropdown_sex_element + id).value;
            let shipping = document.getElementById(this.dropdown_shipping_element + id).value;
            let flower = document.getElementById(this.dropdown_flower_element + id).value;
            let file = document.getElementById(this.file_element + id).files[0];

            let formData = new FormData();
            let csrf_token = this.getToken(this.csrfTokenName);

            formData.append("name", name);
            formData.append("description", description);
            formData.append("sex", sex);
            formData.append("shipping", shipping);
            formData.append("flower", flower);
            formData.append("image", file);
            formData.append("csrfmiddlewaretoken", csrf_token);

            // todo use put/patch instead post
            this.axios.put('/api/nepenthes/edit/'+id, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });


        },
        removeNepenthes: function (index) {
            // TODO delete request

            axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            axios.defaults.xsrfCookieName = "csrftoken";
            axios.defaults.withCredentials = true;

            this.axios.delete('/api/nepenthes/edit/' + this.nepenthes[index].id, {
                headers: {
                },
                data: {
                }
            });

            //this.$delete(this.nepenthes, index);

        },


    }
});




